from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.forms import inlineformset_factory

from accounts.models import *
from accounts.forms import OrderForm

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

def createOrder(request, pk):
    #inlineformset_factory(Parent_Model, Child_Model)
    OrderFormSet = inlineformset_factory(Customer, Order, fields=('product', 'status'))
    customer = Customer.objects.get(id=pk)

    formset = OrderFormSet(queryset=Order.objects.none() ,instance=customer)
    #form = OrderForm(initial={'customer':customer})
    if request.method == 'POST':
        #print('Priting POST: ', request.POST)
        #form = OrderForm(request.POST)
        formset = OrderFormSet(request.POST, instance=customer)
        if formset.is_valid():
            formset.save()
            return redirect('/')

    context = {'formset':formset}
    return render(request, 'accounts/order_form.html', context)

def updateOrder(request, pk):

    order = Order.objects.get(id=pk)
    form = OrderForm(instance=order)

    if request.method == 'POST':
        #print('Priting POST: ', request.POST)
        form = OrderForm(request.POST, instance=order)
        if form.is_valid():
            form.save()
            return redirect('/')

    context = {'form':form}
    return render(request, 'accounts/order_form.html', context)

def deleteOrder(request, pk):
    order = Order.objects.get(id=pk)
    if request.method == 'POST':
        order.delete()
        return redirect('/')

    context = {'order':order}
    return render(request, 'accounts/delete.html', context)
