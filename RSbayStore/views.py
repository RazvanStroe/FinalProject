from django.shortcuts import render, redirect
from django.contrib import messages
from .forms import *
from .models import *
from django.contrib.auth.models import User
from django.contrib.auth import login, authenticate, logout
from django.http import JsonResponse
import json
import datetime
from . utils import cookie_cart, cart_user_data, guest_order


def welcome_page(request):
    data = cart_user_data(request)
    cart_products = data['cart_products']

    return render(request, template_name="index.html", context={"cart_products": cart_products})


################################### proba
def show_all(request):
    all_users = User.objects.all()
    users_context = {
        "users": all_users
    }
    return render(request, template_name="RSbayStore/showusers.html", context=users_context)
################################### proba


def products_page(request):
    products = Product.objects.all()
    data = cart_user_data(request)
    cart_products = data['cart_products']

    return render(request, template_name="RSbayStore/products_page.html", context={"products": products, "cart_products": cart_products})


def user_signup(request):
    form = SignUpForm()
    if request.method == "POST":
        form = SignUpForm(request.POST)
        if form.is_valid():
            user = form.save()
            username = form.cleaned_data.get('username')
            Customer.objects.create(user=user)

            messages.success(request, "Account was succesfully created!")
    return render(request, template_name="RSbayStore/signup.html", context={"form": form})


def user_login(request):
    if request.method == "GET":
        form = LogInForm()
        return render(request, template_name="RSbayStore/login.html", context={"form": form})
    elif request.method == "POST":
        form = LogInForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data["username"]
            password = form.cleaned_data["password"]
            user = authenticate(request, username=username, password=password)
            if user:
                login(request, user)
                messages.success(request, message="You have been succesfully logged in !")
                return redirect("welcome-page")
        messages.error(request, message="Failed to log in! Please check your username or password and try again!")
    return render(request, template_name="RSbayStore/login.html", context={"form": form})


def user_logout(request):
    logout(request)
    messages.success(request, message="Succesfully logged out!")
    return redirect("login")


def cart_page(request):
    data = cart_user_data(request)
    cart_products = data['cart_products']
    order = data['order']
    products = data['products']

    return render(request, template_name="RSbayStore/cart.html", context={"products": products, "order": order, "cart_products": cart_products})


def checkout_page(request):
    data = cart_user_data(request)
    cart_products = data['cart_products']
    order = data['order']
    products = data['products']

    return render(request, template_name="RSbayStore/checkout.html", context={"products": products, "order": order, "cart_products": cart_products})


def update_product(request):
    data = json.loads(request.body)
    product_id = data['product_id']
    action = data['action']
    print('Action:', action)
    print('product_id', product_id)

    customer = request.user.customer
    product = Product.objects.get(id=product_id)
    order, created = Order.objects.get_or_create(customer=customer, status=False)
    orderproduct, created = OrderProduct.objects.get_or_create(order=order, product=product)

    if action == 'add':
        orderproduct.quantity = (orderproduct.quantity + 1)
    elif action == 'remove':
        orderproduct.quantity = (orderproduct.quantity - 1)

    orderproduct.save()

    if orderproduct.quantity <= 0:
        orderproduct.delete()

    return JsonResponse('Added to cart', safe=False)


def process_order(request):
    transaction_id = datetime.datetime.now().timestamp()
    data = json.loads(request.body)

    if request.user.is_authenticated:
        customer = request.user.customer
        order, created = Order.objects.get_or_create(customer=customer, status=False)

    else:
        customer, order = guest_order(request, data)

    total = float(data['form']['total'])
    order.transaction_id = transaction_id

    if total == float(order.total_cart_price):
        order.status = True
    order.save()
    if order.delivery == True:
        DeliveryAddress.objects.create(
            customer=customer,
            order=order,
            address=data['delivery']['address'],
            city=data['delivery']['city'],
            country=data['delivery']['country'],
            postal_code=data['delivery']['postalcode']
        )
    return JsonResponse('Payment complete! Thank you for your order!', safe=False)
