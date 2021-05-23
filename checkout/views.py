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
        'stripe_public_key': 'pk_test_51IsaNNDTPFyBfatlFYO2kI6MnoUNk2tCFuJ4uC7JjdB4C07Pj7n6kUyr3jm8iO7Xq7pRdliJ6pcVg7saadcH1srV00QIRb9eko',
        'client_secret': 'test_client_secret',
    }

    return render(request, 'checkout/checkout.html', context)
