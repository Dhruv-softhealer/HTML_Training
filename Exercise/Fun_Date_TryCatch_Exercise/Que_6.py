# 30) Using Try-catech

#  1) value Error (for ex. sum of string + integer)

#  2) Dvide by zero

#  3) Access Error

n1 = input("Enter Number 1 : ")
n2 = input("Enter Number 2 : ")
passwd = input("Enter Password : ") # 123
str = "10"
try:
    if passwd != '123':
        raise PermissionError("Access Denied")
    divide = int(n1)/int(n2)
    print(divide)
except PermissionError as pe:
    print("Access Error : ",pe)
except ValueError as ve:
    print("Value Error : ",ve)
except ZeroDivisionError as ze:
    print("Divison Error : ",ze)
