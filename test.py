import sys
import requests
import json
import os

# Base URLs of the Spring Boot application
BASE_URL_USER = "http://localhost:8080/api/users"
BASE_URL_CART = "http://localhost:8080/api/carts"
BASE_URL_ORDER = "http://localhost:8080/api/orders"
BASE_URL_PAYMENT = "http://localhost:8080/api/payments"
BASE_URL_FOOD = "http://localhost:8080/api/foods"

def create_food_items():
    food_items = [
        # Appetizers
        {"name": "Garlic Bread Sticks", "description": "Crispy on the outside, soft and garlicky inside.",
         "price": 3.99, "image": "url_to_garlic_bread_sticks_image", "quantity": 25, "category": "APPETIZER"},
        {"name": "Chicken Wings", "description": "Spicy and savory, served with blue cheese dressing.", "price": 5.49,
         "image": "url_to_chicken_wings_image", "quantity": 20, "category": "APPETIZER"},
        {"name": "Stuffed Mushrooms", "description": "Mushrooms filled with herbs and cream cheese.", "price": 4.59,
         "image": "url_to_stuffed_mushrooms_image", "quantity": 25, "category": "APPETIZER"},

        # Main Courses
        {"name": "Grilled Salmon", "description": "Grilled salmon with a lemon herb seasoning.", "price": 12.99,
         "image": "url_to_grilled_salmon_image", "quantity": 15, "category": "MAIN_COURSE"},
        {"name": "Beef Lasagna", "description": "Layers of pasta, seasoned beef, and cheese.", "price": 11.49,
         "image": "url_to_beef_lasagna_image", "quantity": 15, "category": "MAIN_COURSE"},
        {"name": "Vegetable Stir Fry", "description": "A mix of fresh vegetables sautéed with soy sauce.",
         "price": 9.99, "image": "url_to_vegetable_stir_fry_image", "quantity": 15, "category": "MAIN_COURSE"},

        # Desserts
        {"name": "Double Chocolate Muffin", "description": "Rich double chocolate delight, every bite full of chips.",
         "price": 2.69, "image": "url_to_double_chocolate_muffin_image", "quantity": 30, "category": "DESSERT"},
        {"name": "Choco Chip Muffin Deluxe", "description": "Deluxe version with extra chocolate chips.", "price": 2.79,
         "image": "url_to_choco_chip_muffin_deluxe_image", "quantity": 30, "category": "DESSERT"},
        {"name": "Mini Chocolate Muffin", "description": "Tiny treats, big chocolate chip flavors.", "price": 2.49,
         "image": "url_to_mini_chocolate_muffin_image", "quantity": 30, "category": "DESSERT"},

        # Drinks
        {"name": "Iced Lemon Tea", "description": "Refreshing lemon tea served chilled with a slice of lemon.",
         "price": 1.99, "image": "url_to_iced_lemon_tea_image", "quantity": 50, "category": "DRINK"},
        {"name": "Mango Smoothie", "description": "Fresh mangoes blended with ice and a hint of honey.", "price": 3.49,
         "image": "url_to_mango_smoothie_image", "quantity": 30, "category": "DRINK"},
        {"name": "Choco Chip Muffin Classic", "description": "Classic choco chip muffin, soft and delicious.",
         "price": 2.59, "image": "url_to_choco_chip_muffin_classic_image", "quantity": 30, "category": "DRINK"}
    ]

    for food_data in food_items:
        url = f"{BASE_URL_FOOD}/1"
        response = requests.post(url, json=food_data)
        if response.ok:
            print(f"Successfully created food item: {food_data['name']}")
        else:
            print(f"Failed to create food item {food_data['name']}")

create_food_items()