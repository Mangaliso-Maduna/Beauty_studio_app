from django.urls import path
from . import views, dashboard

urlpatterns = [
    path("", views.home, name="home"),
    path("services/", views.service_list, name="service_list"),
    path("products/", views.product_list, name="product_list"),
    path("signup/", views.signup, name="signup"),
    path("book/", views.book_appointment, name="book_appointment"),
    path("my-appointments/", views.my_appointments, name="my_appointments"),
    path("appointments/<int:pk>/cancel/", views.cancel_appointment, name="cancel_appointment"),
    path("products/<int:pk>/buy/", views.buy_product, name="buy_product"),
    path("my-orders/", views.my_orders, name="my_orders"),

    # --- Staff dashboard (superuser only) ---
    path("dashboard/", dashboard.dashboard_home, name="dashboard_home"),

    path("dashboard/services/", dashboard.service_manage_list, name="dashboard_services"),
    path("dashboard/services/new/", dashboard.service_create, name="dashboard_service_create"),
    path("dashboard/services/<int:pk>/edit/", dashboard.service_edit, name="dashboard_service_edit"),
    path("dashboard/services/<int:pk>/delete/", dashboard.service_delete, name="dashboard_service_delete"),

    path("dashboard/products/", dashboard.product_manage_list, name="dashboard_products"),
    path("dashboard/products/new/", dashboard.product_create, name="dashboard_product_create"),
    path("dashboard/products/<int:pk>/edit/", dashboard.product_edit, name="dashboard_product_edit"),
    path("dashboard/products/<int:pk>/delete/", dashboard.product_delete, name="dashboard_product_delete"),

    path("dashboard/appointments/", dashboard.appointment_manage_list, name="dashboard_appointments"),
    path(
        "dashboard/appointments/<int:pk>/status/<str:new_status>/",
        dashboard.appointment_update_status,
        name="dashboard_appointment_status",
    ),

    path("dashboard/orders/", dashboard.order_manage_list, name="dashboard_orders"),
    path(
        "dashboard/orders/<int:pk>/status/<str:new_status>/",
        dashboard.order_update_status,
        name="dashboard_order_status",
    ),
]
