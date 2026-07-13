"""
Custom staff dashboard — lets the salon owner manage services, products,
appointments and orders without touching /admin/.

Every view here is locked down to superusers only via `superuser_required`.
"""
from django.contrib import messages
from django.contrib.auth.decorators import login_required, user_passes_test
from django.shortcuts import render, redirect, get_object_or_404
from django.db.models import Count, Q

from .models import Service, Product, Appointment, Order
from .forms import ServiceForm, ProductForm


def superuser_required(view_func):
    """Only the superuser account may access these views."""
    decorated = user_passes_test(lambda u: u.is_superuser, login_url="login")
    return login_required(decorated(view_func))


# ---------- Dashboard home ----------

@superuser_required
def dashboard_home(request):
    context = {
        "pending_appointments": Appointment.objects.filter(status="pending").count(),
        "today_appointments": Appointment.objects.filter(status="confirmed").count(),
        "low_stock_products": Product.objects.filter(stock__lte=5, active=True).count(),
        "pending_orders": Order.objects.filter(status="pending").count(),
        "total_services": Service.objects.count(),
        "total_products": Product.objects.count(),
        "recent_appointments": Appointment.objects.all()[:5],
        "recent_orders": Order.objects.all()[:5],
        "active": "home",
    }
    return render(request, "dashboard/home.html", context)


# ---------- Services ----------

@superuser_required
def service_manage_list(request):
    services = Service.objects.all()
    return render(request, "dashboard/service_list.html", {"services": services, "active": "services"})


@superuser_required
def service_create(request):
    if request.method == "POST":
        form = ServiceForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "Service created.")
            return redirect("dashboard_services")
    else:
        form = ServiceForm()
    return render(request, "dashboard/service_form.html", {"form": form, "title": "Add Service", "active": "services"})


@superuser_required
def service_edit(request, pk):
    service = get_object_or_404(Service, pk=pk)
    if request.method == "POST":
        form = ServiceForm(request.POST, instance=service)
        if form.is_valid():
            form.save()
            messages.success(request, "Service updated.")
            return redirect("dashboard_services")
    else:
        form = ServiceForm(instance=service)
    return render(request, "dashboard/service_form.html", {"form": form, "title": "Edit Service", "active": "services"})


@superuser_required
def service_delete(request, pk):
    service = get_object_or_404(Service, pk=pk)
    if request.method == "POST":
        service.delete()
        messages.info(request, "Service deleted.")
    return redirect("dashboard_services")


# ---------- Products ----------

@superuser_required
def product_manage_list(request):
    products = Product.objects.all()
    return render(request, "dashboard/product_list.html", {"products": products, "active": "products"})


@superuser_required
def product_create(request):
    if request.method == "POST":
        form = ProductForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            messages.success(request, "Product created.")
            return redirect("dashboard_products")
    else:
        form = ProductForm()
    return render(request, "dashboard/product_form.html", {"form": form, "title": "Add Product", "active": "products"})


@superuser_required
def product_edit(request, pk):
    product = get_object_or_404(Product, pk=pk)
    if request.method == "POST":
        form = ProductForm(request.POST, request.FILES, instance=product)
        if form.is_valid():
            form.save()
            messages.success(request, "Product updated.")
            return redirect("dashboard_products")
    else:
        form = ProductForm(instance=product)
    return render(request, "dashboard/product_form.html", {"form": form, "title": "Edit Product", "active": "products"})


@superuser_required
def product_delete(request, pk):
    product = get_object_or_404(Product, pk=pk)
    if request.method == "POST":
        product.delete()
        messages.info(request, "Product deleted.")
    return redirect("dashboard_products")


# ---------- Appointments ----------

@superuser_required
def appointment_manage_list(request):
    status_filter = request.GET.get("status", "")
    appointments = Appointment.objects.all()
    if status_filter:
        appointments = appointments.filter(status=status_filter)
    return render(
        request,
        "dashboard/appointment_list.html",
        {
            "appointments": appointments,
            "status_filter": status_filter,
            "statuses": Appointment.STATUS_CHOICES,
            "active": "appointments",
        },
    )


@superuser_required
def appointment_update_status(request, pk, new_status):
    appointment = get_object_or_404(Appointment, pk=pk)
    valid_statuses = dict(Appointment.STATUS_CHOICES)
    if request.method == "POST" and new_status in valid_statuses:
        appointment.status = new_status
        appointment.save()
        messages.success(request, f"Appointment marked as {valid_statuses[new_status]}.")
    return redirect("dashboard_appointments")


# ---------- Orders ----------

@superuser_required
def order_manage_list(request):
    status_filter = request.GET.get("status", "")
    orders = Order.objects.all()
    if status_filter:
        orders = orders.filter(status=status_filter)
    return render(
        request,
        "dashboard/order_list.html",
        {"orders": orders, "status_filter": status_filter, "statuses": Order.STATUS_CHOICES, "active": "orders"},
    )


@superuser_required
def order_update_status(request, pk, new_status):
    order = get_object_or_404(Order, pk=pk)
    valid_statuses = dict(Order.STATUS_CHOICES)
    if request.method == "POST" and new_status in valid_statuses:
        order.status = new_status
        order.save()
        messages.success(request, f"Order #{order.pk} marked as {valid_statuses[new_status]}.")
    return redirect("dashboard_orders")
