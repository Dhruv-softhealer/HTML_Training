# Question 6: Flatten a Nested List
# Write a Python program to flatten a nested list and return the flattened list.


lst = [[1, 2, 3], [4, 5], [6, 7, [8, 9]]]
def flatten(lst):
    result=[]
    for item in lst:
        if type(item) is list:
            result.extend(flatten(item))
        else:
            result.append(item)
    return result

ans = flatten(lst)
print(ans)