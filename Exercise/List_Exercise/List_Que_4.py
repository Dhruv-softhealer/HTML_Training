# 9) 

# # Program to perform different set operations like in mathematics

# union,intersection,difference,symmetric difference

# # define three sets

# E = {0, 2, 4, 6, 8};

# N = {1, 2, 3, 4, 5};

set1 = {0, 2, 4, 6, 8}
set2 = {1, 2, 3, 4, 5}

ans1 = set1.union(set2)
ans2 = set1.intersection(set2)
ans3 = set1.difference(set2)
ans4 = set1.symmetric_difference(set2)
print(ans1)
print(ans2)
print(ans3)
print(ans4)