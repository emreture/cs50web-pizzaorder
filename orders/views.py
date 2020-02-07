from django.http import HttpResponse, JsonResponse, HttpResponseNotFound
from django.views.decorators.http import require_POST
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from .models import MenuItem, SubAddition, Topping, Cart, Order, OrderItem
from django.db.models import Sum
from django.contrib.auth.models import User
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
        "dinner_platters": dinner_platters
    }
    if request.user.is_authenticated:
        context["cart_items_count"] = Cart.objects.filter(user=request.user).count()
    return render(request, "orders/index.html", context)


@login_required(login_url="users:login")
def order(request):
    regular_pizzas = MenuItem.objects.filter(meal__meal_type__name="Regular Pizza")
    sicilian_pizzas = MenuItem.objects.filter(meal__meal_type__name="Sicilian Pizza")
    toppings = Topping.objects.all()
    subs = MenuItem.objects.filter(meal__meal_type__name="Sub")
    sub_additions = SubAddition.objects.all()
    pastas = MenuItem.objects.filter(meal__meal_type__name="Pasta")
    salads = MenuItem.objects.filter(meal__meal_type__name="Salad")
    platters = MenuItem.objects.filter(meal__meal_type__name="Dinner Platter")

    context = {
        "regular_pizzas": regular_pizzas,
        "sicilian_pizzas": sicilian_pizzas,
        "toppings": toppings,
        "subs": subs,
        "sub_additions": sub_additions,
        "pastas": pastas,
        "salads": salads,
        "platters": platters,
        "cart_items_count": Cart.objects.filter(user=request.user).count()
    }
    return render(request, "orders/order.html", context)


@require_POST
def add_to_cart(request):
    form = request.POST
    user_id = request.user.id
    menu_item_id = form.get('menu_item_id', None)
    toppings = form.get('toppings_list', None)
    toppings_list = list()
    sub_additions = form.get('sub_additions_list', None)
    sub_additions_list = list()
    if user_id is None or menu_item_id is None:
        return JsonResponse({'success': False, 'message': 'No user or menu item.'}, status=400)
    try:
        user = User.objects.get(pk=user_id)
    except User.DoesNotExist:
        return JsonResponse({'success': False, 'message': "User doesn't exist."}, status=400)
    try:
        menu_item = MenuItem.objects.get(pk=menu_item_id)
    except MenuItem.DoesNotExist:
        return JsonResponse({'success': False, 'message': "Menu item doesn't exist."}, status=400)
    if toppings:
        toppings_list = toppings.split(",")
    if menu_item.toppings_count and menu_item.toppings_count != len(toppings_list):
        return JsonResponse({'success': False, 'message': 'Invalid toppings count.'}, status=400)
    if sub_additions:
        sub_additions_list = sub_additions.split(",")
    item = Cart()
    item.user = user
    item.menu_item = menu_item
    item.price = menu_item.price
    item.save()
    for i in toppings_list:
        topping = Topping.objects.get(pk=i)
        item.toppings.add(topping)
    for i in sub_additions_list:
        sub_addition = SubAddition.objects.get(pk=i)
        item.sub_additions.add(sub_addition)
        item.price += sub_addition.price
    item.save()
    cart_items_count = Cart.objects.filter(user=user).count()
    return JsonResponse({'success': True, 'message': 'Item added to cart.', 'cart_items_count': cart_items_count, 'item': str(menu_item)}, status=200)


@login_required(login_url="users:login")
def cart(request):
    form = request.POST
    if form:
        item_id = form.get('remove_item', None)
        if item_id:
            cart_item = Cart.objects.get(pk=item_id)
            cart_item.delete()

    context = {
        "cart_items_count": Cart.objects.filter(user=request.user).count(),
        "cart_items": Cart.objects.filter(user=request.user),
        "cart_cost": Cart.objects.filter(user=request.user).aggregate(Sum('price')),
        "remove_button": True
    }
    return render(request, "orders/cart.html", context)


