import json
from . models import *


def cookie_cart(request):
    try:
        cart = json.loads(request.COOKIES['cart'])
    except:
        cart = {}

    print('Cart:', cart)
    products = []
    order = {"total_cart_price": 0, "total_cart_products": 0, 'delivery': False}
    cart_products = order['total_cart_products']

    for i in cart:
        try:
            cart_products += cart[i]["quantity"]
            product = Product.objects.get(id=i)
            total = (product.price * cart[i]["quantity"])

            order['total_cart_price'] += total
            order['total_cart_products'] += cart[i]["quantity"]

            things = {
                'product': {
                    'id': product.id,
                    'name': product.name,
                    'price': product.price,
                    'thumbnail_url': product.thumbnail_url,
                },
                'quantity': cart[i]["quantity"],
                'cart_total': total
            }
            products.append(things)

            if product.digital == False:
                order['delivery'] = True

        except:
            pass

    return {'cart_products': cart_products, 'order': order, 'products': products}


def cart_user_data(request):
    if request.user.is_authenticated:
        customer = request.user.customer
        order, created = Order.objects.get_or_create(customer=customer, status=False)
        products = order.orderproduct_set.all()
        cart_products = order.total_cart_products
    else:
        cookie_data = cookie_cart(request)
        cart_products = cookie_data['cart_products']
        order = cookie_data['order']
        products = cookie_data['products']
    return {'cart_products': cart_products, 'order': order, 'products': products}


def guest_order(request, data):
    print("User is not logged in!")
    print('Cookies', request.COOKIES)

    firstname = data['form']['firstname']
    lastname = data['form']['lastname']
    email = data['form']['email']

    cookie_data = cart_user_data(request)
    things = cookie_data['products']

    customer, created = Customer.objects.get_or_create(
        email=email,
    )
    customer.first_name = firstname
    customer.last_name = lastname
    customer.save()

    order = Order.objects.create(
        customer=customer,
        status=False,
    )

    for thing in things:
        product = Product.objects.get(id=thing['product']['id'])

        order_product = OrderProduct.objects.create(
            product=product,
            order=order,
            quantity=thing['quantity']
        )
    return customer, order
