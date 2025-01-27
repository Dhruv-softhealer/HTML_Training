# Question 13: Reverse Only Vowels in a String
# Given a string, your task is to reverse only the vowels in the string.

a = input("Enter string to reverse a vowels only : ")
lst = []
for i in a:
    if i in 'aeiou':
        lst.append(i)
letters = list(a)
for i in range(len(letters)):
    if letters[i] in 'aeiou':
        letters[i] = lst.pop(-1)

print(letters)
