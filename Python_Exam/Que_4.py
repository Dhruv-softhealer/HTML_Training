# Question 4: Remove Even Numbers Using List Comprehension
# Write a program to remove all even numbers from a list and return the remaining list using
# list comprehension.

lst = [1, 2, 3, 4, 5, 6, 7, 8, 9]
new_lst=[]
for i in range(0, len(lst)):
    if lst[i]%2!=0:
        new_lst.append(lst[i])
print(new_lst)