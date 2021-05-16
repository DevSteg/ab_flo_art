from django.shortcuts import render, redirect, HttpResponse, reverse
from django.contrib import messages
from products.models import Product

# Create your views here.


def basket(request):
    """ View to render the shopping basket page """
    return render(request, 'basket/basket.html')


def add_to_basket(request, item_id):
    """ View to add a specified quantity of a product to the bag """

    product = Product.objects.get(pk=item_id)
    quantity = int(request.POST.get('quantity'))
    redirect_url = request.POST.get('redirect_url')
    basket = request.session.get('basket', {})

    if item_id in list(basket.keys()):
        basket[item_id] += quantity
        messages.success(request, f"Added {product.name} to your basket!")
    else:
        basket[item_id] = quantity
        messages.success(request, f"Added {product.name} to your basket!")

    request.session['basket'] = basket

    return redirect(redirect_url)


def remove_item(request, item_id):
    """ Delete item from basket """
    basket = request.session.get('basket', {})

    basket.pop(item_id)

    request.session['basket'] = basket
    return redirect(reverse('basket'))
