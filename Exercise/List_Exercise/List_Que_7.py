# 12) print-duplicates-list-integers 
# x = [1,2,1,2,3,4,5,1,1,2,5,6,7,8,9,9]


a = [1,2,1,2,3,4,5,1,1,2,5,6,7,8,9,9]

dup = []

for i in range(len(a)):
    for j in range(i + 1, len(a)):
        if a[i] == a[j] and a[i] not in dup:
            dup.append(a[i]) 

print(dup)