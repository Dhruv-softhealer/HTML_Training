'''
4) write below pattern using loop

A A A A A A A
A A
A A
A A
A
A A
A A
A A
A A A A A A A

'''

for i in range(9):
    for j in range(7):
        if i==0 or i==8 or j<2:
            if i==4 and j>0:
                continue 
            print('A ',end="")
    print()