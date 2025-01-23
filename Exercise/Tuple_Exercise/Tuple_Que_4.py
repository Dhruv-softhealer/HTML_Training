# 20)count the elements in a list until an element is a tuple.
# tup = [10,20,30,(10,20),40]

tup = [10,20,30,(10,20),40]


count = 0

for x in tup:
    if isinstance(x, tuple):
        break
    count+=1

print(count)
