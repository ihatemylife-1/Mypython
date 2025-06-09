import base64
import secrets
import requests

# Webhook URL
WEBHOOK_URL = "https://discord.com/api/webhooks/1380648110992130169/irhUpd0mk_XLreCuFmc-ZWDQwedg46rp3A97CvOtAwXHVAK54BCzC_JG93WqKlJIPGRO"

def generate_base64_key(length=16):
    """Generates a random base64 key."""
    return base64.b64encode(secrets.token_bytes(length)).decode()

def main():
    # Ask for user input
    original_text = input("Enter the text to encode in Base64: ")

    # Encode the user input in Base64
    encoded_text = base64.b64encode(original_text.encode()).decode()

    # Generate 3 base64 keys
    key1 = generate_base64_key()
    key2 = generate_base64_key()
    key3 = generate_base64_key()

    # Create a payload with nice formatting
    payload = {
        "embeds": [
            {
                "title": "🔐 Base64 Encoding Report",
                "color": 0x00ffcc,
                "fields": [
                    {"name": "🧩 Key 1", "value": f"`{key1}`", "inline": False},
                    {"name": "🧩 Key 2", "value": f"`{key2}`", "inline": False},
                    {"name": "🧩 Key 3", "value": f"`{key3}`", "inline": False},
                    {"name": "📦 Encoded String", "value": f"```{encoded_text}```", "inline": False},
                ],
                "footer": {"text": "Base64 Encoder by Python"}
            }
        ]
    }

    # Send to Discord webhook
    response = requests.post(WEBHOOK_URL, json=payload)

    if response.status_code == 204:
        print("✅ Successfully sent to the Discord webhook.")
    else:
        print(f"❌ Failed to send webhook. Status: {response.status_code}")
        print(response.text)

if __name__ == "__main__":
    main()