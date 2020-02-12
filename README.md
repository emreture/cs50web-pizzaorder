# Project 3

Web Programming with Python and JavaScript

## Web application for online pizza orders

In addition to the built in django applications, there are two more applications in this project. Users application is a simple front-end for django's auth application for users to register, log in and log out. Orders application provides both back-end for front-end to manage orders of users. Django's built-in admin application is used for site administration. Super users can alter meal menu using this built-in admin application.

## Models

The restaurant's menu consists of menu items which are modelled in MenuItem class. A menu item has 4 properties:

1. Meal
2. Meal size (small or large)
3. Max toppings count
4. Price

A meal can have a name and a type (regular pizza, sicilian pizza, sub, pasta, salad or dinner platter) and is modelled in Meal class. Meal types are modelled in MealType class.

Meal sizes are modelled in MealSize class.

Pizza toppings are modelled in Topping class and sub additions are modeled in SubAddition class. In addition to a name property, SubAddition class has a price property.

Site admins can add, remove and update meals, menu items, pizza toppings and sub additions using built in Django admin user interface. Meal type and meal size tables can be altered using Django's shell. These tables are not shown on the admin user interface because after adding items to these tables or removing items form these tables, the menu and the order pages and the code behind these pages must be updated.

A cart item has 5 properties and is modelled in Cart class.

1. User
2. Menu item
3. Toppings (if any)
4. Sub additions (if any)
5. Price

Every cart item is associated with a user and stored in the database. Thus the contents of the cart is remembered even if a user closes the window, or logs out and logs back in again.

Topping property has a many to many relation with Topping class and sub addition property has a many to many relation with SubAddition class.

When a user checks out a new order is created first. This order is modelled in Order class. An order object has user, order_date and is_completed properties.

Then every cart item is transformed to an order item which is modelled in OrderItem class. After the transformation the cart item is deleted so that the cart can be empty after the order.

### Special pizza
Special pizza is a pizza with five toppings which users can choose.

## Web pages
### Homepage (/)
This is the landing page of the website. A price list of the menu items are shown on this page.

### Log in (/u/login) and register (/u/register) pages
If a user is not authenticated, links for log in and register pages are shown on the navigation bar. These pages provide necessary forms for users to log in or register.

Users can register for the web application with a username, password, first name, last name, and email address. Then they can log in and log out of the website.

Duplicate usernames are not allowed. When a user tries to register with a username already exists, registration fails and the user is warned.

### Log out (/u/logout) page
When a user is authenticated, a log out link is shown on the navigation bar instead of log in and register links. When an authenticated user clicks on that link, he/she is logged out and redirected to the homepage.

### Order page (/order)
This is the page where menu items can be added to shopping cart. Users can see menu items along with optional selections and additions with their prices updated by their selection. For pizza items 'add to cart' button is disabled until proper number of toppings are selected. Adding items to user's cart is achieved via functions using AJAX and the user is informed with a modal message box shown about the status. The number shown next to the cart icon on the navigation bar is also updated when an item is added or removed.

### Viewing cart (/cart) and placing an order (/checkout)
User can view their carts by clicking on the cart icon shown on the navigation bar. On the cart page users can review their carts, remove any items or proceed to checkout.

If the cart is empty, "Your cart is empty" message is shown and checkout button is not displayed.

On the checkout page user information and cart items are shown for user to confirm his/her order. When user clicks on the 'confirm and pay' button, order is placed and the order confirmation is shown. On this page there's a link for user to track the status of order.

### Viewing orders (/orders and /orders/<int:order_id>)
Users can access to a list of their orders on this page. If user is a superuser he/she can see all of the orders placed by all users. On this page, order number, date of order and status of order is shown.

If user is a superuser he/she can see the users of orders and can mark orders as complete or pending on this page (which is my first personal touch).

Orders list can be filtered by order's status. Users can view only completed orders, only pending orders or all orders (which is my second touch).

Details of any order can be accessed by clicking on the order number. If the order is completed users can order same items by simply clicking 'order again' button (which is my third personal touch).

## My personal touches
As mentioned above I added three additional features:

1. Site administrators (superusers) can mark orders as completed or pending.
2. On the view orders page, orders list can be filtered by order's status.
3. Users can reorder their previous orders with a simple button click.
