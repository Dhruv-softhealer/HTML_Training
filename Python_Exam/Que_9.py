# Question 9: Day of the Week from Date
# Write a Python program that takes a date in YYYY-MM-DD format and returns the day of the
# week (e.g., "Monday", "Tuesday").

import datetime
x = datetime.datetime(2021,10,11)

print(x.strftime("%A"))