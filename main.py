import telegram
import json


WEBINAR_TOKEN = "1b626d7421537440afcdea38b9e314f0"
TELEGRAM_TOKEN = "211900707:AAEHh24_XSCDFWIBonvEMW073H51yKjafFE"


if __name__ == "__main__":
    print("Starting the bot...")
    with open("users.json") as f:
        print("Loading users...")
        user_data = json.load(f)
    with open("last_date.txt") as f:
        print("Loading time data...")
        last_date = int(f.read().strip())
    print("Go!")
    telegram.start_bot(user_data, WEBINAR_TOKEN, last_date)
