# 29) Enter three input dates with time. Check whether
#  third input date is between first and second entered date.


from datetime import datetime

def check_date_in_range(date1, date2, date3):
    date_format = "%d-%m-%Y %H:%M" 
    
    try:
        date1 = datetime.strptime(date1, date_format)
        date2 = datetime.strptime(date2, date_format)
        date3 = datetime.strptime(date3, date_format)
        
        if date1 < date3 < date2 or date2 < date3 < date1:
            return "Yes, the third date is between the first and second dates."
        else:
            return "No, the third date is not between the first and second dates."
    except ValueError:
        return "Invalid date format. Please use the correct format: dd-mm-yyyy HH:MM"

date1 = "31-01-1996 14:00"
date2 = "30-08-1996 10:00"
date3 = "22-07-1996 20:00"

print(check_date_in_range(date1, date2, date3))
