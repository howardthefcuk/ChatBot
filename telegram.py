from twx.botapi import TelegramBot
import time
import json


API_TOKEN = "211900707:AAEHh24_XSCDFWIBonvEMW073H51yKjafFE"


def return_help(uid, userdata, args):
    help_text = """Привет! Я бот компании CompanyName на webinar.ru! Я расскажу тебе о наших вебинарах и помогу зарегистрироваться на интересующие тебя вебинары, а заодно и заранее напомню о времени, чтобы ты ничего не забыл. Чтобы воспользоваться моей помощью, введи команду из списка:
                /register название_семинара: зарегистрироваться на семинар
                /list: получить список доступных семинаров
                /help: получить помощь"""
    bot.send_message(uid, help_text)


def join(uid, userdata, args):
    bot.send_message(uid, "Здесь можно будет записаться")


def register(uid, userdata, args):
    bot.send_message(uid, "Тут будет регистрация на вебинары")


def schedule(uid, userdata, args):
    bot.send_message(uid, "Тут будет расписание вебинаров")


def ical_export(uid, userdata, args):
    pass


COMMANDS = {
    "/register": register,
    "/schedule": schedule,
    "/join": join,
    "/help": return_help,
    "/export": ical_export
}

bot = TelegramBot(API_TOKEN)


def greet(uid):
    bot.send_message(uid, "Привет!")


def get_command(message):
    message = message.split()
    if message[0].strip().startswith("/"):
        return message[0], message[1:]
    return None, None


def parse_command(uid, userdata, command, args):
    if command in COMMANDS:
        COMMANDS[command](uid, userdata, args)


def start_bot(user_data, last=0):
    last_date = last
    while True:
        updates = bot.get_updates().wait()
        if updates:
            for update in updates:
                if update.message.date > last_date:
                    last_date = update.message.date
                    uid = str(update.message.sender.id)
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
                    print("LOGGING: received a message: {}".format(message_text))
                    command, command_args = get_command(message_text)
                    if command:
                        print("LOGGING: parsing command {} from {}".format(command, uid))
                        parse_command(uid, command, command_args)
                    print("DEBUG: ", end="")
                    print(update)
                    bot.send_message(uid, "Отсос")
                    with open("last_date.txt", "w") as w:
                        w.write(str(last_date))
                    with open("users.json", "w") as f:
                        print(user_data)
                        json.dump(user_data, f)
        time.sleep(3)
