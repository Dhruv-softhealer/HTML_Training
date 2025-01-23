# 11) Remove Even(number) element from list. 

# list1 = [11, 5, 17, 18, 23, 50]

li = [11, 5, 17, 18, 23, 50]



ans = []

for i in li:
	if i % 2 != 0:
		ans.append(i)

print(ans)
