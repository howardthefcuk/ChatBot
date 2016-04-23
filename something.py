from twx.botapi import TelegramBot
import time

API_TOKEN = "211900707:AAEHh24_XSCDFWIBonvEMW073H51yKjafFE"

bot = TelegramBot(API_TOKEN)

offset = 0
while True:
    updates = bot.get_updates().wait()
    new_updates = updates[offset:]
    for update in new_updates:
        uid = update.message.sender.id
        print(update.message.sender.id)
        print(update.message.text)
        bot.send_message(uid, "Отсос")
        offset = len(updates)
    time.sleep(5)