''' 
Please write a program which count and print the numbers of each character in a string input by console.
'''

dic = {}
input_st = input("Enter a String : ")

for st in input_st:
    if st not in dic.keys():
        dic[st] = 1
    else:
        dic[st]+=1


print("Input String : ",input_st)
print("Character count : ")
for char,count in dic.items():
    print(f'{char},{count}')