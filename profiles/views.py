from django.shortcuts import render, get_object_or_404, redirect, reverse
from .models import UserProfile
from django.contrib import messages
from .forms import ProfileForm

# Create your views here.


def profile(request):
    """ View to display the users profile"""
    user = request.user
    if user.is_authenticated:
        profile = get_object_or_404(UserProfile, user=user)

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
