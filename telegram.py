from twx.botapi import TelegramBot
import webinar
import time
import json
from datetime import datetime
from time import strptime
from time import mktime

API_TOKEN = "211900707:AAEHh24_XSCDFWIBonvEMW073H51yKjafFE"


def parse_time(timestr):
   timeformat = "%Y-%m-%dT%H:%M:%S%z"
   parsed = strptime(timestr, timeformat)
   return int(mktime(parsed))


def return_help(uid, userdata, args):
    help_text = """Привет! Я бот компании CompanyName на webinar.ru! Я расскажу тебе о наших вебинарах и помогу зарегистрироваться на интересующие тебя вебинары, а заодно и заранее напомню о времени, чтобы ты ничего не забыл. Чтобы воспользоваться моей помощью, введи команду из списка:
                /register название_семинара: зарегистрироваться на семинар
                /list: получить список доступных семинаров
                /help: получить помощь"""
    bot.send_message(uid, help_text)


def join(uid, userdata, args):
    bot.send_message(uid, "Здесь можно будет записаться")


def register(uid, userdata, args):
    if args is None:
        bot.send_message(uid, "Для регистрации в системе напишите: /register ваш_email")
    else:
        userdata[uid]['email'] = args[0]
        bot.send_message(uid, "Поздравляем, вы успешно зарегистрированы в системе!")
        print("DEBUG: email is: {}".format(args[0]))


def schedule(uid, userdata, args):
    if 'email' not in userdata[uid]:
        bot.send_message(uid, "Извините, вы не зарегистрированы в системе.\n"
                              "Для регистрации в системе напишите: /register ваш_email")
    else:
        w = webinar.webinarAPICalls(userdata[uid]['email'], webinar_token)
        timetable = w.webinarSchedule()
        message = list()
        for event in timetable:
            if event['status'] is not 'STOP':
                name = event['name']
                event_id = event['id']
                starts_at = time.strftime("%D %H:%M", time.localtime(parse_time(event['startsAt'])))
                # lectors = ",".join(event['lectors'])
                description = event['description']
                message.append("Событие: {}\n"
                               "Номер события: {}\n"
                               "Время начала: {}\n"
                               "Описание:\n"
                               "{}".format(name, event_id, starts_at, description))
        bot.send_message(uid, "\n\n".join(message))



def ical_export(uid, userdata, args):
    pass


COMMANDS = {
    "/register": register,
    "/schedule": schedule,
    "/join": join,
    "/help": return_help,
    "/export": ical_export,
}

bot = TelegramBot(API_TOKEN)


def greet(uid):
    bot.send_message(uid, "Привет!")


def get_command(message):
    message = message.split()
    args = None
    command = None
    if message[0].strip().startswith("/"):
        command = message[0]
        if len(message) > 1:
            args = message[1:]
    return command, args


def parse_command(uid, userdata, command, args):
    if command in COMMANDS:
        COMMANDS[command](uid, userdata, args)


def start_bot(user_data, token, last_update):
    global webinar_token
    webinar_token = token

    while True:
        updates = bot.get_updates(offset=-20).wait()
        if updates:
            for update in updates:
                if update.update_id > last_update:
                    last_update = update.update_id
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
                        parse_command(uid, user_data, command, command_args)
                    print("DEBUG: ", end="")
                    print(update)
                    bot.send_message(uid, "Ты - солнышко, лучший человек на свете, тебе всегда будет везти во всем, какой же ты охуенный БОГ ТЫ МОЙ ПРОСТО ОХУИТЕЛЬНЫЙ")
                    with open("last_date.txt", "w") as w:
                        w.write(str(last_update))
                    with open("users.json", "w") as f:
                        print(user_data)
                        json.dump(user_data, f)
        time.sleep(5)
