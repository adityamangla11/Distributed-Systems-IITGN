import requests
import json
import time

CENTRAL_SERVER_URL = "http://localhost:8080/dispatch"

def test_operation(operation, text, expected_result):
    payload = {
        "operation": operation,
        "text": text
    }
    try:
        response = requests.post(CENTRAL_SERVER_URL, json=payload)
        if response.status_code == 200:
            result = response.json().get('result')
            print(f"Test Op {operation} ('{text}'): {'PASS' if result == expected_result else 'FAIL'} (Got: {result})")
            return result == expected_result
        else:
            print(f"Test Op {operation} ('{text}'): FAIL (Status: {response.status_code}, Error: {response.json().get('error')})")
            return False
    except Exception as e:
        print(f"Test Op {operation} ('{text}'): ERROR ({str(e)})")
        return False

def main():
    print("Waiting for services to be ready...")
    # Basic wait for central server
    max_retries = 5
    for i in range(max_retries):
        try:
            requests.get("http://localhost:8080")
            break
        except requests.exceptions.ConnectionError:
            if i == max_retries - 1:
                print("Error: Central Server not reachable. Make sure 'docker-compose up' is running.")
                return
            time.sleep(2)

    tests = [
        (1, "hello world", "HELLO WORLD"),
        (2, "HELLO WORLD", "hello world"),
        (3, "abcde", "edcba"),
        (4, "this is a test", 4)
    ]

    all_passed = True
    for op, text, expected in tests:
        if not test_operation(op, text, expected):
            all_passed = False

    if all_passed:
        print("\nAll verification tests PASSED!")
    else:
        print("\nSome verification tests FAILED.")

if __name__ == "__main__":
    main()
