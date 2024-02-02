import requests
import time

def check_application_status(url):
    try:
        response = requests.get(url)
        if response.status_code == 200:
            return "Application is up and running!"
        else:
            return f"Application is down. HTTP Status Code: {response.status_code}"
    except requests.ConnectionError:
        return "Unable to connect to the application. It may be down or unreachable."

if __name__ == "__main__":
    application_url = "https://theallenanand.com"  # Replace with the actual URL of your application
    check_interval_seconds = 60  # Adjust the interval based on your requirements

    while True:
        result = check_application_status(application_url)
        print(f"{time.strftime('%Y-%m-%d %H:%M:%S')} - {result}")

        time.sleep(check_interval_seconds)