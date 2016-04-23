from twx.botapi import TelegramBot
import time


def return_help():
    pass


API_TOKEN = "211900707:AAEHh24_XSCDFWIBonvEMW073H51yKjafFE"
COMMANDS = {
    "/register": register,
    "/help": return_help
}


bot = TelegramBot(API_TOKEN)


def get_command(message):
    message = message.split()
    if message[0].strip().startswith("/"):
        return message[0], message[1:]
    return None, None


def start_bot(user_data, last=0):
    last_date = last
    while True:
        updates = bot.get_updates().wait()
        for update in updates:
            if update.message.date > last_date:
                last_date = update.message.date
                uid = update.message.sender.id
                first_name = update.message.sender.first_name
                if first_name:
                    bot.send_message(uid, "Привет, дорогой {}".format(first_name))
                else:
                    bot.send_message(uid, "Привет, дорогой друг!")
                message_text = update.message.text
                command, command_args = get_command(message_text)
                print(command)
                if command:
                    bot.send_message(uid, "Вау, это же КОМАНДА")
                print(update)
                print(update.message.text)
                bot.send_message(uid, "Отсос")
                with open("last_date.txt", "w") as w:
                    w.write(str(last_date))
        time.sleep(5)
