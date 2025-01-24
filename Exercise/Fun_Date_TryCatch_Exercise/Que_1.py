# 27) . I am having an list [1,2,3,4,5,6,7,8,9,10,11,12,13].

# 	Now i am creating a function that returns if the input is a
#  	valid sequence or not, but i have some exceptions that need to be resolved.

# 	1. Input will always be in a sorted manner.
# 	2. Function should return true or false.
# 	3. input length should be >= 3 and < 14. from (numbers 1 to 13)

# 	Examples.

# 	[1,2,3] - true
# 	[1,2,3,4,5] - true
# 	[8,9,10,11] - true
# 	[11,12,13] - true

# 	Exceptions.

# 	[1,11,12,13] - false
# 	[1,8,9,10,11,12,13] - false
# 	[1,4,5,6] - false
# 	[1,3,4,5] – false

seq = [8,9,10,11]

def is_valid_sequence(seq):
    if len(seq) < 3 or len(seq) > 13:
        return False
    
    for i in range(1, len(seq)):
        if seq[i] != seq[i - 1]+1:
            return False
        else:
            return True
print(is_valid_sequence(seq))