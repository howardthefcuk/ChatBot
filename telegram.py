from twx.botapi import TelegramBot
import time
import json

def return_help():
    pass


API_TOKEN = "211900707:AAEHh24_XSCDFWIBonvEMW073H51yKjafFE"



def return_help(uid, args):
    bot.send_message(uid, "Здесь будет помощь")


def webinar_list(uid, args):
    bot.send_message(uid, "Здесь будет список семинаров")


def register(uid, args):
    bot.send_message(uid, "Тут будет регистрация на вебинары")

COMMANDS = {
    "/register": register,
    "/help": return_help,
    "/list": webinar_list
}

bot = TelegramBot(API_TOKEN)


def greet(uid):
    bot.send_message(uid, "Привет!")


def get_command(message):
    message = message.split()
    if message[0].strip().startswith("/"):
        return message[0], message[1:]
    return None, None


def parse_command(uid, command, args):
    if command in COMMANDS:
        COMMANDS[command](uid, args)


def start_bot(user_data, last=0):
    last_date = last
    while True:
        updates = bot.get_updates().wait()
        for update in updates:
            if update.message.date > last_date:
                last_date = update.message.date
                uid = update.message.sender.id
                first_name = update.message.sender.first_name
                if str(uid) in user_data:
                    if "last_session" in user_data[uid]:
                        if time.time() - user_data[uid]["last_session"] > 10800:
                            greet(uid)
                else:
                    user_data[str(uid)] = dict()
                    greet(uid)
                user_data[uid]["last_session"] = update.message.date
                message_text = update.message.text
                command, command_args = get_command(message_text)
                print(command)
                if command:
                    parse_command(uid, command, command_args)
                print(update)
                print(update.message.text)
                bot.send_message(uid, "Отсос")
                with open("last_date.txt", "w") as w:
                    w.write(str(last_date))
                with open("users.json", "w") as f:
                    print(user_data)
                    json.dump(user_data, f)
        time.sleep(3)
