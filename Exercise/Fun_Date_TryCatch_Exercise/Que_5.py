# 10 ) Program to display calendar of the given month and year

# November 2014

# Mo Tu We Th Fr Sa Su
# 1 2
# 3 4 5 6 7 8 9
# 10 11 12 13 14 15 16
# 17 18 19 20 21 22 23
# 24 25 26 27 28 29 30

import calendar 
   

year = int(input("Enter Year : "))
month = int(input("Enter Month : "))

print(calendar.month(year, month)) 