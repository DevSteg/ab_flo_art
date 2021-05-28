from django.shortcuts import render, get_object_or_404, redirect, reverse
from .models import UserProfile
from django.contrib import messages
from .forms import ProfileForm
from checkout.models import Order

# Create your views here.


def profile(request):
    """ View to display the users profile"""
    user = request.user
    if user.is_authenticated:
        profile = get_object_or_404(UserProfile, user=user)

        if request.method == 'POST':
            form = ProfileForm(request.POST, instance=profile)
            if form.is_valid():
                form.save()
                messages.success(request, 'Your Profile has been updated')
            else:
                messages.success(
                    request, 'Update profile failed, Please check the form is correct')
        else:
            form = ProfileForm(instance=profile)
        orders = profile.orders.all()

        context = {
            'form': form,
            'orders': orders,
        }

        return render(request, 'profiles/profile.html', context)
    else:
        messages.error(request, 'Please login first!')
        return redirect(reverse('account_login'))


def order_history(request, order_number):
    order = get_object_or_404(Order, order_number=order_number)

    messages.info(request, (
        f'This is a past confirmation for order_number {order_number}.'
        'A confirmation email was sent on the order date'
    ))

    context = {
        'order': order,
        'from_profile': True,
    }

    return render(request, 'checkout/checkout_success.html', context)
