from django.shortcuts import render


def index(request):
    """ Render the index page """
    return render(request, 'home/index.html')


def about(request):
    """ Render the about page """
    return render(request, 'home/about.html')
