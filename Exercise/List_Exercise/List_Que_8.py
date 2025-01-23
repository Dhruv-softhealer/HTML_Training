# 13) reversing the given list
# x = [10, 11, 12, 13, 14, 15]

x = [10, 11, 12, 13, 14, 15]
newl = []
num = len(x)-1
while num >= 0:
    newl.append(x[num])
    num -= 1

print(newl)

# OR

# x = [10, 11, 12, 13, 14, 15]
# x.sort(reverse=True)
# print(x)