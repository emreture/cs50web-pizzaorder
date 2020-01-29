from django.http import HttpResponse
from django.shortcuts import render
from .models import MenuItem, SubAddition, Topping
from .utils import menu_to_dict

# Create your views here.


def index(request):
    regular_pizzas = menu_to_dict(MenuItem.objects.filter(meal__meal_type__name="Regular Pizza").values("meal__name", "meal_size__name", "price"))
    sicilian_pizzas = menu_to_dict(MenuItem.objects.filter(meal__meal_type__name="Sicilian Pizza").values("meal__name", "meal_size__name", "price"))
    toppings = Topping.objects.values("name")
    subs = menu_to_dict(MenuItem.objects.filter(meal__meal_type__name="Sub").values("meal__name", "meal_size__name", "price"))
    sub_additions = SubAddition.objects.values("name", "price")
    pastas = MenuItem.objects.filter(meal__meal_type__name="Pasta").values("meal__name", "price")
    salads = MenuItem.objects.filter(meal__meal_type__name="Salad").values("meal__name", "price")
    dinner_platters = menu_to_dict(MenuItem.objects.filter(meal__meal_type__name="Dinner Platter").values("meal__name", "meal_size__name", "price"))

    context = {
        "regular_pizzas": regular_pizzas,
        "sicilian_pizzas": sicilian_pizzas,
        "toppings": toppings,
        "subs": subs,
        "sub_additions": sub_additions,
        "pastas": pastas,
        "salads": salads,
        "dinner_platters": dinner_platters,
    }
    return render(request, "orders/index.html", context)


def order(request):
    pass
