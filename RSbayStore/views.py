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
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger

def welcome_page(request):
    data = cart_user_data(request)
    cart_products = data['cart_products']

    return render(request, template_name="index.html", context={"cart_products": cart_products})


def products_page(request):
    # Fetch all products
    products = Product.objects.all()

    # retrieve cart data
    data = cart_user_data(request)
    cart_products = data['cart_products']

    # Fetch categories
    categories = Product.CATEGORIES

    # Filter products based on the selected category
    selected_category = request.GET.get('category')
    if selected_category:
        products = Product.objects.filter(category=selected_category)

    # Pagination
    page = request.GET.get('page', 1)
    paginator = Paginator(products, 6)

    try:
        products = paginator.page(page)
    except PageNotAnInteger:
        products = paginator.page(1)
    except EmptyPage:
        products = paginator.page(paginator.num_pages)
    return render(request, template_name="RSbayStore/products_page.html", context={
        "products": products,
        "cart_products": cart_products,
        "categories": categories,
        "selected_category": selected_category,
    })


def create_product_view(request):
    if request.method == 'POST':
        form = CreateProductForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect('products')
    else:
        form = CreateProductForm

    return render(request, template_name="RSbayStore/create_product.html", context={'form': form})

def product_view(request, pk):
    data = cart_user_data(request)
    cart_products = data['cart_products']
    product = Product.objects.get(id=pk)
    return render(request, template_name="RSbayStore/product_view.html", context={"product": product, "cart_products": cart_products})

def search_view(request):
    query = request.GET.get('q')

    if query:
        results = Product.objects.filter(name__icontains=query)
        if results.count() == 1:
            product = results.first()
            return redirect('product_view', pk=product.pk)
        page = request.GET.get('page', 1)
        paginator = Paginator(results, 6)
        try:
            results = paginator.page(page)
        except PageNotAnInteger:
            results = paginator.page(1)
        except EmptyPage:
            results = paginator.page(paginator.num_pages)
    else:
        results = []
    return render(request, template_name='RSbayStore/search_results.html', context={'results': results, 'query': query})


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

def edit_account(request):
    data = cart_user_data(request)
    cart_products = data['cart_products']
    if request.method == 'POST':
        user_form = UpdateUserForm(request.POST, instance=request.user)
        profile_form = UpdateProfileForm(request.POST, request.FILES, instance=request.user.customer)
        if user_form.is_valid() and profile_form.is_valid():
            user_form.save()
            profile_form.save()
            messages.success(request, "Your account has been succesfully updated!")
            return redirect("account-details")
    else:
        user_form = UpdateUserForm(instance=request.user)
        profile_form = UpdateProfileForm(instance=request.user.customer)
    return render(request, template_name="RSbayStore/edit_profile.html", context={'user_form': user_form, 'profile_form': profile_form, "cart_products": cart_products})

# change password from account settings



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
