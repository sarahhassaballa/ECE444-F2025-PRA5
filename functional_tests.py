import requests

# AWS Elastic Beanstalk endpoint
BASE_URL = "http://ece444pra5-env.eba-fx6kixxw.us-east-2.elasticbeanstalk.com/predict"

# Define test cases (2 fake, 2 real)
test_cases = {
    "fake_1": "Scientists claim the moon is made of cheese.",
    "fake_2": "Hurricane Melissa is destroying downtown Toronto.",
    "real_1": "French is the predominant language in France.",
    "real_2": "Mark Carney is the Prime Minister of Canada.",
}

print("=== FUNCTIONAL TEST RESULTS ===\n")

for name, text in test_cases.items():
    response = requests.post(BASE_URL, json={"message": text})
    print(f"--- {name} ---")
    print("Input:", text)
    print("Status Code:", response.status_code)
    try:
        print("Response JSON:", response.json())
    except Exception:
        print("Invalid JSON Response:", response.text)
    print()