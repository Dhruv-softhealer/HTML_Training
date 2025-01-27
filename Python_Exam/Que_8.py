# Question 8: Most Frequent Element Across Lists
# You have a dictionary where the values are lists. Find the most frequent element across all
# lists.

mydict = {'a': [1, 2, 3], 'b': [2, 3, 4], 'c': [2, 3, 4]}
lst = []
for i in mydict.values():
    lst.append(i)

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

n = max(ans,key=ans.count)
print(n)