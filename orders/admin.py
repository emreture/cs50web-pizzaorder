from django.contrib import admin

from .models import Meal, MenuItem, Topping, SubAddition
# Register your models here.


admin.site.register(Meal)
admin.site.register(Topping)
admin.site.register(SubAddition)


@admin.register(MenuItem)
class MenuItemAdmin(admin.ModelAdmin):
    list_display = ["meal", "meal_size", "toppings_count", "price"]
    list_filter = ["meal__meal_type", "meal_size", "price"]

    class Meta:
        model = MenuItem
