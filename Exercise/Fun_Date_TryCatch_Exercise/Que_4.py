# ==> input 3 name and related birthdate and find out who is yonger and older.

# input

# Sagar 31-1-1996
# Kishan 30-1-1996
# Nikhil 22-7-1989

# Output

# Kishan is yonger
# Nikhil is older


from datetime import datetime

def find_age_order(names_and_birthdates):
    people = []
    
    date_format = "%d-%m-%Y"
    for name, birthdate in names_and_birthdates:
        try:
            birthdate = datetime.strptime(birthdate, date_format)
            people.append((name, birthdate))
        except ValueError:
            return "Invalid date format. Please use the correct format: dd-mm-yyyy"
    
    people.sort(key=lambda x: x[1])
    
    oldest = people[0]
    youngest = people[-1]
    
    return f"{youngest[0]} is younger\n{oldest[0]} is older"

names_and_birthdates = [
    ("Sagar", "31-01-1996"),
    ("Kishan", "30-01-1996"),
    ("Nikhil", "22-07-1989")
]

print(find_age_order(names_and_birthdates))
