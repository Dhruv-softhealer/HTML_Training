# ​15) Make only one list if you have list inside list inside list.
# my_list = [1,[1.1,2,[3],6],7,9,[5.6,[8]],9]

# output = [1,1.1,2,3,6,7,9,5.6,8,9]

# lis = [1,[1.1,2,[3],6],7,9,[5.6,[8]],9]

# def flat(lis):
# 	flatList = []
# 	for element in lis:
# 		if type(element) is list:
# 			for item in element:
# 				flatList.append(item)
# 		else:
# 			flatList.append(element)
# 	return flatList



# print('Flat List', flat(lis))

lst = [1,[1.1,2,[3],6],7,9,[5.6,[8]],9]
def flatten(lst):
    result = []
    for item in lst:
        if type(item) is list:
            result.extend(flatten(item)) 
        else:
            result.append(item)
    return result

flattened_list = flatten(lst)
print(flattened_list)

