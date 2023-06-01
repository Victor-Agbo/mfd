from django.shortcuts import render, redirect
import json
from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError
from django.http import HttpResponseRedirect, JsonResponse, HttpResponse

from django.urls import reverse
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator
from . import models

# Create your views here.


def add_to_cart(request, product_id):
    to_add = models.Product.objects.get(id=product_id)
    user = models.User.objects.get(username=request.user)

    if to_add in user.cart.all():
        user.cart.remove(to_add)

    else:
        user.cart.add(to_add)

    user.save()
    return redirect(f"/product/{product_id}")


def index(request):
    products = models.Product.objects.all()
    categories = models.Category.objects.all()
    return render(
        request, "store/index.html", {"products": products, "categories": categories}
    )


@login_required
def cart(request):
    user = models.User.objects.get(username=request.user)
    cart_items = user.cart.all()
    return render(request, "store/cart.html", {"cart_items": cart_items})


def category(request, category_name):
    category_id = models.Category.objects.get(name=category_name).id
    products = models.Product.objects.filter(category=category_id)
    categories = models.Category.objects.all()
    return render(
        request, "store/index.html", {"products": products, "categories": categories}
    )


@login_required
def remove_from_cart(request, product_id):
    to_remove = models.Product.objects.get(id=product_id)
    user = models.User.objects.get(username=request.user)

    user.cart.remove(to_remove)

    user.save()
    return HttpResponseRedirect(reverse("cart"))


def login_view(request):
    if request.method == "POST":
        # Attempt to sign user in
        username = request.POST.get("email", "")
        password = request.POST.get("password", "")

        user = authenticate(request, username=username, password=password)
        print(user)
        # Check if authentication successful
        if user is not None:
            login(request, user)
            return HttpResponseRedirect(reverse("index"))
        else:
            return render(
                request,
                "store/login.html",
                {"message": "Invalid username and/or password."},
            )
    else:
        return render(request, "store/login.html")


@login_required
def logout_view(request):
    logout(request)
    return HttpResponseRedirect(reverse("index"))


@login_required
def order(request, product_id):
    pass


@login_required
def product_view(request, product_id):
    product = models.Product.objects.get(id=product_id)
    user = models.User.objects.get(username=request.user)

    if product in user.cart.all():
        add = "Remove From Cart"
    else:
        add = "Add to Cart"
    print(product)
    return render(request, "store/product.html", {"product": product, "add": add})


def register(request):
    if request.method == "POST":
        username = request.POST["username"]
        email = request.POST["email"]

        # Ensure password matches confirmation
        password = request.POST["password"]
        confirmation = request.POST["confirmation"]
        if password != confirmation:
            return render(
                request, "store/register.html", {"message": "Passwords must match."}
            )

        # Attempt to create new user
        try:
            user = models.User.objects.create_user(username, email, password)
            user.save()
        except IntegrityError:
            return render(
                request, "store/register.html", {"message": "Username already taken."}
            )
        login(request)
        return HttpResponseRedirect(reverse("index"))
    else:
        return render(request, "store/register.html")
