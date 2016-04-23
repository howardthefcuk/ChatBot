from twx.botapi import TelegramBot
import twx.botapi
import webinar
import time
import json
import datetime
from time import strptime
from time import mktime
from icalendar import Calendar, Event, vDatetime


API_TOKEN = "211900707:AAEHh24_XSCDFWIBonvEMW073H51yKjafFE"
webinar_token = "1b626d7421537440afcdea38b9e314f0"

def parse_time(timestr):
   timeformat = "%Y-%m-%dT%H:%M:%S%z"
   parsed = strptime(timestr, timeformat)
   return int(mktime(parsed))


def return_help(uid, userdata, args):
    help_text = """Привет! Я бот компании CompanyName на webinar.ru! Я расскажу тебе о наших вебинарах и помогу зарегистрироваться на интересующие тебя вебинары, а заодно и заранее напомню о времени, чтобы ты ничего не забыл. Чтобы воспользоваться моей помощью, введи команду из списка:
                /register почтовый_ящик: зарегистрироваться в системе
                /schedule: получить расписание вебинаров
                /joinevent номер_вебинара: зарегистрироваться на вебинар
                /joinsession номер_сессии: зарегистрироваться на конкретную сессию вебинара
                /help: помощь"""
    bot.send_message(uid, help_text)


def joinevent(uid, userdata, args):
    if 'email' not in userdata[uid]:
            bot.send_message(uid, "Извините, вы не зарегистрированы в системе.\n"
                "Для регистрации в системе напишите: /register ваш_email")
    elif args is None:
        bot.send_message("Для записи на событие используйте команду /join номер_события")
    else:
        w = webinar.webinarAPICalls(userdata[uid]['email'], webinar_token)
        regdata = w.webinarRegisterEvent(args[0])
        print(regdata)
        if 'link' in regdata:
            bot.send_message(uid, "Поздравляем, вы записались на вебинар!\n"
                                  "Ваша персональная ссылка: {}".format(regdata['link']))
        elif 'error' in regdata and regdata['error']['code'] == 409:
            bot.send_message(uid, "Вы уже записаны на этот вебинар.")
        else:
            bot.send_message(uid, "Произошла ошибка. Попробуйте позже.")


def joinsession(uid, userdata, args):
    if 'email' not in userdata[uid]:
            bot.send_message(uid, "Извините, вы не зарегистрированы в системе.\n"
                "Для регистрации в системе напишите: /register ваш_email")
    elif args is None:
        bot.send_message("Для записи на событие используйте команду /join номер_события")
    else:
        w = webinar.webinarAPICalls(userdata[uid]['email'], webinar_token)
        regdata = w.webinarRegisterEventSession(args[0])
        print(regdata)
        if 'link' in regdata:
            bot.send_message(uid, "Поздравляем, вы записались на сессию вебинара!\n"
                                  "Ваша персональная ссылка: {}".format(regdata['link']))
        elif 'error' in regdata and regdata['error']['code'] == 409:
            bot.send_message(uid, "Вы уже записаны на эту сессию.")
        else:
            bot.send_message(uid, "Произошла ошибка. Попробуйте позже.")


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
                print(event)
                name = event['name']
                event_id = event['id']
                sessions = list()
                for session in event['eventSessions']:
                    if session['status'] is not 'STOP':
                        starts_at = time.strftime("%D %H:%M", time.localtime(parse_time(session['startsAt'])))
                        sessions.append("Сессия #{}: {}\n"
                                        "Вступить: /joinsession_{}".format(session['id'], starts_at, session['id']))
                # lectors = ",".join(event['lectors'])
                description = event['description']
                message.append("Событие: {}\n"
                               "Вступить: /joinevent_{}\n"
                               "Сессии:\n{}\n"
                               "Описание:\n"
                               "{}".format(name, event_id, "\n".join(sessions), description))
        bot.send_message(uid, "\n\n".join(message))


def ical_export(uid, userdata, args):
    def data2iCal(name, start, description):
        cal = Calendar()
        cal['summary'] = name + ": " + description
        cal['dtstart'] = vDatetime(datetime.datetime.fromtimestamp(int(start)))
        return cal.to_ical().decode("utf-8")
    if args is not None:
        event_id = args[0]
        found = None
        for event in event_data:
            if event['id'] == event_id:
                found = event
                break
        if found is not None:
            print("DEBUG: Preparing ical")
            ical = data2iCal(found['name'], found['starts_at'], found['description'])
            bot.send_message(uid, ical)
            #bot.send_document()
            # with open('temp.ical', "w") as f:
            #     f.write(ical)
            # with open('temp.ical') as f:
            #     file_info = twx.botapi.InputFileInfo(found['name'] + ".ical", f, 'document')
            #     file = twx.botapi.InputFile(found['name'] + ".ical", file_info)
            #     bot.send_document(uid, f)


COMMANDS = {
    "/register": register,
    "/schedule": schedule,
    "/joinevent": joinevent,
    "/joinsession": joinsession,
    "/help": return_help,
    "/ical": ical_export,
}

bot = TelegramBot(API_TOKEN)


def update_events():
    global event_data
    event_data = list()
    email = "dummy@dummy.com"
    w = webinar.webinarAPICalls(email, webinar_token)
    timetable = w.webinarSchedule()
    for event in timetable:
        e = {
                "id": event['id'],
                "name": event['name'],
                "description": event['description'],
                "starts_at": parse_time(event['startsAt']),
                "type": "event"
        }
        print(e)
        event_data.append(e)
        for session in event['eventSessions']:
            e = {
                "id": session['id'],
                "name": session['name'],
                "description": session['description'],
                "starts_at": parse_time(session['startsAt']),
                "type": "session"
            }
            event_data.append(e)
    return event_data


def greet(uid):
    bot.send_message(uid, "Привет!")


def get_command(message):
    message = message.replace("_", " ").split()
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


def start_bot(user_data, last_update):
    event_update_counter = 0
    while True:
        if event_update_counter == 0:
            print("LOGGING: updating events")
            events = update_events()
            print("DEBUG: {}".format(events))
            with open("event_data.json", "w", encoding="utf-8") as f:
                json.dump(events, f)
            event_update_counter = 100000
        event_update_counter -= 1
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
