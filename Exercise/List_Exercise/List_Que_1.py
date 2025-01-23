# 6) Sort the values of first list using second list

# Input : list1 = ["a", "b", "c", "d", "e", "f", "g", "h", "i"]
# 	​        list2 = [ 0,   1,   1,    0,   1,   2,   2,   0,   1]

# Output :['a', 'd', 'h', 'b', 'c', 'e', 'i', 'f', 'g']


list1 = ["a", "b", "c", "d", "e", "f", "g", "h", "i"]
list2 = [0, 1, 1, 0, 1, 2, 2, 0, 1]

x = [val for _, val in sorted(zip(list2, list1))]

print(x)
