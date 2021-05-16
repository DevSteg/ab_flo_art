from django.shortcuts import render, redirect, reverse
from django.contrib import messages
from .forms import OrderForm

# Create your views here.


def checkout(request):
    """ View to render the shopping basket page """
    basket = request.session.get('basket', {})
    if not basket:
        messages.error(request, 'There are no items in your basket')
        return redirect(reverse('products'))

    order_form = OrderForm()
    context = {
        'order_form': order_form,
    }

    return render(request, 'checkout/checkout.html', context)
