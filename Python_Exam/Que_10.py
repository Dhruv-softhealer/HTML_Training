# Question 10: Parse JSON and Check Keys
# Write a Python program that parses a JSON string into a Python dictionary, checks if the
# name and age keys are present, and prepares a new JSON string from the dictionary.


import json

json_string = '{"name": "Alice", "age": 25}'

dic = json.loads(json_string)
print(dic)

keys= ['name', 'age']

for i in dic:
    if i not in keys:
        print(f'{i} is not present')
    else:
        print(f'{i} is present')

json_data = json.dumps(dic)
print("Converted into Json : ",json_data)