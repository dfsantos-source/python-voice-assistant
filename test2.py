import datetime

DAYS = [
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


text = "december 31"
today = datetime.date.today()
day = -1
month = -1
year = today.year

if text.count("today") > 0:
    print(today)

for word in text.split():
    if word in MONTHS:
        month = MONTHS.index(word) + 1
    elif word.isdigit():
        day = int(word)

if month < today.month:
    year += 1

print(datetime.date(month=month, day=day, year=year))
