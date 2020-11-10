from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.forms import inlineformset_factory
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import Group
#from django.contrib.auth.forms import UserCreationForm
from accounts.models import *
from accounts.forms import OrderForm, CreateUserForm
from .filters import OrderFilter
from .decorators import unauthenticated_user, allowed_users, admin_only


# Create your views here.
#Register View
@unauthenticated_user
def registerPage(request):
    form = CreateUserForm()
    if request.method == 'POST':
        form = CreateUserForm(request.POST)
        if form.is_valid():
            user = form.save()
            username = form.cleaned_data.get('username')

            group = Group.objects.get(name='customer')
            user.groups.add(group)

            messages.success(request, "Account was created for "+ username)
            return redirect('login')

    context = {'form':form}
    return  render(request, 'accounts/register.html', context)

#Login View
@unauthenticated_user
def loginPage(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)
            return redirect('home')
        else:
            messages.info(request, 'Username or Password is incorrect!')
    context = {}
    return  render(request, 'accounts/login.html', context)

#logout View
def logoutUser(request):
    logout(request)
    return redirect('login')

#Home View
@login_required(login_url='login')
@admin_only
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


#User View
def userPage(request):
    context = {}
    return render(request, 'accounts/user.html', context)

#Product View
@login_required(login_url='login')
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


#Customer View
@login_required(login_url='login')
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


#Update View
@login_required(login_url='login')
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


#Delete View
@login_required(login_url='login')
def deleteOrder(request, pk):
    order = Order.objects.get(id=pk)
    if request.method == 'POST':
        order.delete()
        return redirect('/')

    context = {'order':order}
    return render(request, 'accounts/delete.html', context)
