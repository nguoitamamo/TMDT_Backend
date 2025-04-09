import os
from twilio.rest import Client
from dotenv import load_dotenv
from unicodedata import decimal

# Load thông tin từ .env
load_dotenv()

TWILIO_ACCOUNT_SID = os.getenv("TWILIO_ACCOUNT_SID")
TWILIO_AUTH_TOKEN = os.getenv("TWILIO_AUTH_TOKEN")
TWILIO_PHONE_NUMBER = os.getenv("TWILIO_PHONE_NUMBER")


def send_otp(phone_number):
    try:
        otp = str(100000 + (int.from_bytes(os.urandom(2), "big") % 900000))  # Tạo OTP 6 chữ số
        client = Client(TWILIO_ACCOUNT_SID, TWILIO_AUTH_TOKEN)

        message = client.messages.create(
            body=f"Mã OTP từ HNT của bạn là: {otp}",
            from_=TWILIO_PHONE_NUMBER,
            to=phone_number
        )

        return {"success": True, "otp": otp, "message_sid": message.sid}
    except Exception as e:
        return {"success": False, "error": str(e)}





from django.contrib.auth.models import  (
    AbstractUser, Permission, Group
)

#
if __name__ == '__main__':
    price = "2,000,000 VND".replace(' VND', '')
    price = float(price.replace(',', '')) / 1_000_000
    print(price)