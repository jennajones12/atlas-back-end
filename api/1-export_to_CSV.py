#!/usr/bin/python3
"""Exports to-do list information for a given user ID to CSV format."""

import csv
import requests
import sys

if __name__ == "__main__":
    # Check if user ID is provided as a command-line argument
    if len(sys.argv) != 2:
        print("Usage: python3 script.py <user_id>")
        sys.exit(1)

    user_id = sys.argv[1]

    # Define the base URL for the JSON API
    base_url = "https://jsonplaceholder.typicode.com/"

    try:
        # Fetch user information from the API
        user_response = requests.get(f"{base_url}users/{user_id}")
        user_response.raise_for_status()
        user = user_response.json()
        username = user.get("username")

        # Fetch the to-do list items associated with the user ID
        todos_response = requests.get(
            f"{base_url}todos",
            params={"userId": user_id}
        )
        todos_response.raise_for_status()
        todos = todos_response.json()

        # Write to CSV file
        with open(f"{user_id}.csv", "w", newline="",
                  encoding="utf-8") as csvfile:
            csv_writer = csv.writer(csvfile)
            csv_writer.writerow(["User ID", "Username", "Completed", "Title"])

            for todo in todos:
                csv_writer.writerow(
                    [user_id, username, todo["completed"], todo["title"]])

        print(f"CSV file '{user_id}.csv' has been successfully created.")

    except requests.exceptions.RequestException as e:
        print(f"Error fetching data: {e}")
        sys.exit(1)

    except (KeyError, IndexError) as e:
        print(
            f"Error: {e}. Please check if the provided
            user ID '{user_id}' is valid.")
        sys.exit(1)
