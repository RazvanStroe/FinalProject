from django.contrib import admin

from RSbayStore.models import *

admin.site.register(Customer)
admin.site.register(Product)
admin.site.register(ProductTag)
admin.site.register(Order)
admin.site.register(OrderProduct)
admin.site.register(DeliveryAddress)
