# 21)multiplying all the numbers of a given tuple.
# Original Tuple:
# (4, 3, 2, 2, -1, 18)
# Output : -864

tup = (4, 3, 2, 2, -1, 18)
ans = 1
i = 0
while i < len(tup):
    ans*=tup[i]
    i+=1
print(ans)