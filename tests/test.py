import sys
import requests
import json
import os
import time

def create_user():
    start_time = time.time()
    url = "http://localhost:6543/users/add"
    user_data = {
        "email": "newuser@example.com",
        "username": "newuser",
        "password": "password"
    }
    response = requests.post(url, json=user_data)
    end_time = time.time()
    print("Create user response:", response.text)
    print(f"Time taken to create user: {end_time - start_time} seconds")

def add_item():
    start_time = time.time()
    url = "http://localhost:6543/items/add"
    item_data = {
        "user_id": 3,
        "description": "New pants",
        "category": "CLOTHING",
        "condition": "NEW",
        "trade_status": "AVAILABLE"
    }
    response = requests.post(url, json=item_data)
    end_time = time.time()
    print("Added item response:", response.text)
    print(f"Time taken to add item: {end_time - start_time} seconds")

def initiate_trade():
    start_time = time.time()
    url = "http://localhost:6543/trade/initiate"
    trade_data = {
        "requester_item_id": 103,
        "accepter_item_id": 1
    }
    response = requests.post(url, json=trade_data)
    end_time = time.time()
    print("Initiate trade response:", response.text)
    print(f"Time taken to initiate trade: {end_time - start_time} seconds")

def execute_trade():
    start_time = time.time()
    url = "http://localhost:6543/trade/execute"
    trade_data = {
        "requester_item_id": 103,
        "accepter_item_id": 1
    }
    response = requests.post(url, json=trade_data)
    end_time = time.time()
    print("Execute trade response:", response.text)
    print(f"Time taken to execute trade: {end_time - start_time} seconds")

def main():
    total_start_time = time.time()
    create_user()
    add_item()
    initiate_trade()
    execute_trade()
    total_end_time = time.time()
    print(f"Total time taken for workflow: {total_end_time - total_start_time} seconds")

if __name__ == '__main__':
    main()
