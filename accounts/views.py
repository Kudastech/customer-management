from django.shortcuts import render
from django.http import HttpResponse
from .models import *

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

def product(request):
    products = Product.objects.all()
    return render(request, "accounts/products.html", {'products':products})

def customer(request):
    customers = Customer.objects.all()
    return render( request, "accounts/customer.html", {'customers' : customers})


# Create your views here.
