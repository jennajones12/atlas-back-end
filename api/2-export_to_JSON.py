#!/usr/bin/python3
"""
Exports to-do list information for a given employee ID to JSON format.
"""
import json
import sys
import requests

if __name__ == "__main__":
    if len(sys.argv) != 2 or not sys.argv[1].isdigit():
        print("Usage: python3 script.py <user_id>")
        sys.exit(1)

    user_id = sys.argv[1]
    base_url = "https://jsonplaceholder.typicode.com/"

    try:
        # Fetch user information from the API
        user_response = requests.get(f"{base_url}users/{user_id}")
        user_response.raise_for_status()
        user = user_response.json()
        username = user.get("username")

        # Fetch the to-do list items associated with the user ID
        todos_response = requests.get(
            f"{base_url}todos", params={
                "userId": user_id})
        todos_response.raise_for_status()
        todos = todos_response.json()

        # Construct JSON data structure
        json_data = {
            user_id: [{"task": todo["title"],
                       "completed": todo["completed"],
                       "username": username} for todo in todos]
        }

        # Write JSON data to file
        with open(f"{user_id}.json", "w", encoding="utf-8") as json_file:
            json.dump(json_data, json_file, indent=2)

        print(f"JSON file '{user_id}.json' has been successfully created.")

    except requests.exceptions.RequestException as e:
        print(f"Error fetching data: {e}")
        sys.exit(1)

    except (KeyError, IndexError) as e:
        print(
            f"Error: {e}. Please check if the provided user ID '{user_id}' is valid.")
        sys.exit(1)
