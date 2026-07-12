from django.contrib import messages
from django.contrib.auth import login
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect, get_object_or_404

from .forms import SignUpForm, AppointmentForm
from .models import Service, Product, Appointment, Order, OrderItem


def home(request):
    services = Service.objects.filter(active=True)[:6]
    products = Product.objects.filter(active=True)[:6]
    return render(request, "salon/home.html", {"services": services, "products": products})


def service_list(request):
    services = Service.objects.filter(active=True)
    return render(request, "salon/service_list.html", {"services": services})


def product_list(request):
    products = Product.objects.filter(active=True)
    return render(request, "salon/product_list.html", {"products": products})


def signup(request):
    if request.method == "POST":
        form = SignUpForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            messages.success(request, "Welcome! Your account has been created.")
            return redirect("home")
    else:
        form = SignUpForm()
    return render(request, "registration/signup.html", {"form": form})


@login_required
def book_appointment(request):
    if request.method == "POST":
        form = AppointmentForm(request.POST)
        if form.is_valid():
            appointment = form.save(commit=False)
            appointment.client = request.user
            appointment.save()
            messages.success(request, "Your appointment request has been submitted.")
            return redirect("my_appointments")
    else:
        form = AppointmentForm()
    return render(request, "salon/book_appointment.html", {"form": form})


@login_required
def my_appointments(request):
    appointments = request.user.appointments.all()
    return render(request, "salon/my_appointments.html", {"appointments": appointments})


@login_required
def cancel_appointment(request, pk):
    appointment = get_object_or_404(Appointment, pk=pk, client=request.user)
    if request.method == "POST":
        appointment.status = "cancelled"
        appointment.save()
        messages.info(request, "Appointment cancelled.")
    return redirect("my_appointments")


@login_required
def buy_product(request, pk):
    """Simple one-click purchase: creates an order with a single product line."""
    product = get_object_or_404(Product, pk=pk, active=True)
    if request.method == "POST":
        quantity = int(request.POST.get("quantity", 1) or 1)
        if quantity < 1:
            quantity = 1
        if quantity > product.stock:
            messages.error(request, f"Only {product.stock} left in stock.")
            return redirect("product_list")

        order = Order.objects.create(client=request.user, status="paid")
        OrderItem.objects.create(order=order, product=product, quantity=quantity, price=product.price)
        product.stock -= quantity
        product.save()
        messages.success(request, f"Thanks! You bought {quantity} x {product.name}.")
        return redirect("my_orders")
    return redirect("product_list")


@login_required
def my_orders(request):
    orders = request.user.orders.all()
    return render(request, "salon/my_orders.html", {"orders": orders})
