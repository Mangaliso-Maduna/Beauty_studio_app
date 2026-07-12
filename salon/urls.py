from django.urls import path
from . import views

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
]
