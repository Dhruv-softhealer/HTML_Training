# Question 3: Count Occurrences in List
# Write a Python program to count the number of occurrences of an element in a list.

lst = [10, 20, 30, 10, 10, 20, 40, 50]
a = int(input("enter number from list to count total occurence : "))
i=0
count=0
while i<len(lst):
    if a == lst[i]:
        count+=1
    i+=1
print(a, "appears",count,"times")