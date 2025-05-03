from django.shortcuts import render, redirect
from django.forms import inlineformset_factory
from django.http import HttpResponse
from django.contrib.auth.forms import UserCreationForm
from django.contrib import messages
from django.contrib.auth import authenticate, login as auth_login, logout as auth_logout
from django.contrib.auth.models import Group 
from django.contrib.auth.decorators import login_required
from .models import *
from .form import OrderForm, CreateUserForm
from .filter import orderFilter
from .decorator import unauthenticated_user, allowed_users, admin_only


@unauthenticated_user
def register(request):
    form = CreateUserForm()
    if request.method == "POST":
        form = CreateUserForm(request.POST)
        if form.is_valid():
            user = form.save()
            username = form.cleaned_data.get('username')

            group = Group.objects.get(name='customer')
            user.groups.add(group)
            messages.success(request, 'Account was created for '+ username)
            return redirect('home')

    context = {
        'form':form,
        }
    return render(request, 'accounts/auth/register.html', context)

@unauthenticated_user
def login(request):
    if request.method == "POST":
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)
        if user is not None:
            auth_login(request, user)
            return redirect('home')
        else:
            messages.info(request, 'Username or password incorrect')
    context = {}
    return render(request, 'accounts/auth/login.html', context)

def logout(request):
    auth_logout(request)
    return redirect('login') 

def user(request):
    return render(request, 'accounts/user.html')

@login_required(login_url='login')
@admin_only
def home(request):
    orders = Order.objects.all()
    customers = Customer.objects.all()
    total_order = Order.objects.count()
    total_customer = Customer.objects.count()
    order_delivered = Order.objects.filter(status='Delivered').count()
    order_pending = Order.objects.filter(status='Pending').count()
    context = {
        'orders': orders, 
        'customers': customers, 
        'total_order': total_order, 
        'total_customer': total_customer,
        'order_delivered': order_delivered, 
        'order_pending': order_pending
    }
    return render(request, 'accounts/dashboard.html', context )

@login_required(login_url='login')
def products(request):
    products = Product.objects.all()
    return render(request, "accounts/products.html", {'products':products})

@login_required(login_url='login')
def customer(request, pk_test):
    customers = Customer.objects.get(id=pk_test)
    orders = customers.order_set.all()
    total_order = Order.objects.count()
    filters = orderFilter(request.GET, queryset= orders)
    orders = filters.qs
    context = {
        'customers':customers,
        'orders': orders,
        'total_order':total_order,
        'filters':filters
    }
    return render( request, "accounts/customer.html", context)

@login_required(login_url='login')
def createOrder(request,pk):
    OrderFormSet = inlineformset_factory(Customer, Order, fields=('product', 'status'), extra=1)
    customer = Customer.objects.get(id=pk)
    formset = OrderFormSet(queryset = Order.objects.none(), instance= customer)
    # form = OrderForm(initial={'customer': customer})
    if request.method == "POST":
        formset = OrderFormSet(request.POST, instance= customer)
        # form = OrderForm(request.POST)
        if formset.is_valid():
            formset.save()
            return redirect('/')
    #     else:
    #         # Debugging: Print formset errors to console or log them
    #         print(formset.errors)
    # else:
    #     formset = OrderFormSet(instance=customer)
    context = {
        'formset':formset
    }
    return render(request, 'accounts/order-form.html', context)

@login_required(login_url='login')
@allowed_users(allowed_roles=['admin'])
def updateOrder(request, pk):

    order = Order.objects.get(id=pk)
    form = OrderForm(instance=order)
    if request.method == "POST":
        form = OrderForm(request.POST, instance=order)
        if form.is_valid():
            form.save()
            return redirect('/')
    context = {
            'form':form
        }
    return render(request, 'accounts/order-form.html', context)

@login_required(login_url='login')
@allowed_users(allowed_roles=['admin'])
def deleteOrder(request, pk):
    order = Order.objects.get(id=pk)
    if request.method == "POST":
        order.delete()
        return redirect('/')
    context = {
        'item':order
    }
    return render(request, 'accounts/order-form.html', context)



# Create your views here.
