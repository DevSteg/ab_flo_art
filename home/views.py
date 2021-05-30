from django.shortcuts import render, redirect, reverse
from .forms import ContactForm
from django.conf import settings
from django.core.mail import send_mail
from django.contrib import messages


def index(request):
    """ Render the index page """
    return render(request, 'home/index.html')


def about(request):
    """ Render the about page """
    return render(request, 'home/about.html')


def contact(request):
    """ Render Contact Page and handle form """

    if request.method == 'POST':
        form = ContactForm(request.POST)
        if form.is_valid():
            subject = 'Website Enquiry'
            body = {
                'full_name': form.cleaned_data['full_name'],
                'email': form.cleaned_data['email_address'],
                'message': form.cleaned_data['message'],
            }
            email = '\n'.join(body.values())

            try:
                send_mail(subject, email, settings.DEFAULT_FROM_EMAIL, [
                          settings.DEFAULT_FROM_EMAIL])
                messages.success(
                    request, 'Your message has been sent, \
                             We will get back to you as soon as posisble')
            except Exception:
                messages.error(
                    request, 'Your message could not be sent please \
                              check the form is filled out correctly')

            return redirect(reverse('home'))

    form = ContactForm()

    context = {
        'form': form
    }
    return render(request, 'home/contact.html', context)
