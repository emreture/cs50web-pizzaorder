from django.db import models

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
        return f"{self.meal} - {self.meal_size}"

