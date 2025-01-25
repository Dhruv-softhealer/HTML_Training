'''
With a given list [12,24,35,24,88,120,155,88,120,155], write a program to print this list after removing all duplicate values with original order reserved.
'''

li = [12,24,35,24,88,120,155,88,120,155]
lis = []

for i in li:
    if i in lis:
        continue
    else:
        lis.append(i)

print("Origiinal List : ",li)
print("After removing duplicates and reverse",lis[::-1])