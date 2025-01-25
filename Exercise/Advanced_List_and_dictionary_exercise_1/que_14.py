'''
Write a Python program that accepts a string and calculate the number of digits and letters.

Input

Hello321Bye360

Output

Digit - 6
Letter - 8
'''

input_str = input("Enter String : ")

string_count = 0
digit_count = 0
for st in input_str:
    if st.isdigit():
        digit_count+=1
    else:
        string_count+=1

print(f"Digit {digit_count}")
print(f"Letter {string_count}")