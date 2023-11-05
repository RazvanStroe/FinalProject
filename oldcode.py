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
# if request.user.is_authenticated:
#     customer = request.user.customer
#     order, created = Order.objects.get_or_create(customer=customer, status=Order)
#     products = order.orderproduct_set.all
# else:
#     products = []

### cart_page ###


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