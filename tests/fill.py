import requests
import itertools

def fill_it():
    url = "http://localhost:6543/items/add"
    user_id = 2  # Assuming user ID 2 is valid and exists in your database
    categories = ["ART", "MISC", "CLOTHING"]  # List of categories
    conditions = ["NEW", "USED", "OLD"]  # List of conditions

    # Create a product of categories and conditions to ensure equal distribution
    product = list(itertools.product(categories, conditions))
    num_items_per_combo = 100 // len(product)  # Determine how many items per category-condition combo

    count = 0
    for i in range(num_items_per_combo):
        for combo in product:
            category, condition = combo
            count += 1
            description = f"New t-shirt {count}"
            data = {
                "user_id": user_id,
                "description": description,
                "category": category,
                "condition": condition,
                "trade_status": "AVAILABLE"
            }
            response = requests.post(url, json=data)
            print(f"Added item response for {description} ({category}, {condition}):", response.text)

    if count < 100:
        # If there are fewer than 100 items due to division rounding, add the remaining items
        remaining = 100 - count
        for i in range(remaining):
            category, condition = product[i % len(product)]  # Cycle through combinations
            count += 1
            description = f"New t-shirt {count}"
            data = {
                "user_id": user_id,
                "description": description,
                "category": category,
                "condition": condition,
                "trade_status": "AVAILABLE"
            }
            response = requests.post(url, json=data)
            print(f"Added item response for {description} ({category}, {condition}):", response.text)

if __name__ == '__main__':
    fill_it()
