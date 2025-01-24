# 28) Write a Python program to Square and  

# cube every number in a given list of integers using Lambda

lst = [1,2,3,4,5,6,7]

x = list(map(lambda a : a ** 2, lst))
y = list(map(lambda a : a ** 3, lst))
print(x)
print(y)