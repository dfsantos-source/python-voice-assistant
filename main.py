from __future__ import print_function
import datetime
import pickle
import os.path
from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
import os
import time
import speech_recognition as sr
import pyttsx3
import pytz
import random
from random import choice
#playsound gtts

SCOPES = ['https://www.googleapis.com/auth/calendar.readonly']
DAY_PRONOUNCE = [
    "first", "second", "third", "fourth", "fifth", "sixth", "seventh", "eighth", "nineth", "tenth", "eleventh", "twelveth", "thirtheenth", 
    "fourteenth", "fifteenth", "sixteenth", "seventeenth", "eighteenth", 
    "nineteenth", "twentyth", "twentyfirst", "twentysecond", "twentythird",
    "twentyfourth", "twentyfifth", "twentysixth", "twentyseventh", "twentyeigth", "twentynineth", "thirtyth", "thirtyfirst"
]
DAYS_OF_WEEK = [
    "monday", 
    "tuesday", 
    "wednesday", 
    "thursday", 
    "friday", 
    "saturday", 
    "sunday",
]
MONTHS = [
    "january", 
    "february", 
    "march", 
    "april", 
    "may", 
    "june",
    "july", 
    "august", 
    "september",
    "october", 
    "november", 
    "december"
]
GREETING_STRS_1 = [
    "hello",
    "hi",
    "hey",
    "what's up",
    "what is up",
    "what's good",
    "what is good",
]
GREETING_STRS_1_ANSWERS = [
    "hello",
    "hi",
    "hey",
    "what's up",
    "what is up",
    "what's good",
    "what is good",
]

GREETING_STRS_2 = [
    "how are you",
    "how are things",
]   
GREETING_STRS_2_ANSWERS = [
    "just getting by",
    "i'm alright",
    "i'm okay",
]

EVENT_STRS_1 = [
    "what are my upcoming events",
    "when are my upcoming events",
    "show my upcoming events",
]

EVENT_STRS_2 = [
    "what is today's date",
    "give me today's date",
    "what is the date today",
]

NAME_STRS_1 = [
    "what is your name",
    "what's your name",
    "give me your name",
]

def speak(text):
    engine = pyttsx3.init()
    engine.say(text)
    engine.runAndWait()

def get_audio():
    print("Begin speaking..")
    r = sr.Recognizer()
    with sr.Microphone() as source:
        audio = r.listen(source=source,timeout=5,phrase_time_limit=5)
        try:
            print(r.recognize_google(audio))
        except LookupError:
            print("Could not understand")
     
    return r.recognize_google(audio)


def authenticate_google():
    creds = None
    # The file token.pickle stores the user's access and refresh tokens, and is
    # created automatically when the authorization flow completes for the first
    # time.
    if os.path.exists('token.pickle'):
        with open('token.pickle', 'rb') as token:
            creds = pickle.load(token)
    # If there are no (valid) credentials available, let the user log in.
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(
                'credentials.json', SCOPES)
            creds = flow.run_local_server(port=0)
        # Save the credentials for the next run
        with open('token.pickle', 'wb') as token:
            pickle.dump(creds, token)

    service = build('calendar', 'v3', credentials=creds)

    return service

    
def get_events(service):  
    # Call the Calendar API
    now = datetime.datetime.utcnow().isoformat() + 'Z' # 'Z' indicates UTC time
    print('Getting the upcoming 10 events')
    print("-------------")
    events_result = service.events().list(calendarId='primary', timeMin=now,
                                        maxResults=10, singleEvents=True,
                                        orderBy='startTime').execute()
    events = events_result.get('items', [])

    if not events:
        print('No upcoming events found.')
    for event in events:
        start = event['start'].get('dateTime', event['start'].get('date'))
        print(start[5:10])
        print(event['summary'])
        print("----------")
    
    return events

def date_to_string(date): #format ex: 08-21
    day = DAY_PRONOUNCE[int(date[3:5])-1] #int 
    int_month = int(date[0:2]) #int
    return MONTHS[int_month] + " " + day

def date_to_string_year(date): #format ex: 2000-08-21
    day = DAY_PRONOUNCE[int(date[8:10])-1] #int 
    int_month = int(date[5:7])-1 #int
    return f"{MONTHS[int_month]} {day} {date[0:5]}"


#----------------------------------------------------------------------------------------------------------------

service = authenticate_google()
text = get_audio().lower()
print("You said: " + text)

#RETURN 'HELLO'
for greeting in GREETING_STRS_1:
    if greeting in text:
        speak(random.choice(GREETING_STRS_1_ANSWERS))

#RETURN 'HOW ARE YOU'
for greeting in GREETING_STRS_2:
    if greeting in text:
        speak(random.choice(GREETING_STRS_2_ANSWERS))

#RETURN ALL EVENTS (SUMMARY + DATE)
for phrase in EVENT_STRS_1:
    if phrase in text:
        events = get_events(service)
        speak("You have")
        for event in events:
            start = event['start'].get('dateTime', event['start'].get('date'))
            speak(event['summary'] + "On" + date_to_string(start[5:10]))

#RETURN DATE TODAY
for phrase in EVENT_STRS_2:
    if phrase in text:
        date = datetime.date.today()
        today = f"{date}"
        speak(date_to_string_year(today))

#RETURN NAME
for phrase in NAME_STRS_1:
    if phrase in text:
        speak("My name is Neo.")


# TODO 
# implement one return speak() instead of multiple, especially for loops
# keyboard input while loop
# what day is august 24
# install weather api for voice assistant 
# install google maps api for voice assistant , nearby places, traffic 
# install some sort of messaging 
# 



