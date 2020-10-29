from django.shortcuts import render
from django.http import HttpResponse
from accounts.models import *

# Create your views here.

def home(request):
    #return HttpResponse('Home')
    orders = Order.objects.all()
    customers = Customer.objects.all()
    total_orders = orders.count()
    delivered =  orders.filter(status='Delivered').count()
    pending =  orders.filter(status='Pending').count()

    context = { 'orders':orders, 'customers':customers,
                'total_orders':total_orders, 'delivered':delivered,
                'pending':pending}

    return render(request, 'accounts/dashboard.html', context)

def products(request):
    #return HttpResponse('Products')
    products = Product.objects.all()
    return render(request, 'accounts/products.html', {'products': products})

def customers(request, pk_test):
    #return HttpResponse('Customers')
    customer = Customer.objects.get(id=pk_test)
    orders = customer.order_set.all()
    total_orders = orders.count()

    context = {'customer':customer, 'orders':orders, 'total_orders':total_orders}
    return render(request, 'accounts/customers.html', context)
