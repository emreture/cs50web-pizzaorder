def menu_to_dict(items):
    d = dict()
    for i in items:
        meal_name = i['meal__name']
        if meal_name not in d:
            d[meal_name] = dict()
        size = i['meal_size__name']
        price = i['price']
        d[meal_name][size] = price
    return d
