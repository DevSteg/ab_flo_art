from django.shortcuts import render

# Create your views here.


def basket(request):
    """ View to render the shopping basket page """
    return render(request, 'basket/basket.html')
