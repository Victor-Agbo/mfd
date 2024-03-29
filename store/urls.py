from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("add_category", views.add_category, name="add_category"),
    path("about", views.about, name="about"),
    path("add_to_cart/<int:product_id>", views.add_to_cart, name="add_to_cart"),
    path("cart", views.cart, name="cart"),
    path("category/<str:category_name>", views.category, name="category"),
    path("checkout", views.checkout, name="checkout"),
    path("remove/<int:product_id>", views.remove_from_cart, name="remove"),
    path("login", views.login_view, name="login"),
    path("logout", views.logout_view, name="logout"),
    path("operator", views.operator, name="operator"),
    path("operator/<str:category_name>", views.op_category, name="op_category"),
    path("op_remove/<int:product_id>", views.op_remove, name="op_remove"),
    path("order/<int:product_id>", views.order, name="order"),
    path("product/<int:product_id>", views.product_view, name="product"),
    path("register", views.register, name="register"),
]
