from django.db import models
from django.contrib.auth.models import User
from PIL import Image


class Customer(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='customer', null=True, blank=True)
    first_name = models.CharField(max_length=20, null=True)
    last_name = models.CharField(max_length=20, null=True)
    age = models.IntegerField(null=True)
    email = models.EmailField(null=True)
    avatar = models.ImageField(default='Avatar/defaultavatar.jpeg', upload_to="Avatar/", null=True, blank=True)
    city = models.CharField(max_length=30, null=True)
    address = models.CharField(max_length=50, null=True)
    joined_time = models.DateTimeField(auto_now_add=True, null=True)
    is_admin = models.BooleanField(default=False)

    def __str__(self):
        return str(self.user)

    # resize avatar function
    def save(self, *args, **kwargs):
        super().save()
        img = Image.open(self.avatar.path)
        if img.height > 100 or img.width > 100:
            new_img = (100, 100)
            img.thumbnail(new_img)
            img.save(self.avatar.path)


class ProductTag(models.Model):
    name = models.CharField(max_length=30, null=True)

    def __str__(self):
        return self.name


class Product(models.Model):
    CATEGORIES = (
        ('Mens clothing', 'Mens clothing'),
        ('Womens clothing', 'Womens clothing'),
        ('Kids clothing', 'Kids clothing'),
        ('Computer', 'Computer'),
        ('Notebooks', 'Notebooks'),
        ('TVs', 'Tvs'),
        ('Audio', 'Audio'),
        ('Smartphones', 'Smartphones'),
        ('Accessories', 'Accessories'),
        ('Bicycles', 'Bicycles'),
        ('Fitness', 'Fitness'),
    )
    name = models.CharField(max_length=150, null=True)
    price = models.FloatField(null=True)
    description = models.CharField(max_length=200, null=True, blank=True)
    digital = models.BooleanField(default=False, null=True, blank=False)
    thumbnail = models.ImageField(upload_to="Thumbnails/", null=True, blank=True)
    category = models.CharField(max_length=20, null=True, choices=CATEGORIES)
    tags = models.ManyToManyField(ProductTag)

    def __str__(self):
        return self.name

    @property   # permite accesul la url daca produsul nu are poza, in caz contrar = eroare
    def thumbnail_url(self):
        try:
            url = self.thumbnail.url
        except:
            url = ''
        return url


class Order(models.Model):
    OrderStatus = (
        ('Pending', 'Pending'),
        ('Being delivered', 'Being delivered'),
        ('Delivered', 'Delivered')
    )
    customer = models.ForeignKey(Customer, on_delete=models.SET_NULL, null=True, blank=True)
    date_created = models.DateTimeField(auto_now_add=True, null=True, blank=True)
    status = models.CharField(max_length=150, null=True, choices=OrderStatus, default='Pending')
    transaction_id = models.CharField(max_length=200, null=True)

    def __str__(self):
        return str(self.id)


    @property
    def delivery(self):
        delivery = False
        orderproducts = self.orderproduct_set.all()
        for p in orderproducts:
            if p.product.digital == False:
                delivery = True
        return delivery

    @property   # unsupported operand type(s) for +: 'int' and 'str'
    def total_cart_price(self):
        orderproducts = self.orderproduct_set.all()
        total_price = sum([product.total_products_price for product in orderproducts])
        return total_price

    @property   # unsupported operand type(s) for +: 'int' and 'method'
    def total_cart_products(self):
        orderproducts = self.orderproduct_set.all()
        total_price = sum([product.quantity for product in orderproducts])
        return total_price


class OrderProduct(models.Model):
    product = models.ForeignKey(Product, on_delete=models.SET_NULL, null=True, blank=True)
    order = models.ForeignKey(Order, on_delete=models.SET_NULL, null=True, blank=True)
    quantity = models.IntegerField(default=0, null=True, blank=True)
    date_added = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return str(self.product)

    @property  # fara decorator va calcula un int cu un string - modifica
    def total_products_price(self):
        total_price = self.product.price * self.quantity
        return total_price


class DeliveryAddress(models.Model):
    customer = models.ForeignKey(Customer, on_delete=models.SET_NULL, null=True, blank=True)
    order = models.ForeignKey(Order, on_delete=models.SET_NULL, null=True, blank=True)
    address = models.CharField(max_length=50, null=True)
    city = models.CharField(max_length=50, null=True)
    country = models.CharField(max_length=50, null=True)
    postal_code = models.CharField(max_length=50, null=True)
    date_added = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.address





