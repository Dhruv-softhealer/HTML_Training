'''# Program to add two matrices using nested loop

            X = [[12,7,3],
            [4 ,5,6],
            7 ,8,9]]

            Y = [[5,8,1],
            [6,7,3],
            [4,5,9]]

            Z = [[0,8,4],
            [6,9,3],
            [9,1,9]]

Result Matrix = 3Y + (X + 2Y) + (5Z + 4X)'''


x = [[12,7,3],
    [4,5,6],
    [7,8,9]]

y = [[5,8,1],
    [6,7,3],
    [4,5,9]]

z = [[0,8,4],
    [6,9,3],
    [9,1,9]]

res_matrix = [ [0,0,0] for i in x]

for i in range(len(x)):
    for j in range(len(x[i])):
        res_matrix[i][j] = 3*y[i][j] + (x[i][j] + 2*y[i][j]) + (5*z[i][j] + 4*x[i][j])

for i in res_matrix:
    print(i)