# Question 12: Bracket Matcher
# Have the function bracketMatcher(str) take the str parameter being passed and
# return 1 if the brackets are correctly matched and each one is accounted for. Otherwise,
# return 0. Only ( and ) will be used as brackets. If str contains no brackets, return 1.



def Bracketmatcher(str):
    count = 0
    for i in str:
        if i == '(':
            count += 1
        elif i == ')':
            count -= 1
        if count < 0:
            return 0

    if count == 0:
        return 1
    else:
        return 0
    
ans = Bracketmatcher("(hello))((world)")
print(ans)