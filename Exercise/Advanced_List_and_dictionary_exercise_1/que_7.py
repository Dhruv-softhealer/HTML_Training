'''
By using list comprehension, please write a program to print the list after removing the 0th,4th,5th numbers in [12,24,35,70,88,120,155].
'''

li = [12,24,35,70,88,120,155]
print(li)
lis2 = [li[i] for i in range(len(li)) if i!=4 and i!=5 and i!=0]
print(lis2)