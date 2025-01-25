'''
Given a number N.Find Sum of 1 to N Using Recursion

Input

5

Output

15
Hints
Make a recursive function to get the sum
'''

def sum_of_n(n):
    if n < 1:
        return 0
    else:
        return n + sum_of_n(n-1)

n = int(input("Enter Number "))
print(f"Sum of 1 to {n} : ",sum_of_n(n))