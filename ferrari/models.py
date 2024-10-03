import uuid
from django.contrib.auth.models import User
from django.db import models

# Create your models here.


class Ferrari_model(models.Model):
    car_model = models.CharField(max_length=64)
    model_desciption = models.CharField(max_length=300, default="Ferrari")
    car_cover = models.ImageField(upload_to="covers/")

    def __str__(self):
        return self.car_model


class Ferrari_car(models.Model):
    car_models = models.ForeignKey(
        Ferrari_model, on_delete=models.CASCADE, related_name="car_list"
    )
    model_name = models.CharField(max_length=50)
    description = models.CharField(max_length=500)
    backphoto = models.ImageField(upload_to="cars/")
    price = models.IntegerField()
    available = models.BooleanField(default=True)

    def __str__(self):
        return f"{self.car_models}, {self.model_name}"


class Shopping_Cart(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="buyer")
    cart = models.ForeignKey(Ferrari_car, on_delete=models.CASCADE)

    def __str__(self):
        return self.cart

    def total_price(self):
        total = 0
        for car in self.cart:
            price = self.cart.price
            total += price

        return total


class PasswordReset(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    reset_id = models.UUIDField(default=uuid.uuid4, unique=True, editable=False)
    created_when = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Password reset for {self.user.username} at {self.created_when}"
