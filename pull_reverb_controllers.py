import requests
import os
from twilio.rest import Client

"""
For later use:
rx3 = "https://reverb.com/p/pioneer-xdj-rx3-2-channel-rekordbox-slash-serato-all-in-one-dj-system?sort=price%7Casc"
xz = "https://reverb.com/p/pioneer-xdj-xz-4-channel-rekordbox-slash-serato-all-in-one-dj-system?sort=price%7Casc"

rx3_blacklist = {}
xz_blacklist = {}
"""


def get_controllers():
    blacklist = {}
    headers = {"Authorization": os.getenv("REVERB_BEARER_TOKEN")}
    listings = requests.get("https://api.reverb.com/api/my/feed", headers=headers)

    controllers = []

    for item in listings.json()["listings"]:
        if (
            item["price"]["amount_cents"] / 100 <= 1500
            and str(item["id"]) not in blacklist
        ):
            controllers.append(item)

    return controllers


def format_message(controllers):
    message = ""
    for controller in controllers:
        # title = controller["model"]
        link = "https://reverb.com/item/" + str(controller["id"])
        price = controller["price"]["display"]

        message += f"\n{link} - {price}"

    if message:
        send_sms(message)


def send_sms(message):
    account_sid = os.getenv("TWILIO_ACCOUNT_SID")
    auth_token = os.getenv("TWILIO_AUTH_TOKEN")
    client = Client(account_sid, auth_token)

    # message = client.messages.create(
    #     from_="+18555429907", body=message, to="+14159396293"
    # )

    message = client.messages.create(
        from_="whatsapp:+14155238886",
        body=message,
        to="whatsapp:+14159396293",
    )


if __name__ == "__main__":
    controllers = get_controllers()
    format_message(controllers)
