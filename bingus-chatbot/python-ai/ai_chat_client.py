import requests

API_URL = "http://localhost:5001/ai-chat"

def get_ai_response(user_message):
    payload = {"message": user_message}
    try:
        response = requests.post(API_URL, json=payload)
        response.raise_for_status()
        return response.text.strip()
    except requests.RequestException as e:
        return f"Error: {e}"

if __name__ == "__main__":
    user_message = input("Enter your message: ")
    ai_response = get_ai_response(user_message)
    print(f"AI Response: {ai_response}")