#### products_page ####
#
#         <div class="row">
#             <div class="col-sm">
#                 <h4>Products</h4>
#             </div>
#             <div class="card card-body">
# <!--                <div class="card card-body">-->
#                     <table class="table">
#                         <tr>
#                             <th>Thumbnails</th>
#                             <th>Product</th>
#                             <th>Category</th>
#                             <th>Price</th>
#                             <th>Details</th>
#                         </tr>
#                         {% for product in products %}
#                         <tr>
#                             <td>{{ product.thumbnail }}</td>
#                             <td>{{ product.name }}</td>
#                             <td>{{ product.category }}</td>
#                             <td>{{ product.price }}</td>
#                             <td>{{ product.description }}</td>
#                         </tr>
#                         {% endfor %}
#                     </table>
# <!--                </div>-->
#             </div>

#### products_page ####




### cart_page ###
# def cart_page(request):
#     if request.user.is_authenticated:
#         customer = request.user.customer
#         order, created = Order.objects.get_or_create(customer=customer, status=False)
#         products = order.orderproduct_set.all()
#         cart_products = order.total_cart_products
#     else:
#         products = []
#         order = {"total_cart_price": 0, "total_cart_products": 0, 'shipping':False}
#         if not request.user.is_authenticated:
#             messages.error(request, "You have to be logged in to view your cart!")
#
#             return redirect("login")
#     return render(request, template_name="RSbayStore/cart.html", context={"products": products, "order": order, "cart_products": cart_products})


### cart_page ###


### checkout_page ###
# def checkout_page(request):
#     if request.user.is_authenticated:
#         customer = request.user.customer
#         order, created = Order.objects.get_or_create(customer=customer, status=False)
#         products = order.orderproduct_set.all()
#         cart_products = order.total_cart_products
#     else:
#         cart_products = []
#         order = {'total_cart_price': 0, 'total_cart_products': 0, 'shipping': False}
#         if not request.user.is_authenticated:
#             messages.error(request, message="You have to be logged in to view your checkout!")
#             return redirect("login")
#     return render(request, template_name="RSbayStore/checkout.html", context={"products": products, "order": order, "cart_products": cart_products})
### checkout_page ###


### logo link ###
# <img src="{% static 'images/logo2.png' %}">
### logo link ###


### navbar bg-light css ###
# .bg-light{
# 	background-color: #1f517d!important;
# }
### navbar bg-light css ###


### headers css ##
# h1,h2,h3,h4,h5,h6{
# 	color:hsl(0, 0%, 30%);
# }
### headers css ##

# CATEGORIES = (
#     ('Mens clothing', 'Mens clothing'),
#     ('Womens clothing', 'Womens clothing'),
#     ('Kids clothing', 'Kids clothing'),
#     ('Computer', 'Computer'),
#     ('Notebooks', 'Notebooks'),
#     ('TVs', 'Tvs'),
#     ('Audio', 'Audio'),
#     ('Smartphones', 'Smartphones'),
#     ('Accessories', 'Accessories'),
#     ('Bicycles', 'Bicycles'),
#     ('Fitness', 'Fitness'),
# )