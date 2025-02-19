import requests

API_URL = "https://deine-codio-url/api/welcome"  # Passe die URL an!

def fetch_welcome_message():
    try:
        response = requests.get(API_URL)
        if response.status_code == 200:
            print("Server Response:", response.json())
        else:
            print(f"Error: {response.status_code} - {response.text}")
    except requests.exceptions.RequestException as e:
        print("Connection error:", e)

if __name__ == "__main__":
    fetch_welcome_message()
