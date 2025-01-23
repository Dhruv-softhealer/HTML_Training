# 10) 
# # Program to multiply two matrices using nested loops

# # 3x3 matrix

# X = [[12,7,3],
#     [4 ,5,6],
#     [7 ,8,9]]	​
# # 3x4 matrix
# Y = [[5,8,1,2],
#     [6,7,3,0],
#     [4,5,9,1]]

A = [[12, 7, 3],
    [4, 5, 6],
    [7, 8, 9]]

B = [[5, 8, 1, 2],
    [6, 7, 3, 0],
    [4, 5, 9, 1]]
    
ans = [[0, 0, 0, 0],
        [0, 0, 0, 0],
        [0, 0, 0, 0]]

for i in range(len(A)):
    for j in range(len(B[0])):
        for k in range(len(B)):
            ans[i][j] += A[i][k] * B[k][j]

for a in ans:
    print(a)