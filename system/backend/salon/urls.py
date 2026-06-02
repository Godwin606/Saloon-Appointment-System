from django.urls import path

from .views import (
    appointments_page,
    barber_login_page,
    book_appointment_page,
    customer_login_page,
    feedback_page,
    home,
    logout_page,
    update_appointment_status_page,
)


urlpatterns = [
    path("", home, name="home"),
    path("customer-login/", customer_login_page, name="customer_login"),
    path("barber-login/", barber_login_page, name="barber_login"),
    path("logout/", logout_page, name="logout_page"),
    path("appointments/", appointments_page, name="appointments_page"),
    path("book/", book_appointment_page, name="book_appointment"),
    path(
        "appointments/<int:appointment_id>/<str:new_status>/",
        update_appointment_status_page,
        name="update_appointment_status",
    ),
    path("feedback/", feedback_page, name="feedback_page"),
]
