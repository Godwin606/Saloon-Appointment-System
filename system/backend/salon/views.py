from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404, redirect, render

from .forms import AppointmentForm, FeedbackForm
from .models import Appointment


CONTACT_PHONE = "0785468022"


def _base_context(**extra):
    return {"contact_phone": CONTACT_PHONE, **extra}


def home(request):
    if request.user.is_authenticated:
        return redirect("appointments_page")

    return render(request, "salon/home.html", _base_context())


def customer_login_page(request):
    if request.method == "POST":
        username = request.POST.get("username", "")
        password = request.POST.get("password", "")
        user = authenticate(request, username=username, password=password)

        if user is None or user.is_staff:
            messages.error(request, "Invalid customer username or password.")
        else:
            login(request, user)
            return redirect("appointments_page")

    return render(request, "salon/customer_login.html", _base_context())


def barber_login_page(request):
    if request.method == "POST":
        username = request.POST.get("username", "")
        password = request.POST.get("password", "")
        user = authenticate(request, username=username, password=password)

        if user is None or not user.is_staff:
            messages.error(request, "Invalid barber username or password.")
        else:
            login(request, user)
            return redirect("appointments_page")

    return render(request, "salon/barber_login.html", _base_context())


def logout_page(request):
    logout(request)
    return redirect("home")


@login_required
def appointments_page(request):
    appointments = Appointment.objects.select_related("client", "service")
    if not request.user.is_staff:
        appointments = appointments.filter(client=request.user)

    return render(
        request,
        "salon/appointments.html",
        _base_context(appointments=appointments.order_by("date", "time_slot")),
    )


@login_required
def book_appointment_page(request):
    if request.user.is_staff:
        messages.error(request, "Barber accounts manage appointments but do not book customer appointments.")
        return redirect("appointments_page")

    if request.method == "POST":
        form = AppointmentForm(request.POST)
        if form.is_valid():
            appointment = form.save(commit=False)
            appointment.client = request.user
            appointment.client_name = request.user.get_full_name() or request.user.username
            appointment.client_email = request.user.email
            appointment.quoted_price = appointment.service.price
            try:
                appointment.save()
            except Exception:
                messages.error(request, "That date and time slot is already booked. Please choose another slot.")
            else:
                messages.success(request, "Your appointment has been booked.")
                return redirect("appointments_page")
    else:
        form = AppointmentForm()

    return render(request, "salon/book.html", _base_context(form=form))


@login_required
def update_appointment_status_page(request, appointment_id, new_status):
    if not request.user.is_staff:
        messages.error(request, "Only the barber account can update appointment statuses.")
        return redirect("appointments_page")

    valid_statuses = {choice[0] for choice in Appointment.Status.choices}
    if new_status not in valid_statuses:
        messages.error(request, "Invalid appointment status.")
        return redirect("appointments_page")

    appointment = get_object_or_404(Appointment, id=appointment_id)
    appointment.status = new_status
    appointment.save(update_fields=["status"])
    messages.success(request, f"{appointment.client_name}'s appointment is now {new_status}.")
    return redirect("appointments_page")


def feedback_page(request):
    initial = {}
    if request.user.is_authenticated:
        initial = {
            "name": request.user.get_full_name() or request.user.username,
            "email": request.user.email,
        }

    if request.method == "POST":
        form = FeedbackForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "Thank you for your feedback.")
            return redirect("feedback_page")
    else:
        form = FeedbackForm(initial=initial)

    return render(request, "salon/feedback.html", _base_context(form=form))
