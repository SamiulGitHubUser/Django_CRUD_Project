from django.shortcuts import render
from django.http import HttpResponse

# Create your views here.

def home(request):
    #return HttpResponse('Home')
    return render(request, 'accounts/dashboard.html')

def products(request):
    #return HttpResponse('Products')
    return render(request, 'accounts/products.html')

def customers(request):
    #return HttpResponse('Customers')
    return render(request, 'accounts/customers.html')
