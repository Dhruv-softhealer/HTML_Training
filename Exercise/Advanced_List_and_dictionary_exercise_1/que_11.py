'''
Python Program to Convert Two Lists Into a Dictionary
index = [1, 2, 3]
languages = ['python', 'java', 'c']
'''

index = [1, 2, 3]
languages = ['python', 'java', 'c']
dt = {}
for key,value in zip(index,languages):
    dt[key] = value

print(dt)