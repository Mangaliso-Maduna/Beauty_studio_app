from django.contrib import admin
from .models import Service, Product, Appointment, Order, OrderItem


@admin.register(Service)
class ServiceAdmin(admin.ModelAdmin):
    list_display = ("name", "category", "price", "duration_minutes", "active")
    list_filter = ("category", "active")
    search_fields = ("name",)


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ("name", "price", "stock", "active")
    list_filter = ("active",)
    search_fields = ("name",)


@admin.register(Appointment)
class AppointmentAdmin(admin.ModelAdmin):
    list_display = ("client", "service", "date", "time", "status")
    list_filter = ("status", "date", "service")
    search_fields = ("client__username", "service__name")


class OrderItemInline(admin.TabularInline):
    model = OrderItem
    extra = 0


@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ("id", "client", "status", "created_at", "total")
    list_filter = ("status",)
    inlines = [OrderItemInline]
