from django import forms
from profiles.models import UserProfile


class ContactForm(forms.Form):
    """ Contact Form """

    full_name = forms.CharField(max_length=100)
    email_address = forms.EmailField(max_length=150)
    message = forms.CharField(widget=forms.Textarea, max_length=2000)
