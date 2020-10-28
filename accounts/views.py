from django.shortcuts import render
from django.http import HttpResponse
from accounts.models import *

# Create your views here.

def home(request):
    #return HttpResponse('Home')
    orders = Order.objects.all()
    customers = Customer.objects.all()
    context = {'orders':orders, 'customers':customers}
    return render(request, 'accounts/dashboard.html', context)

def products(request):
    #return HttpResponse('Products')
    products = Product.objects.all()
    return render(request, 'accounts/products.html', {'products': products})

def customers(request):
    #return HttpResponse('Customers')
    return render(request, 'accounts/customers.html')
