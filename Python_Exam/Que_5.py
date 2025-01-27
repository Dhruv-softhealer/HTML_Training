# Question 5: Rotate List n Positions
# Write a Python function to rotate a list n positions to the right.

lst = [1, 2, 3, 4, 5, 6]

n = int(input("enter position : "))

rotated_lst = lst[n:]+lst[:n]
print(rotated_lst)