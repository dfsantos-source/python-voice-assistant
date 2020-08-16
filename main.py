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
DAY_ABREVS = [
    'mon',
    'tue',
    'wed',
    'thu',
    'fri',
    'sat',
    'sun',
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
    "greetings",
    "what's good",
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
    "upcoming events",
    "what are my upcoming events",
    "when are my upcoming events",
    "show my upcoming events",
]

DATE_STRS_1 = [
    "what is today's date",
    "give me today's date",
    "what's today's date",
    "what is the date today",
]

EVENT_STRS_3 = [
    "what is on",
    "anything on",
    "plans on",
    "events on",
    "event on",
    "event tomorrow",
    "events tomorrow",
    "events today",
    "event today"
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
        except Exception:
            print("EXCEPTION FOUND")
     
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
        return None
    else:
        return events

# Gets an event, given a date
def get_event(date, service):
    # Call the Calendar API
    start = datetime.datetime.combine(date, datetime.datetime.min.time())
    start = start.astimezone(pytz.UTC).isoformat()
    end = datetime.datetime.combine(date, datetime.datetime.max.time())
    end = end.astimezone(pytz.UTC).isoformat()  
    
    events_result = service.events().list(calendarId='primary', timeMin=start, timeMax=end,
                                        singleEvents=True,
                                        orderBy='startTime').execute()
    events = events_result.get('items', [])
    if not events:
        return None
    else:
        return events

#AT THE SAME TIME WE MUST KEEP IN MIND THE YEAR
#WE ARE TALKING ABOUT OTHER MONTHS
#august 21
#WE ARE TALKING ABOUT THIS MONTH
#next mon,tues,etc.
#on the [21st, 22nd etc.]
def get_date(text):
    today = datetime.date.today()
    day = -1
    month = -1
    year = today.year

    if text.count("tomorrow") > 0:
        return today + datetime.timedelta(1)

    if text.count("today") > 0:
        return today    
    

    for word in text.split():
        if word in MONTHS:
            month = MONTHS.index(word) + 1
        elif word.isdigit():
            day = int(word)

    if month < today.month:
        year += 1

    return datetime.date(month=month, day=day, year=year)

def date_to_string(date): #format ex: 08-21
    day = DAY_PRONOUNCE[int(date[3:5])-1] #int 
    int_month = int(date[0:2]) #int
    return MONTHS[int_month-1] + " " + day

def date_to_string_year(date): #format ex: 2000-08-21
    day = DAY_PRONOUNCE[int(date[8:10])-1] #int 
    int_month = int(date[5:7])-1 #int
    return f"{MONTHS[int_month]} {day} {date[0:4]}"


#----------------------------------------------------------------------------------------------------------------

# WAIT FOR USER INPUT
# input("Press Enter then begin speaking..")

# INITIALIZE VARIABLES
service = authenticate_google()
text = get_audio().lower()
text_tokens = text.split()
print('You said: ' + text)
output = ""
phraseFound = False

# RETURN 'HELLO'
for greeting in GREETING_STRS_1:
    if greeting in text_tokens:
        phraseFound = True
        output += ' ' + random.choice(GREETING_STRS_1) + '.'
        break

# RETURN 'HOW ARE YOU'
for greeting in GREETING_STRS_2:
    if greeting in text:
        phraseFound = True
        output += ' ' + random.choice(GREETING_STRS_2_ANSWERS) + '.'
        break

# RETURN ALL EVENTS (SUMMARY + DATE)
for phrase in EVENT_STRS_1:
    if phrase in text:
        phraseFound = True
        events = get_events(service)
        output += ' ' + "you have"
        for event in events:
            start = event['start'].get('dateTime', event['start'].get('date'))
            output += ' ' + event['summary'] + ' ' + "on" + ' ' + date_to_string(start[5:10]) + ','
        break

# RETURN DATE TODAY (month, day, year)
for phrase in DATE_STRS_1:
    if phrase in text:
        phraseFound = True
        date = datetime.date.today()
        today = f"{date}"
        output += '' + "today's date is, " + date_to_string_year(today) + ','
        break

# RETURN NAME
for phrase in NAME_STRS_1:
    if phrase in text:
        phraseFound = True
        output += ' ' + "My name is Neo."
        break

# RETURN EVENT, GIVEN A DATE
# must be said in the form ex: 'on august 21'
for phrase in EVENT_STRS_3:
    if phrase in text:
        phraseFound = True
        dateInstance = get_date(text)
        events = get_event(dateInstance, service)
        if events is not None:
            for event in events:
                start = event['start'].get('dateTime', event['start'].get('date'))
                output += ' ' + event['summary'] + ' ' + "on" + ' ' + date_to_string(start[5:10]) + ','
            break
        else:
            output += " No events on that date."
            break


# SPEAK OUTPUT
if phraseFound == True:
    print("Output String: " + output)
    speak(output)
else:
    print("No phrase found.")


# TODO 
# implement st, nd, rd, th, and 'tomorrow' for date 
# what day is august 24
# install weather api for voice assistant 
# install google maps api for voice assistant , nearby places, traffic 
# install some sort of messaging 
# 



