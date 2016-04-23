import json
import requests


class webinarAPICalls:
    def __init__(self, email, token):
        self.email =  email
        self.token = token

    def webinarSchedule(self):
        r = requests.get("https://userapi.webinar.ru/v3/organization/events/schedule", headers={"x-auth-token":self.token})
        schedData =  json.loads(r.text.split("]{")[0][1:])
        return schedData

    def webinarRegisterEvent(self, eventId="40149"):
        r = requests.post("https://userapi.webinar.ru/v3/events/"+eventId+"/register", headers={"x-auth-token":self.token}, data ={ "email":self.email})
        regData = json.loads(r.text)
        self.contactId = regData["contactId"]
        return regData

    def webinarRegisterEventSession(self, eventSessionId="42626"):
        r = requests.post("https://userapi.webinar.ru/v3/eventsessions/"+eventSessionId+"/register", headers={"x-auth-token":self.token}, data ={ "email":self.email})
        regData = json.loads(r.text)
        self.contactId = regData["contactId"]
        return regData


w = webinarAPICalls("gg2@wp.ru","1b626d7421537440afcdea38b9e314f0")
print(w.webinarRegisterEventSession())
