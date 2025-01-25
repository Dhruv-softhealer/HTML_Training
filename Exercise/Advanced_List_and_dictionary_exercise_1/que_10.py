'''
# Sort only the values
'''

dt = {7:8, 1:9, 6:3}
print("Original Dict : ",dt)

keys = list(dt)
values = list(dt.values())
values.sort()

for key,value in zip(keys,values):
    dt[key]=value

print("Only Values Order Dict : ",dt)