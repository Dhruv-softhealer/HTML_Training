# Question 2: List People Aged 30 and Above
# Write a function that takes a list of tuples (each tuple contains a name and age) and returns
# a list of names of people aged 30 and above.

mylist = [("Alice", 25), ("Bob", 35), ("Charlie", 30)]

c = [i for i in mylist if i[1]>=30]
print(c)
