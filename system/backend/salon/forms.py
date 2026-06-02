from django import forms

from .models import Appointment, Feedback


class AppointmentForm(forms.ModelForm):
    class Meta:
        model = Appointment
        fields = ["service", "date", "time_slot"]
        widgets = {
            "date": forms.DateInput(attrs={"type": "date"}),
        }


class FeedbackForm(forms.ModelForm):
    class Meta:
        model = Feedback
        fields = ["name", "phone", "email", "message"]
        widgets = {
            "message": forms.Textarea(attrs={"rows": 5}),
        }
