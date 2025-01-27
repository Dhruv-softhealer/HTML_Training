# Question 1: Find Second Largest Number
# Write a function that takes a list of integers as input and returns the second largest number
# in the list.

lst = [5, 10, 10]
x = set(lst)
x.remove(max(x))

print(max(x))