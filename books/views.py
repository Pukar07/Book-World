from audioop import reverse
from email import message
from itertools import product
from multiprocessing import context
from django.shortcuts import redirect, render
from matplotlib.pyplot import get
from matplotlib.style import available
from numpy import prod, save
import requests
from sklearn.preprocessing import OrdinalEncoder
from .models import *
from django.http import HttpResponse, HttpResponseRedirect, JsonResponse
import json
from plyer import notification
import datetime
from django.views.decorators.csrf import csrf_exempt


# Create your views here.


# home page
from django.shortcuts import render
from .models import Product
from django.shortcuts import render
from django.utils import timezone
from .models import Product

def index_page(request):
    # Get the six most recently added books
    books = Product.objects.order_by('-sequence')[:6]

    context = {'books': books}
    return render(request, 'index.html', context)



def store(request):
    if request.user.is_authenticated:
        order, created = Order.objects.get_or_create(user= request.user.username,complete=False)
        items = order.orderitem_set.all()
        cartItems = order.get_cart_items
    else:
        items = []   
        # cartItems= order['get_cart_items']

    products = Product.objects.all()
    context = {'products':products,  'cartItems': cartItems}
    return render(request,'store.html',context)
 

def cart(request):

    if request.user.is_authenticated:
        order, created = Order.objects.get_or_create(user=request.user.username,complete=False)
        items = order.orderitem_set.all()
        cartItems = order.get_cart_items
    else:
        items = []
        # order = {'get_cart_total':0, 'get_cart_items':0}
    
    context = {'items': items, 'order':order,'cartItems': cartItems}
    return render(request, 'cart.html',context)

def checkout(request):
    context = {}
    if request.user.is_authenticated:
        order, created = Order.objects.get_or_create(user=request.user.username, complete=False)
        items = order.orderitem_set.all()
        cartItems = order.get_cart_items
        context = {'items': items, 'order': order, 'cartItems': cartItems}
    else:
        items = []
        cartItems = 0
        context = {'items': items, 'cartItems': cartItems}

    return render(request, 'checkout.html', context)




def prod_detail(request):
    return render(request, 'productdetails.html',context)


def prod_detail(request,id):
    if request.user.is_authenticated:
        order, created = Order.objects.get_or_create(user=request.user.username,complete=False)
        items = order.orderitem_set.all()
        cartItems = order.get_cart_items

    else:
        items = [] 
    

    product = Product.objects.get(id=id)
    return render(request,'productdetails.html',{'cartItems':cartItems,'data':product})

from django.contrib.auth.decorators import login_required

@login_required
def updateItem(request):
    data = json.loads(request.body)
    productId = data['productId']
    action = data['action']
    print('Action:',action)
    print('Product:',productId)

    
    Book_name = Product.objects.get( id=productId)
    order, created = Order.objects.get_or_create(user=request.user.username,complete=False)

    orderItem, created = OrderItem.objects.get_or_create(order=order, Book_name=Book_name)

    if action =='add':
        orderItem.quantity = (orderItem.quantity + 1)
        Book_name.quantity = (Book_name.quantity - 1)
        Book_name.save()
    

    elif action == 'remove':
        orderItem.quantity = (orderItem.quantity -1)
        Book_name.quantity = (Book_name.quantity + 1)
        Book_name.save()
    orderItem.save()

    if orderItem.quantity <=0:
        orderItem.delete()
    

    return JsonResponse('Item was added',safe=False)


def remove_from_cart(request, id):
    if request.method == 'POST':
        
        delb = OrderItem.objects.get(Book_name_id=id)
        delb.delete()
        return HttpResponseRedirect('/cart')

def remove_from_wishlist(request, id):
    if request.method == 'POST':
        delb = Wishlist.objects.get(user = request.user.username, product_id=id)
        delb.delete()
        return HttpResponseRedirect('/wishlist')
 
def ProcessOrder(request):
    transaction_id = datetime.datetime.now().timestamp()
    data = json.loads(request.body)
    
 
    if request.user.is_authenticated:
        order, created = Order.objects.get_or_create(user=request.user.username,complete=False)
        total = float(data['form']['total'])
        order.transaction_id = transaction_id

        if total == order.get_cart_total:
            order.complete = True
        order.save()

        # if total == order.get_cart_total:
        #     completedOrder.objects.create(
        #         user= request.user.username,
        #         order = order,
                
                
        #     )

        if order.shipping == False:
             ShippingAddress.objects.create(
                user = request.user.username,
                order = order,
                address = data['shipping']['address'],
                city = data['shipping']['city'],
                ward_no = data['shipping']['ward_no'],
                zip_code = data['shipping']['zip_code'],
                phone = data['shipping']['phone'],

            )


    return JsonResponse('payment submited',safe=False)


