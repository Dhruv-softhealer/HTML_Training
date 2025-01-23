'''
5) Take number inputs from users till he press "q" key, after that print
Minimum Number
Maximum Number
Closest Number
Longest Number
Total Sum
Average Of All
'''

li = []
user_input = 0
sum_of_num = 0
while user_input != 'q':
    user_input = input('Enter Number or "q" for quit : ')

    if user_input!='q':
        li.append(int(user_input))
        sum_of_num += int(user_input)

li = sorted(li)

diff_li = [0,0]

temp = li[-1]
for i in range(1,len(li)):
    diff = li[i] - li[i-1]
    if diff <= temp:
        # temp=diff
        diff_li[0]=li[i]
        diff_li[1]=li[i-1]
        if diff == 1:
            break
    
print("Minimum Number : ",li[0])
print("Maximum Number : ",li[-1])
print("Closest Number : ",diff_li)
print(f"Longest Number : {li[0],li[-1]}")
print("Total Sum : ", sum_of_num)
print("Average Of All : ",sum_of_num/len(li))