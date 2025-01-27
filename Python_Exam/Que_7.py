# Question 7: Invert a Dictionary
# Given a dictionary, write a program to invert it. The keys become values, and the values
# become keys.

mydict = {'a': 1, 'b': 2, 'c': 3}
newdict = {v: k for k, v in mydict.items()}
print(newdict)