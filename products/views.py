from django.shortcuts import render, get_object_or_404, redirect, reverse
from django.contrib import messages
from .models import Product, Category
from .forms import ProductForm

# Create your views here.


def all_products(request):
    """ Renders all products """
    products = Product.objects.all()
    categories = None

    if request.GET:
        if 'category' in request.GET:
            categories = request.GET['category'].split(',')
            products = products.filter(category__name__in=categories)
            categories = Category.objects.filter(name__in=categories)

    context = {
        'products': products,
        'current_categories': categories,
    }

    return render(request, 'products/products.html', context)


def product_info(request, product_id):
    """ Renders product info """
    product = get_object_or_404(Product, pk=product_id)

    context = {
        'product': product,
    }

    return render(request, 'products/product_info.html', context)


def add_product(request):
    """ Add a product to the store """
    # Only accessible to superusers
    if request.user.is_superuser:
        if request.method == 'POST':
            form = ProductForm(request.POST, request.FILES)
            if form.is_valid():
                form.save()
                messages.success(request, 'New product added successfully!')
                return redirect(reverse('add_product'))
            else:
                messages.error(
                    request, 'Failed to add product, Please check the form is correct')
        else:
            form = ProductForm()

        form = ProductForm()

        context = {
            'form': form,
        }

        return render(request, 'products/add_product.html', context)
    else:
        messages.error(request, 'You must be admin to access this page')
        return render(request, 'home/index.html')
