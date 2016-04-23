import telegram
import json

if __name__ == "__main__":
    with open("users.json") as f:
        user_data = json.load(f)
    with open("last_date.txt") as f:
        last_date = int(f.read().strip())
    telegram.start_bot(user_data, last_date)
