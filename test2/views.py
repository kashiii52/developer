from django.shortcuts import render, redirect
from django.forms import inlineformset_factory
from django.http import HttpResponse
from .models import *
from .forms import OrderForm, CreateUserForm, CustomerForm
from .filters import OrderFilter
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.decorators import login_required
from .decorators import unauthenticated_user, allowed_users, admin_only
from django.contrib.auth.models import Group

@unauthenticated_user
def registerPage(request):
    """
    Register a new user.
    """
    form = CreateUserForm()
    if request.method == 'POST':
        form = CreateUserForm(request.POST)
        if form.is_valid():
            user = form.save()
            username = form.cleaned_data.get('username')
            messages.success(request, 'Account was created for ' + username)
            return redirect('login')
    context = {'form': form}
    return render(request, 'test2/register.html', context)

@unauthenticated_user
def loginPage(request):
    """
    Log in a user.
    """
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('home')
        else:
            messages.info(request, 'Username or Password is incorrect')
    context = {}
    return render(request, 'test2/login.html', context)

def logoutUser(request):
    """
    Log out the current user.
    """
    logout(request)
    return redirect('login')


@login_required(login_url='login')
def home(request):
    """
    Display the dashboard with orders and customers information.
    """

    customers = Customer.objects.filter(user=request.user)
    orders = Order.objects.filter(customer__in=customers)

    total_orders = orders.count()
    delivered = orders.filter(status='Delivered').count()
    pending = orders.filter(status='Pending').count()
    outofdelivery = orders.filter(status='Out of delivery').count()

    context = {
        'orders': orders,
        'customers': customers,
        'total_orders': total_orders,
        'delivered': delivered,
        'pending': pending,
        'outofdelivery': outofdelivery,
    }
    return render(request, 'test2/dashboard.html', context)


@login_required(login_url='login')
def accountSettings(request):
    """
    Display and update the user profile of the logged-in user.
    """
    user = request.user
    form = CustomerForm(instance=user)
    context = {'form': form}
    return render(request, 'test2/account_settings.html', context)


@login_required(login_url='login')
def products(request):
    """
    Display a list of products.
    """
    products = Product.objects.all()
    context = {'products': products}
    return render(request, 'test2/products.html', context)

@login_required(login_url='login')
def createOrder(request, pk):
    """
    Create a new order for a specific customer.
    """
    # form = OrderForm()

    customers = Customer.objects.filter(user=request.user)
    form = OrderForm(request.POST or None, initial={'customers': customers})
    form.fields['customer'].queryset = customers
    
    products = Product.objects.all()
    if request.method == 'POST':
        # form = OrderForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('/')
        else:
            print(form.errors)

    context = {'form': form, 'products': products}
    return render(request, 'test2/order_form.html', context)

@login_required(login_url='login')
@allowed_users(allowed_roles=['admin'])
def updateOrder(request, pk):
    """
    Update an existing order.
    """
    order = Order.objects.get(id=pk)
    form = OrderForm(instance=order)
    if request.method == "POST":
        form = OrderForm(request.POST, instance=order)
        if form.is_valid():
            form.save()
            return redirect('/')
        else:
            print(form.errors)
    context = {'form': form}
    return render(request, 'test2/order_form.html', context)

@login_required(login_url='login')
@allowed_users(allowed_roles=['admin'])
def deleteOrder(request, pk):
    """
    Delete an order.
    """
    order = Order.objects.get(id=pk)
    if request.method == "POST":
        order.delete()
        return redirect('/')
    context = {'item': order}
    return render(request, 'test2/delete.html', context)

@login_required(login_url='login')
def deleteCustomer(request, pk):
    """
    Delete a customer and associated orders.
    """
    customer = Customer.objects.get(id=pk)
    orders = Order.objects.filter(customer=customer)
    if request.method == "POST":
        for order in orders:
            order.delete()
        customer.delete()
        return redirect('/')

    context = {'customer': customer}
    return render(request, 'test2/delete_customer.html', context)

@login_required(login_url='login')
def AddCustomer(request):
    """
    Add a new customer.
    """
    form = CustomerForm()
    if request.method == 'POST':
        form = CustomerForm(request.POST)
        if form.is_valid():
            customer = form.save(commit=False)
            customer.user = request.user
            customer.save()
            return redirect('/')

    context = {'form': form}
    return render(request, 'test2/add_customer.html', context)

@login_required(login_url='login')
def allOrders(request):
    """
    Display a list of all orders with filtering options.
    """
    customers = Customer.objects.filter(user=request.user)
    orders = Order.objects.filter(customer__in=customers)
    
    total_orders = orders.count()
    delivered = orders.filter(status='Delivered').count()
    pending = orders.filter(status='Pending').count()
    outofdelivery = orders.filter(status='Out of delivery').count()
    myFilter = OrderFilter(request.GET, queryset=orders)
    orders = myFilter.qs
    

    context = {
        'orders': orders,
        'total_orders': total_orders,
        'delivered': delivered,
        'pending': pending,
        'myFilter': myFilter,
        'outofdelivery': outofdelivery,
    }
    return render(request, 'test2/show_all_orders.html', context)
