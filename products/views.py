from django.shortcuts import render, get_object_or_404, redirect, reverse
from django.contrib import messages
from .models import Product, Category
from .forms import ProductForm
from django.contrib.auth.decorators import login_required

# Create your views here.


def all_products(request):
    """ Renders all products """
    products = Product.objects.all()
    categories = None

    # Category Filter
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
    """ Renders product information """
    product = get_object_or_404(Product, pk=product_id)

    context = {
        'product': product,
    }

    return render(request, 'products/product_info.html', context)


@login_required
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
                    request, 'Failed to add product, \
                    Please check the form is correct')
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


@login_required
def edit_product(request, product_id):
    """ Edit and existing product in the store """
    # Only accessible to superusers
    if request.user.is_superuser:
        product = get_object_or_404(Product, pk=product_id)
        if request.method == 'POST':
            form = ProductForm(request.POST, request.FILES, instance=product)
            if form.is_valid():
                form.save()
                messages.success(
                    request, f'{product.name} Updated Successfully')
                return redirect(reverse('product_info', args=[product.id]))
            else:
                messages.error(
                    request, 'Failed to update product, \
                         Please check the form is correct')
        else:
            form = ProductForm(instance=product)
            messages.info(request, f'You are editing {product.name}')

        context = {
            'form': form,
            'product': product,
        }

        return render(request, 'products/edit_product.html', context)
    else:
        messages.error(request, 'You must be admin to access this page')
        return render(request, 'home/index.html')


@login_required
def delete_product(request, product_id):
    """ Delete Product from the store """
    # Only accessible to superusers
    if request.user.is_superuser:
        product = get_object_or_404(Product, pk=product_id)
        product.delete()
        messages.success(request, f'{product.name} was deleted from the store')
        return redirect(reverse('products'))
    else:
        messages.error(request, 'You must be admin to delete a product')
        return render(request, 'home/index.html')
