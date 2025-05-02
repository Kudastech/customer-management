from django.shortcuts import render, redirect
from django.http import HttpResponse
from .models import *
from .form import OrderForm

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

def products(request):
    products = Product.objects.all()
    return render(request, "accounts/products.html", {'products':products})

def customer(request, pk_test):
    customers = Customer.objects.get(id=pk_test)
    orders = customers.order_set.all()
    total_order = Order.objects.count()
    context = {
        'customers':customers,
        'orders': orders,
        'total_order':total_order
    }
    return render( request, "accounts/customer.html", context)

def createOrder(request):

    form = OrderForm()
    if request.method == "POST":
        form = OrderForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('/')
    context = {
        'form':form
    }
    return render(request, 'accounts/order-form.html', context)

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

# Create your views here.
