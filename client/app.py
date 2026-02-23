import requests
import sys
import os

CENTRAL_SERVER_URL = os.getenv('CENTRAL_SERVER_URL', 'http://localhost:8080/dispatch')

def get_menu_choice():
    print("\n--- Distributed Text Processor ---")
    print("1. Convert text to UPPERCASE")
    print("2. Convert text to lowercase")
    print("3. Reverse text")
    print("4. Count number of words")
    print("5. Exit")
    return input("Enter choice: ")

def main():
    while True:
        choice = get_menu_choice()

        if choice == '5':
            print("Exiting...")
            sys.exit()

        if choice not in ['1', '2', '3', '4']:
            print("Invalid choice. Please enter 1-5.")
            continue

        text_input = input("Enter text: ")

        if not text_input.strip():
            print("Error: Input text cannot be empty")
            continue

        payload = {
            "operation": int(choice),
            "text": text_input
        }

        try:
            response = requests.post(CENTRAL_SERVER_URL, json=payload)
            
            if response.status_code == 200:
                result = response.json().get('result')
                print(f"Result: {result}")
            else:
                error_msg = response.json().get('error', 'Unknown Error')
                print(f"Error: {error_msg}")

        except requests.exceptions.ConnectionError:
            print(f"Error: Could not connect to Central Server at {CENTRAL_SERVER_URL}. Is it running?")

if __name__ == "__main__":
    main()