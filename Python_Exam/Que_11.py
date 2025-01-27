# Question 11: Word Split from Dictionary
# Have the function WordSplit(strArr) read the array of strings stored in strArr, which
# will contain 2 elements: the first element will be a sequence of characters, and the second
# element will be a long string of comma-separated words in alphabetical order, that
# represents a dictionary.
# Your goal is to determine if the first element in the input can be split into two words, where
# both words exist in the dictionary provided in the second input.

strArr = ["hellocat", "apple,bat,cat,goodbye,hello,yellow,why"]
newstr = []
x = strArr[1]
s=x.split(",")

for n in s:
    if n in strArr[0]:
        newstr.append(n)
print(newstr)