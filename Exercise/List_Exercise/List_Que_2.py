# 7) From a given list of n	​atural numbers, return the two closest numbers.



# Input = [3, 9, 50, 15, 99, 7, 98, 65]

# Output = [98,99]

li = [3, 9, 50, 15, 99, 7, 98, 65]

li = sorted(li)

c_li = [0, 0]

temp = li[-1]

for i in range(1, len(li)):
    dif = li[i] - li[i-1]
    if dif <= temp:
        temp=dif
        c_li[0] = li[i]
        c_li[1] = li[i-1]
        if dif == 1:
            break

print(c_li)