'''
Question:

You are given a string.Your task is to count the frequency of letters of the string and print the letters in descending order of frequency.

'''

input_str = input("Enter String : ")

def sort_freq(freq):
    return freq[1]

dt = {}

for st in input_str:
    if st in dt.keys():
        dt[st]+=1
    else:
        dt[st]=1

dt_ls = list(dt.items())
dt_ls.sort(key=sort_freq,reverse=True)
dt = dict(dt_ls)

for key,value in dt.items():
    print(f'{key},{value}')