# 22) Sorted dic sequence wise

# INPUT : dic1 = {‘list1’ : {‘id’: 123 ,’name’: ‘ABC’ , sequence: ‘5’},

# list2’ : {‘id’: 124 ,’name’: ‘DEF’ , sequence: ‘4’},

# list3’ : {‘id’: 125 ,’name’: ‘XYZ’ , sequence: ‘1’},

# list4’ : {‘id’: 126 ,’name’: ‘MNO’ , sequence: ‘3’},

# list5’ : {‘id’: 127 ,’name’: ‘PQR’ , sequence: ‘2’}}


# OUTPUT :

# dic1 = { list3’ : {‘id’: 125 ,’name’: ‘XYZ’ , sequence: ‘1’},

# list5’ : {‘id’: 127 ,’name’: ‘PQR’ , sequence: ‘2’},

# list4’ : {‘id’: 126 ,’name’: ‘MNO’ , sequence: ‘3’},

# list2’ : {‘id’: 124 ,’name’: ‘DEF’ , sequence: ‘4’},

# ‘list1’ : {‘id’: 123 ,’name’: ‘ABC’ , sequence: ‘5’}}

dic = {
    "lst1" : {'id' : 123, 'name' : 'ABC', 'sequence': 5},
    "lst2" : {'id' : 124, 'name' : 'DEF', 'sequence': 4},
    "lst3" : {'id' : 125, 'name' : 'XYZ', 'sequence': 1},
    "lst4" : {'id' : 126, 'name' : 'MNO', 'sequence': 3},
    "lst5" : {'id' : 127, 'name' : 'PQR', 'sequence': 2},
}

 
res = sorted(dic.items(), key = lambda x: x[1]['sequence'])
 
print("The sorted dictionary by marks is : " + str(res))