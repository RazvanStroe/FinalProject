from django.shortcuts import render, redirect
from django.contrib import messages
from .forms import *
from .models import *
from django.contrib.auth.models import User
from django.contrib.auth import login, authenticate, logout
from django.http import JsonResponse
import json


def welcome_page(request):
    if request.user.is_authenticated:
        customer = request.user.customer
        order, created = Order.objects.get_or_create(customer=customer)
        cart_products = order.total_cart_products
    else:
        cart_products = []
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
    if request.user.is_authenticated:
        customer = request.user.customer
        order, created = Order.objects.get_or_create(customer=customer)
        cart_products = order.total_cart_products
    else:
        cart_products = []
        products = Product.objects.all()
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
    if request.user.is_authenticated:
        customer = request.user.customer
        order, created = Order.objects.get_or_create(customer=customer)
        products = order.orderproduct_set.all()
        cart_products = order.total_cart_products
    else:
        products = []
        order = {"total_cart_price": 0, "total_cart_products": 0}
        if not request.user.is_authenticated:
            messages.error(request, "You have to be logged in to view your cart!")

            return redirect("login")
    return render(request, template_name="RSbayStore/cart.html", context={"products": products, "order": order, "cart_products": cart_products})


def checkout_page(request):
    if request.user.is_authenticated:
        customer = request.user.customer
        order, created = Order.objects.get_or_create(customer=customer)
        products = order.orderproduct_set.all()
        cart_products = order.total_cart_products
    else:
        if not request.user.is_authenticated:
            messages.error(request, message="You have to be logged in to view your checkout!")
            return redirect("login")
    return render(request, template_name="RSbayStore/checkout.html", context={"products": products, "order": order, "cart_products": cart_products})


def update_product(request):
    data = json.loads(request.body)
    product_id = data['product_id']
    action = data['action']
    print('Action:', action)
    print('product_id', product_id)

    customer = request.user.customer
    product = Product.objects.get(id=product_id)
    order, created = Order.objects.get_or_create(customer=customer)
    orderproduct, created = OrderProduct.objects.get_or_create(order=order, product=product)

    if action == 'add':
        orderproduct.quantity = (orderproduct.quantity + 1)
    elif action == 'remove':
        orderproduct.quantity = (orderproduct.quantity - 1)
    orderproduct.save()
    if orderproduct.quantity <= 0:
        orderproduct.delete()

    return JsonResponse('Added to cart', safe=False)



