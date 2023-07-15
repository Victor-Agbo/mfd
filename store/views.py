from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError
from django.http import HttpResponseRedirect, HttpResponseForbidden
from django.urls import reverse
from django.contrib.auth.decorators import login_required
from django.conf import settings
import os
from django.contrib.auth.models import Group
from datetime import datetime
from . import models
import requests

# Create your views here.


@login_required
def add_category(request):
    # operators_group = Group.objects.get(name="Operator")

    # if not request.user.groups.filter(name=operators_group).exists():
    #     return HttpResponseForbidden("You don't have access to this page.")

    if request.method == "POST":
        category = request.POST.get("add_category", "")

        new_category = models.Category(name=category)
        new_category.save()
        return HttpResponseRedirect(reverse("operator"))

    else:
        return HttpResponseRedirect(reverse("operator"))


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
        request,
        "store/index.html",
        {
            "products": products,
            "categories": categories,
            "category_name": "All Items",
            "show_side": "show_side",
        },
    )


@login_required
def cart(request):
    user = models.User.objects.get(username=request.user)
    cart_items = user.cart.all()
    categories = models.Category.objects.all()
    return render(
        request,
        "store/cart.html",
        {"cart_items": cart_items, "show_side": "show_side", "categories": categories},
    )


def category(request, category_name):
    category_id = models.Category.objects.get(name=category_name).id
    products = models.Product.objects.filter(category=category_id)
    categories = models.Category.objects.all()
    return render(
        request,
        "store/index.html",
        {
            "products": products,
            "categories": categories,
            "category_name": category_name,
            "show_side": "show_side",
        },
    )


@login_required
def checkout(request):
    cart = models.User.objects.get(id=request.user.id).cart.all()
    print(cart)
    total = 0
    for item in cart:
        total += item.price
    print(total)
    # url = "https://api.flutterwave.com/v3/payments"
    # headers = {
    #     "Authorization": "Bearer FLWSECK_TEST-47dfe450627f49b6f6c22cb6fefd88aa-X"
    # }
    # json = {
    #     "tx_ref": generate_name(request.user, "pid"),
    #     "amount": str(product.price),
    #     "currency": "NGN",
    #     "redirect_url": "https://google.com",
    #     "meta": {"consumer_id": 23, "consumer_mac": "92a3-912ba-1192a"},
    #     "customer": {
    #         "email": request.user.email,
    #         "name": request.user,
    #     },
    #     "customizations": {
    #         "title": "Marvellous",
    #         "logo": "https://get.pxhere.com/photo/food-produce-egg-eggs-egg-yolk-animal-source-foods-989008.jpg",
    #     },
    # }
    # response = requests.post(url, json=json, headers=headers)
    # response_data = response.json()
    # print(response_data)
    # return HttpResponseRedirect(response_data["data"]["link"])


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
        # Check if authentication successful
        if user is not None:
            login(request, user)
            return HttpResponseRedirect(reverse("index"))
        else:
            return render(
                request,
                "store/login.html",
                {"message": "Invalid email and/or password."},
            )
    else:
        return render(request, "store/login.html")


@login_required
def logout_view(request):
    logout(request)
    return HttpResponseRedirect(reverse("index"))


@login_required
def order(request, product_id):
    #return HttpResponseRedirect(f"/product/{product_id}")
    product = models.Product.objects.get(id=product_id)

    url = "https://api.flutterwave.com/v3/payments"
    headers = {
        "Authorization": f"Bearer FLWSECK_TEST-47dfe450627f49b6f6c22cb6fefd88aa-X"
    }
    json = {
        "tx_ref": generate_name(request.user, "pid"),
        "amount": str(product.price),
        "currency": "NGN",
        "redirect_url": "https://google.com",
        "meta": {"consumer_id": 23, "consumer_mac": "92a3-912ba-1192a"},
        "customer": {
            "email": request.user.email,
            "name": request.user.username,
        },
        "customizations": {
            "title": "Marvellous",
            "logo": "",
        },
    }
    response = requests.post(url, json=json, headers=headers)
    response_data = response.json()
    print(response_data)
    if response_data["message"] == "sucess":
        return HttpResponseRedirect(response_data["data"]["link"])
    else:
        return HttpResponseRedirect(reverse(f"product/{product_id}"))

def generate_name(name, ext):
    now = datetime.now()
    print(now)
    return f"{name}-{now.year}_{now.month}_{now.day}-{now.hour}_{now.minute}_{now.second}.{ext}"


@login_required
def operator(request):
    # operators_group = Group.objects.get(name="Operator")

    # if not request.user.groups.filter(name=operators_group).exists():
    #     return HttpResponseForbidden("You don't have access to this page.")

    if request.method == "POST":
        category = request.POST.get("add_product_category", "")
        category = models.Category.objects.get(name=category)

        name = request.POST.get("add_product_name", "")
        description = request.POST.get("add_product_category", "")

        price = request.POST.get("add_product_price", "")
        img = request.FILES["add_product_img"]
        new_file_name = generate_name(request.user, img.name.split(".")[-1])
        file_path = os.path.join(settings.MEDIA_ROOT, "store/images", new_file_name)
        with open(file_path, "wb") as f:
            for chunk in img.chunks():
                f.write(chunk)
        # Handle successful upload
        print(new_file_name)
        print(img)

        new_product = models.Product(
            category=category,
            name=name,
            description=description,
            price=price,
            image=new_file_name,
        )
        new_product.save()
        return HttpResponseRedirect(reverse("operator"))

    else:
        products = models.Product.objects.all()
        categories = models.Category.objects.all()
        return render(
            request,
            "store/operator.html",
            {"categories": categories, "products": products, "show_side": "show_side"},
        )


@login_required
def op_category(request, category_name):
    category_id = models.Category.objects.get(name=category_name).id
    products = models.Product.objects.filter(category=category_id)
    categories = models.Category.objects.all()
    return render(
        request,
        "store/operator.html",
        {
            "products": products,
            "categories": categories,
            "category_name": category_name,
            "show_side": "show_side",
        },
    )


@login_required
def op_remove(request, product_id):
    to_remove = models.Product.objects.get(id=product_id)
    to_remove.delete()
    return HttpResponseRedirect(reverse("operator"))


@login_required
def product_view(request, product_id):
    categories = models.Category.objects.all()
    product = models.Product.objects.get(id=product_id)
    user = models.User.objects.get(username=request.user)

    if product in user.cart.all():
        add = "Remove From Cart"
    else:
        add = "Add to Cart"

    return render(
        request,
        "store/product.html",
        {
            "product": product,
            "add": add,
            "categories": categories,
            "show_side": "show_side",
        },
    )


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
        login(request, user)
        return HttpResponseRedirect(reverse("index"))
    else:
        return render(request, "store/register.html")
