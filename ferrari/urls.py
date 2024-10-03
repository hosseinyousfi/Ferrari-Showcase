from django.urls import path
from . import views

app_name = "ferrari"
urlpatterns = [
    path("", views.index, name="index"),
    path("entry/login", views.login_view, name="login"),
    path("logout", views.logout_view, name="logout"),
    path("entry/register", views.register, name="register"),
    path("cars/<int:id>", views.cars, name="cars"),
    path("FAQ", views.faq, name="faq"),
    path("forgot-password/", views.ForgotPassword, name="forgot-password"),
    path(
        "password-reset-sent/<str:reset_id>/",
        views.PasswordResetSent,
        name="password-reset-sent",
    ),
    path("reset-password/<str:reset_id>/", views.ResetPassword, name="reset-password"),
    path("Cart/", views.shopping_cart, name="cart"),
    path("Cart/remove/<int:id>", views.remove_cart, name="remove"),
    path("cars/Cart/add/<int:id>", views.add_cart, name="add"),
    path("Cart/buy/<int:id>", views.buy, name="buy"),
]
