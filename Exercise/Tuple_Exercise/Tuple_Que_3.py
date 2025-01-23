# 19)remove an empty tuple(s) from a list of tuples.
# Sample data: [(), (), ('',), ('a', 'b'), ('a', 'b', 'c'), ('d')]

lst = [(), (), ('',), ('a', 'b'), ('a', 'b', 'c'), ('d')]
newlst = []
for x in lst:
    if x:
        newlst.append(x)

print(newlst)