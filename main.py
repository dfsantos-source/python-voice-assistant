from __future__ import print_function
import datetime
import pickle
import os.path
from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
import os
import time
import playsound
import pyaudio
import speech_recognition as sr
from gtts import gTTS

SCOPES = ['https://www.googleapis.com/auth/calendar.readonly']
DAYS = ["monday", "tuesday", "wednesday", "thursday", "friday"]
MONTHS = ["january", "february", "march", "april", "may", "june", "july", "august", "september", "october", "november", "december"]
DAY_EXTENSIONS = ["rd","th","st"]


def speak(text):
    tts = gTTS(text=text, lang="en")
    filename = "voice.mp3"
    tts.save(filename)
    playsound.playsound(filename)

def get_audio():
    r = sr.Recognizer()
    with sr.Microphone() as source:
        audio = r.listen(source=source,timeout=5,phrase_time_limit=5)
        said = ""

        try:
            said = r.recognize_google(audio)
            print(said)
        except LookupError:
            print("Could not understand")
     
    return said


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

    
def get_events(n, service):  
    # 'n' is the amount of events to get, 'service' was returned from authenticate_google()
    # Call the Calendar API
    now = datetime.datetime.utcnow().isoformat() + 'Z' # 'Z' indicates UTC time
    print(f'Getting the upcoming {n} events')
    events_result = service.events().list(calendarId='primary', timeMin=now,
                                        maxResults=n, singleEvents=True,
                                        orderBy='startTime').execute()
    events = events_result.get('items', [])

    if not events:
        print('No upcoming events found.')
    for event in events:
        start = event['start'].get('dateTime', event['start'].get('date'))
        print(start, event['summary'])

def get_date(text):
    text = text.lower()
    today = datetime.date.today() 

    if text.count("today") > 0: #if 'today' is mentioned in the text
        return today

    day = -1
    day_of_week = -1
    month = -1
    year = today.year

    for word in text.split(): #splits text word by word, looks for keywords 'month' 'day' 'day_of_week'
        if word in MONTHS:
            month = MONTHS.index(word) + 1  
        elif word in DAYS:
            day_of_week = DAYS.index(word) 
        elif word.isdigit():
            day = int(word)
        else:
            for ext in DAY_EXTENSIONS:
                found = word.find(ext)
                if found > 0:
                    try:
                        day = int(word[:found])
                    except:
                        pass
    
    if month != -1 and month < today.month: #if the month we're talking about exists AND is in the past (before today's month)
        year = year + 1

    if day != -1 and month == -1 and day < today.day: #if the day AND month we're talking about exists AND day is in the next month
        month = month + 1 

    if month == -1 and day == -1 and day_of_week != -1: #we only have a 'day_of_week' to build the date
        current_day_of_week = today.weekday()
        dif = day_of_week - current_day_of_week 

        if dif < 0: 
            dif += 7
            if text.count("next") >= 1:
                dif += 7
        
        return today + datetime.timedelta(dif)
    
    return datetime.date(month=month, day=day, year=year)


#TEST COMMANDS
service = authenticate_google()
get_events(2, service)

text = get_audio().lower()
print(get_date(text))