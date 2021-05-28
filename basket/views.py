from django.shortcuts import render, redirect, reverse, get_object_or_404
from django.contrib import messages
from products.models import Product
from django.db.models import F

# Create your views here.


def basket(request):
    """ View to render the shopping basket page """
    return render(request, 'basket/basket.html')


def add_to_basket(request, item_id):
    """ View to add a specified quantity of a product to the bag """

    product = get_object_or_404(Product, pk=item_id)
    quantity = int(request.POST.get('quantity'))
    redirect_url = request.POST.get('redirect_url')
    basket = request.session.get('basket', {})

    if item_id in list(basket.keys()):
        basket[item_id] += quantity
        product.stock = F('stock') - quantity
        product.save()
        messages.success(
            request,
            f"Updated {product.name} quantity to {basket[item_id]} in basket!")
    else:
        basket[item_id] = quantity
        product.stock = F('stock') - quantity
        product.save()
        messages.success(request, f"Added {product.name} to your basket!")

    request.session['basket'] = basket

    return redirect(redirect_url)


def remove_item(request, item_id):
    """ Delete item from basket """

    product = get_object_or_404(Product, pk=item_id)
    basket = request.session.get('basket', {})

    if basket[item_id] > 1:
        basket[item_id] -= 1
        product.stock = F('stock') + 1
        product.save()
        messages.success(
            request,
            f"Updated {product.name} quantity to {basket[item_id]} in basket!")
    else:
        basket.pop(item_id)
        product.stock = F('stock') + 1
        product.save()
        messages.success(request, f"Removed {product.name} from your basket!")

    request.session['basket'] = basket
    return redirect(reverse('basket'))