@login_required(login_url="users:login")
def checkout(request):
    if request.method == "POST":
        cart_items = Cart.objects.filter(user=request.user)
        new_order = Order()
        new_order.user = request.user
        new_order.is_completed = False
        new_order.save()
        for cart_item in cart_items:
            order_item = OrderItem()
            order_item.order = new_order
            order_item.menu_item = cart_item.menu_item
            order_item.save()
            for topping in cart_item.toppings.all():
                order_item.toppings.add(topping)
            for sub_addition in cart_item.sub_additions.all():
                order_item.sub_additions.add(sub_addition)
            order_item.save()
            cart_item.delete()
        context = {
            "order_no": new_order.id
        }
        return render(request, "orders/order-receipt.html", context)
    context = {
        "cart_items_count": Cart.objects.filter(user=request.user).count(),
        "cart_items": Cart.objects.filter(user=request.user),
        "cart_cost": Cart.objects.filter(user=request.user).aggregate(Sum('price')),
        "remove_button": False
    }
    return render(request, "orders/checkout.html", context)


@login_required(login_url="users:login")
def orders(request, order_id=None):
    context = {
        "cart_items_count": Cart.objects.filter(user=request.user).count()
    }
    if order_id is None:
        if request.method == "POST":
            form = request.POST
            order_id = form.get("order_id")
            action = form.get("action")
            _filter = form.get("filter")
            try:
                _order = Order.objects.get(pk=order_id)
            except Order.DoesNotExist:
                return HttpResponseNotFound("<h1>Order not found!</h1>")
            context['filter_sel'] = _filter
            if action == "mark_as_completed":
                _order.is_completed = True
                _order.save()
            elif action == "mark_as_pending":
                _order.is_completed = False
                _order.save()
        if request.user.is_superuser:
            context['orders'] = Order.objects.all()
        else:
            context['orders'] = Order.objects.filter(user=request.user)
        return render(request, "orders/order-list.html", context)
    else:
        try:
            _order = Order.objects.get(pk=order_id)
        except Order.DoesNotExist:
            return HttpResponseNotFound("<h1>Order not found!</h1>")
        if request.user != _order.user and not request.user.is_superuser:
            return HttpResponseNotFound("<h1>Order not found!</h1>")
        if request.method == "POST":
            form = request.POST
            action = form.get("action")
            if action == "mark_as_completed":
                _order.is_completed = True
                _order.save()
            elif action == "mark_as_pending":
                _order.is_completed = False
                _order.save()
        context['order_items'] = OrderItem.objects.filter(order=_order)
        context['order'] = _order
        return render(request, "orders/order-detail.html", context)


@require_POST
def re_order(request):
    form = request.POST
    order_id = form.get("order_id")
    try:
        _order = Order.objects.get(pk=order_id)
    except Order.DoesNotExist:
        return HttpResponseNotFound("<h1>Order not found!</h1>")
    order_items = OrderItem.objects.filter(order=_order)
    cart_items = Cart.objects.filter(user=request.user)
    for item in cart_items:
        item.delete()
    for item in order_items:
        _cart = Cart()
        _cart.user = request.user
        _cart.menu_item = item.menu_item
        _cart.price = item.menu_item.price
        _cart.save()
        for topping in item.toppings.all():
            _cart.toppings.add(topping)
        for sub_addition in item.sub_additions.all():
            _cart.sub_additions.add(sub_addition)
            _cart.price += sub_addition.price
        _cart.save()

    # form = request.POST
    # order_id = form.get("order_id")
    # _order = Order.objects.get(pk=order_id)
    # order_items = OrderItem.objects.filter(order=_order)
    # new_order = Order()
    # new_order.user = request.user
    # new_order.is_completed = False
    # new_order.save()
    # for item in order_items:
    #     order_item = OrderItem()
    #     order_item.order = new_order
    #     order_item.menu_item = item.menu_item
    #     order_item.save()
    #     for topping in item.toppings.all():
    #         order_item.toppings.add(topping)
    #     for sub_addition in item.sub_additions.all():
    #         order_item.sub_additions.add(sub_addition)
    #     order_item.save()
    #     print(item, "->", order_item)
    # context = {
    #     "order_no": new_order.id
    # }
    # return render(request, "orders/order-receipt.html", context)

    # context = {
    #     "cart_items_count": Cart.objects.filter(user=request.user).count(),
    #     "cart_items": Cart.objects.filter(user=request.user),
    #     "cart_cost": Cart.objects.filter(user=request.user).aggregate(Sum('price')),
    #     "remove_button": False
    # }
    # return render(request, "orders/checkout.html", context)

    return redirect("orders:checkout")
