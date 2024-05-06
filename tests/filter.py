import requests
import time

def get_items():
    url = "http://localhost:6543/items"
    start_time = time.time()

    response = requests.get(url)

    end_time = time.time()
    print(f"Time taken to retrieve items: {end_time - start_time} seconds")

    if response.status_code == 200:
        all_items = response.json()
        print("Retrieved items successfully.")
    else:
        all_items = []
        print("Failed to retrieve items. Status code:", response.status_code)

    return all_items

def filter_items():
    url = "http://localhost:6543/items/filter"
    payload = {
        "category": "CLOTHING",
        "condition": "NEW",
        "user_id": 3
    }
    start_time = time.time()
    response = requests.post(url, json=payload)

    end_time = time.time()  # End timing
    print(f"Time taken to filter items: {end_time - start_time} seconds")

    if response.status_code == 200:
        filtered_items = response.json()
        print("Filtered items successfully.")
    else:
        filtered_items = []
        print("Failed to filter items. Status code:", response.status_code)

    return filtered_items

if __name__ == '__main__':
    items = get_items()
    print(items)

    filtered_clothing_items = filter_items()
    print(filtered_clothing_items)
