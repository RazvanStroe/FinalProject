from django.urls import path
from RSbayStore import views
from django.contrib.auth import views as auth_views
from RSbayStore.views import search_view

urlpatterns = [
    # store related pages
    path("", views.welcome_page, name="welcome-page"),
    path("products/", views.products_page, name="products"),
    path("product/<int:pk>", views.product_view, name="product_view"),
    path("cart/", views.cart_page, name="cart"),
    path("checkout/", views.checkout_page, name="checkout"),

    # js
    path("update-product/", views.update_product, name="update-product"),
    path("process-order/", views.process_order, name="process-order"),

    # account related pages
    path("signup/", views.user_signup, name="signup"),
    path("login/", views.user_login, name="login"),
    path("logout/", views.user_logout, name="logout"),
    path("account/", views.edit_account, name="account-details"),

    # password change/reset
    path("reset_password/",
         auth_views.PasswordResetView.as_view(template_name="RSbayStore/password_reset.html"),
         name="reset_password"),
    path("reset_password_sent/",
         auth_views.PasswordResetDoneView.as_view(template_name="RSbayStore/password_reset_sent.html"),
         name="password_reset_done"),

    path("reset/<uidb64>/<token>/",
         auth_views.PasswordResetConfirmView.as_view(template_name="RSbayStore/password_reset_form.html"),
         name="password_reset_confirm"),

    path("reset_password_complete/",
         auth_views.PasswordResetCompleteView.as_view(template_name="RSbayStore/password_reset_done.html"),
         name="password_reset_complete"),

    # search
    path("search/", search_view, name='search'),

    # create a new product (admin)
    path("create-product/", views.create_product_view, name="create-product"),

    # delete a product (admin)
    path('delete-product/<int:product_id>/', views.delete_product, name='delete-product'),

    # users orders overview
    path("order-overview/", views.order_overview, name="order-overview"),

    # contact
    path("contact-page/", views.contact_page, name="contact-page"),

]