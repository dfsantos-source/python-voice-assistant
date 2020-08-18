import datetime


today = datetime.datetime.today()
today = datetime.datetime.combine(today, datetime.datetime.min.time())

date = today + datetime.timedelta(5)

date = datetime.datetime.combine(date, datetime.datetime.min.time())

print(f"Today: {today}")
print(f"Date: {date}") 

if (today + datetime.timedelta(7) >= date):
    print("Valid date")
else:
    print("Not valid date")

diff = date - today

result = f"{diff}"
result = result[:1]

print("difference is:")
print(result[:1])

x = int(result)
print(x)


#print(today)
#print(today_midnight)
#print(date)
#print(date_midnight)
