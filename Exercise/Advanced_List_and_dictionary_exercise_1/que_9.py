'''
Sort the dictionary based on values
'''

dt = {7:8, 1:9, 6:3}
print("Original Dictionary : ",dt)
def sort_val(dt):
    return dt[1]
    
ls = list(dt.items())
ls.sort(key=sort_val)
dt = dict(ls)
print("Ordered By Value : ",dt)