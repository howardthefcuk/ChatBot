from twx.botapi import TelegramBot
import time

API_TOKEN = "211900707:AAEHh24_XSCDFWIBonvEMW073H51yKjafFE"

bot = TelegramBot(API_TOKEN)


def start_bot(start_offset=0):
    offset = start_offset
    while True:
        updates = bot.get_updates().wait()
        new_updates = updates[offset:]
        for update in new_updates:
            uid = update.message.sender.id
            print(update.message.sender.id)
            print(update.message.text)
            bot.send_message(uid, "Отсос")
            offset = len(updates)
            with open("offset.txt", "w") as w:
                w.write(str(offset))
        time.sleep(5)


if __name__ == "__main__":
    with open("offset.txt") as f:
        offset = int(f.read().strip())
    start_bot(offset)