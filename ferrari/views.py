from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError
from django.http import HttpResponseRedirect, JsonResponse
from django.shortcuts import render
from django.urls import reverse
from .models import *
from django.contrib.auth.decorators import login_required
from django.views.decorators.csrf import csrf_exempt
from django.conf import settings
from django.core.mail import EmailMessage
from django.utils import timezone


# Create your views here.


def index(request):
    models = Ferrari_model.objects.all()
    return render(request, "ferrari/index.html", {"models": models})


def login_view(request):
    if request.method == "POST":

        # Attempt to sign user in
        username = request.POST["username"]
        password = request.POST["password"]
        user = authenticate(request, username=username, password=password)
        user.backend = "django.contrib.auth.backends.ModelBackend"

        # Check if authentication successful
        if user is not None:
            user.backend = "django.contrib.auth.backends.ModelBackend"
            login(request, user)
            return HttpResponseRedirect(reverse("ferrari:index"))
        else:
            messages.error(request, "Invalid username and/or password.")
            return render(request, "ferrari/login.html")
    else:
        return render(request, "ferrari/login.html")


def logout_view(request):
    logout(request)
    return HttpResponseRedirect(reverse("ferrari:index"))


def register(request):
    if request.method == "POST":
        username = request.POST["username"]
        email = request.POST["email"]

        # Ensure password matches confirmation
        password = request.POST["password"]
        confirmation = request.POST["confirmation"]
        if password != confirmation:
            return render(
                request, "ferrari/login.html", {"message": "Passwords must match."}
            )

        # Attempt to create new user
        try:
            # Create a new user
            user = User.objects.create_user(
                username=username, password=password, email=email
            )
            user.backend = "django.contrib.auth.backends.ModelBackend"
            user.save()
        except IntegrityError:
            return render(
                request, "ferrari/login.html", {"message": "Username already taken."}
            )
        login(request, user)
        return HttpResponseRedirect(reverse("ferrari:index"))
    else:
        return render(request, "ferrari/login.html")


def ForgotPassword(request):
    if request.method == "POST":
        email = request.POST["email"]

        try:
            user = User.objects.get(email=email)

            new_password_reset = PasswordReset(user=user)
            new_password_reset.save()

            password_reset_url = reverse(
                "ferrari:reset-password",
                kwargs={"reset_id": new_password_reset.reset_id},
            )
            full_url = f"{request.scheme}://{request.get_host()}{password_reset_url}"
            email_body = f"Reset your password using this link below:\n\n\n{full_url}"

            # send email
            email_message = EmailMessage(
                "Reset your password",  # subject
                email_body,
                settings.EMAIL_HOST_USER,  # sender
                [email],  #  receiver
            )

            email_message.fail_silently = True
            email_message.send()

            return HttpResponseRedirect(
                reverse(
                    "ferrari:password-reset-sent",
                    kwargs={"reset_id": new_password_reset.reset_id},
                )
            )

        except User.DoesNotExist:
            messages.error(request, f"No user with email '{email}' found")
            return HttpResponseRedirect(reverse("ferrari:forgot-password"))

    return render(request, "ferrari/forgot_password.html")


def PasswordResetSent(request, reset_id):
    if PasswordReset.objects.filter(reset_id=reset_id).exists():
        return render(request, "ferrari/password_reset_sent.html")
    else:
        messages.error(request, "There is something wrong with your reset id!")
        return HttpResponseRedirect(reverse("ferrari:forgot-password"))


def ResetPassword(request, reset_id):

    try:
        password_reset_id = PasswordReset.objects.get(reset_id=reset_id)

    except PasswordReset.DoesNotExist:

        # redirect to forgot password page if code does not exist
        messages.error(request, "Invalid reset id")
        return HttpResponseRedirect(reverse("ferrari:forgot-password"))

    if request.method == "POST":
        password = request.POST["password"]
        confirmation = request.POST["confirmation"]

        error = False

        if password != confirmation:
            error = True
            messages.error(request, "Passwords do not match")

        expiration_time = password_reset_id.created_when + timezone.timedelta(
            minutes=10
        )

        if timezone.now() > expiration_time:
            error = True
            messages.error(request, "Reset link has expired")
            password_reset_id.delete()

        if not error:
            user = password_reset_id.user
            user.set_password(password)
            user.save()
            # delete reset id after use
            password_reset_id.delete()
            # redirect to login
            messages.success(request, "Proceed to login")
            return HttpResponseRedirect(reverse("ferrari:login"))

        else:
            # redirect back to password reset page and display errors
            return HttpResponseRedirect(
                reverse("ferrari:reset-password", kwargs={reset_id: reset_id})
            )

    return render(request, "ferrari/reset_password.html")


def cars(request, id):
    m = Ferrari_model.objects.get(id=id)
    name = m.car_model
    cars = Ferrari_car.objects.filter(car_models=m)

    return render(
        request,
        "ferrari/car.html",
        {
            "cars": cars,
            "name": name,
        },
    )


@login_required
def shopping_cart(request):
    client = User.objects.get(id=request.user.id)
    items = client.buyer.all()
    products = []
    for item in items:
        product = item.cart
        products.append(product)

    return render(request, "ferrari/cart.html", {"products": products})


@login_required
def buy(request, id):
    product = Ferrari_car.objects.get(id=id)
    return render(
        request,
        "ferrari/cart.html",
        {
            "car": product,
            "buy": True,
        },
    )


@csrf_exempt
@login_required
def add_cart(request, id):
    product = Ferrari_car.objects.get(id=id)
    car_model = product.car_models
    id_model = car_model.id
    if not Shopping_Cart.objects.filter(user=request.user, cart=product).exists():
        shop_cart = Shopping_Cart(user=request.user, cart=product)
        shop_cart.save()
        return JsonResponse(
            {"message": "Successfully added to your Shopping Cart!"}, status=201
        )
    else:
        return JsonResponse(
            {"error": "This is also exsits in your Shopping Cart!"}, status=201
        )


@login_required
def remove_cart(request, id):
    car = Ferrari_car.objects.get(id=id)
    product = Shopping_Cart.objects.filter(user=request.user, cart=car)
    product.delete()
    return HttpResponseRedirect(reverse("ferrari:cart"))


def faq(request):
    return render(request, "ferrari/faq.html")
