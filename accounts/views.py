from django.shortcuts import render
from django.http import HttpResponse
from accounts.models import *

# Create your views here.

def home(request):
    #return HttpResponse('Home')
    return render(request, 'accounts/dashboard.html')

def products(request):
    #return HttpResponse('Products')
    products = Product.objects.all()

    return render(request, 'accounts/products.html', {'products': products})

def customers(request):
    #return HttpResponse('Customers')
    return render(request, 'accounts/customers.html')