from django.http import JsonResponse
import requests
import json










def wishlist(request):
    if request.user.is_authenticated:
        order, created = Order.objects.get_or_create(user=request.user.username,complete=False)
        items = order.orderitem_set.all()
        cartItems = order.get_cart_items    
        wishlist= Wishlist.objects.filter(user=request.user)

    return render(request,'wishlist.html',{'wishlist':wishlist,'items': items, 'order':order, 'cartItems':cartItems})

def addtowishlist(request):
    if request.method == "POST":
        if request.user.is_authenticated:
            prod_id = int(request.POST.get('product_id'))
            
            product_check = Product.objects.get(id=prod_id)
            if(product_check):
                if(Wishlist.objects.filter(user=request.user, product_id= prod_id)):
                    return JsonResponse({'status':"Product already in wishlist"})
                else:
                    Wishlist.objects.create(user=request.user,product_id = prod_id)
                    return JsonResponse({'status':"product added to wishlist"})

            else:
                return JsonResponse({'status':"No such product found"})

        
        else:
            return JsonResponse({'status':"login to continue"})
    return redirect('/')

# def deletewishlistitem(request):
#     if request.method == "POST":
#         if request.user.is_authenticated:
#             prod_id = int(request.POST.get('product_id'))
#             if(Wishlist.objects.filter(user=request.user, product_id= prod_id)):
#                 wishlistitem = Wishlist.objects.get(product_id = prod_id)
#                 wishlistitem.delete()
#                 return JsonResponse({'status':"Product removed from wishlist"})
#             else:
#                 return JsonResponse({'status':"Product not found in wishlist"})

        
#         else:
#             return JsonResponse({'status':"login to contibue"})
#     return redirect('/')


def profile(request):
    if request.user.is_authenticated:
        order, created = Order.objects.get_or_create(user=request.user.username,complete=False)
        items = order.orderitem_set.all()
        cartItems = order.get_cart_items

    else:
        items = [] 
    
    return render(request,'profile.html',{'items':items,'cartItems':cartItems})


def about(request):
    if request.user.is_authenticated:
        order, created = Order.objects.get_or_create(user=request.user.username,complete=False)
        items = order.orderitem_set.all()
        cartItems = order.get_cart_items
        return  render(request,'about.html',{'order':order,'items':items,'cartItems':cartItems})

    else:
        items = [] 

    
    return render(request,'about.html')

from django.db.models import Q

@login_required(login_url='login')
def searchBar(request):
    order = None
    items = None

    if request.user.is_authenticated:
        order, created = Order.objects.get_or_create(user=request.user.username, complete=False)
        items = order.orderitem_set.all()

        query = request.GET.get('query', '')
        if query:
            # Search for products whose book names or author names contain the query parameter
            products = Product.objects.filter(
                Q(Book_name__icontains=query) | Q(Author__icontains=query)
            )
            
            return render(request, 'searchbar.html', {
                'query': query,
                'products': products,
               
                'items': items,
                'order': order,
            })
        else:
            print("No information to show")
    else:
        return redirect('login')
    
    return render(request, 'searchbar.html', {'items': items, 'order': order})
 
def trackorder(request):
    return render(request,'ordertracking.html')

from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from .models import Order
from .models import Order, OrderItem, ShippingAddress



@login_required
def orders(request):
    orders = Order.objects.filter(user=request.user.username).exclude(order_status='Order Canceled').order_by('-date_ordered')
    context = {'orders': orders}
    return render(request, 'orders.html', context)


@login_required
def delete_order(request, order_id):
    order = get_object_or_404(Order, id=order_id, user=request.user, order_status__in=['Order Received', 'Order Processing', 'On the way'])

    if request.method == 'POST':
        # Update the order status to canceled
        order.order_status = 'Order Canceled'
        order.complete = True
        order.save()
        
        # Delete order items associated with the order
        order_items = OrderItem.objects.filter(order=order)
        for order_item in order_items:
            order_item.delete()
        
        # Delete the shipping address associated with the order
        shipping_address = ShippingAddress.objects.get(order=order)
        shipping_address.delete()
        
        messages.success(request, 'Order canceled successfully.')
        return redirect('order')

    context = {'order': order}
    return render(request, 'order.html', context)


def khalti(request):
    return render(request,'khaltirequest.html')













