# 16) return me list which contains lists of index whose sum is 9, no repetation
# for example: 5 and 4
# my_list = [3,8,5,4,6,3,1]
# for eg [[2,3],[4,5] ]


my_list = [3,8,5,4,6,3,1]
result = []

for i in range(len(my_list)):
    for j in range(i + 1, len(my_list)):
        if my_list[i] + my_list[j] == 9:
            result.append([i, j])

print(result)
