import telegram
import json



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
    telegram.start_bot(user_data, last_date)
