from django.db import models
from django.contrib.auth.models import User

# Create your models here.


class MealSize(models.Model):
    name = models.CharField(max_length=16)

    def __str__(self):
        return f"{self.name}"


class MealType(models.Model):
    name = models.CharField(max_length=64)
    has_sub_additions = models.BooleanField()
    has_toppings = models.BooleanField()

    def __str__(self):
        return f"{self.name}"


class Meal(models.Model):
    name = models.CharField(max_length=64)
    meal_type = models.ForeignKey(MealType, on_delete=models.DO_NOTHING, related_name="types")

    def __str__(self):
        return f"{self.meal_type} - {self.name}"


class Topping(models.Model):
    name = models.CharField(max_length=64)

    def __str__(self):
        return f"{self.name}"


class SubAddition(models.Model):
    name = models.CharField(max_length=64)
    price = models.FloatField()

    def __str__(self):
        return f"{self.name}"


class MenuItem(models.Model):
    meal = models.ForeignKey(Meal, on_delete=models.DO_NOTHING, related_name="items")
    meal_size = models.ForeignKey(MealSize, on_delete=models.DO_NOTHING, related_name="sizes", blank=True, null=True)
    toppings_count = models.IntegerField(blank=True, null=True)
    price = models.FloatField()

    def __str__(self):
        if self.meal_size:
            return f"{self.meal} - {self.meal_size}"
        else:
            return f"{self.meal}"


class Cart(models.Model):
    user = models.ForeignKey(User, on_delete=models.DO_NOTHING, related_name="user")
    menu_item = models.ForeignKey(MenuItem, on_delete=models.DO_NOTHING, related_name="menu_item")
    toppings = models.ManyToManyField(Topping, blank=True, related_name="toppings")
    sub_additions = models.ManyToManyField(SubAddition, blank=True, related_name="sub_additions")
    price = models.FloatField()

    def __str__(self):
        toppings = list(self.toppings.all())
        sub_additions = list(self.sub_additions.all())
        return f"{self.user}, {self.menu_item}, {toppings}, {sub_additions}"


class Order(models.Model):
    user = models.ForeignKey(User, on_delete=models.DO_NOTHING, related_name="order_user")
    order_date = models.DateTimeField(auto_now_add=True)
    is_completed = models.BooleanField()

    def __str__(self):
        return f"{self.user}'s order on {self.order_date}. Completed: {self.is_completed}"


class OrderItem(models.Model):
    order = models.ForeignKey(Order, on_delete=models.DO_NOTHING, related_name="order")
    menu_item = models.ForeignKey(MenuItem, on_delete=models.DO_NOTHING, related_name="order_menu_item")
    toppings = models.ManyToManyField(Topping, blank=True, related_name="order_toppings")
    sub_additions = models.ManyToManyField(SubAddition, blank=True, related_name="order_sub_additions")

    def __str__(self):
        toppings = list(self.toppings.all())
        sub_additions = list(self.sub_additions.all())
        return f"{self.order}, {self.menu_item}, {toppings}, {sub_additions}"
