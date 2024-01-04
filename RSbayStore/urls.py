from django.urls import path
from RSbayStore import views

urlpatterns = [
    path("", views.welcome_page, name="welcome-page"),
    path("products/", views.products_page, name="products"),
    path("cart/", views.cart_page, name="cart"),
    path("checkout/", views.checkout_page, name="checkout"),

    ## js
    path("update-product/", views.update_product, name="update-product"),
    path("process-order/", views.process_order, name="process-order"),

    # proba
    path("showusers/", views.show_all, name="show-people"),
    # proba

    path("signup/", views.user_signup, name="signup"),
    path("login/", views.user_login, name="login"),
    path("logout/", views.user_logout, name="logout"),

]