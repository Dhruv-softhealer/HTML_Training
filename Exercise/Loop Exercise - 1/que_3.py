'''
3) find total occurance of each letter = 'aeiou'
'''

st = '''What is Lorem Ipsum Lorem Ipsum is simply dummy text of the printing and typesetting industry Lorem Ipsum has been the industry's standard dummy 
text ever since the 1500s when an unknown printer took a galley
Of type and scrambled it to make a type specimen book it has? '''

dic = {'a':0,'e':0,'i':0,'o':0,'u':0}

for s in st:
    if s in dic.keys():
        dic[s]+=1

print(dic)