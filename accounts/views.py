from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.forms import inlineformset_factory
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
#from django.contrib.auth.forms import UserCreationForm

from accounts.models import *
from accounts.forms import OrderForm, CreateUserForm
from .filters import OrderFilter

# Create your views here.
#Register
def registerPage(request):
    form = CreateUserForm()

    if request.method == 'POST':
        form = CreateUserForm(request.POST)
        if form.is_valid():
            form.save()
            user = form.cleaned_data.get('username')
            messages.success(request, "Account was created for "+ user)
            return redirect('login')


    context = {'form':form}
    return  render(request, 'accounts/register.html', context)

#Login
def loginPage(request):
    context = {}
    return  render(request, 'accounts/login.html', context)

#Home
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

    myFilter = OrderFilter(request.GET, queryset=orders)
    orders = myFilter.qs

    context = {'customer':customer, 'orders':orders, 'total_orders':total_orders,
    'myFilter':myFilter}
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
