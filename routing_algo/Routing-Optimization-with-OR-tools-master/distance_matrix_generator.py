# Create a zero matrix of w x h
# w, h = 200, 200
# matrix = [[0] * w for i in range(h)]
#
# # List of your numbers
# numbers = list(range(0,200))
#
# # Fill your numbers in
# # go one row at a time and fill until you reach the diagonal
# for i in range(200):
#     for j in range(0, i):
#             matrix[i][j] = matrix[j][i] = numbers[i]
#
# # Print all rows
# for row in matrix:
#     print(str(row) + ",")
import random
demands = []
for demand in range(1, 21):
    demands.append(40)

print(demands)
print(len(demands))