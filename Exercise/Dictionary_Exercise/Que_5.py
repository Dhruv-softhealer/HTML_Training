# 26)Write a Python script to merge two Python dictionaries.

# dic1 = {1:10, 2:20, 3:30, 4:40, 5:50}

# dic2 = {6:60, 7:70, 8:80}

# dic3 = {*dic1.items(), *dic2.items()}

# print(dict(dic3))

d1 = {'w': 1, 'x': 2}
d2 = {'y': 3, 'z': 4}

d1.update(d2)
print(d1)