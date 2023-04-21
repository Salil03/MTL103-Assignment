def gomory(filename):
  f = open(filename)
  n, m = [int(x) for x in f.readline().strip().split(' ')]
  b = [int(x) for x in f.readline().strip().split(' ')]
  c = [-int(x) for x in f.readline().strip().split(' ')]
  A = [[int(x) for x in f.readline().strip().split(' ')] for i in range(m)]
  f.close()
  tableau = tableau_setup(A, b,c,n, m)
  fractional_dual_simplex(tableau)
  x = [0 for x in range(n)]
  for row in tableau:
    if row[0][0] >= 1 and row[0][0] <= n:
      x[row[0][0]-1] = row[0][1]
  return x 

def round_off(num):
  if abs(num - round(num)) < 0.0000000001:
    return round(num)
  else:
    return num

def frac(num):
  if num < 0:
    return 1 + num + int(-num)
  return (num - int(num))

def check_integer(num):
  return (frac(num) == 0)

def generate_cut(tableau, cut_row, n, m):
  tableau[cut_row][0][1] = round_off(tableau[cut_row][0][1])
  for column in range(1, n+1):
    tableau[cut_row][column] = round_off(tableau[cut_row][column])
  for row in range(0, m+1):
    tableau[row].append(0)
  new_row = []
  new_row.append([n+1, -frac(tableau[cut_row][0][1])])
  for column in range(1, n+1):
    new_row.append(-frac(tableau[cut_row][column]))
  new_row.append(1)
  tableau.append(new_row)
  return None

def fractional_dual_simplex(tableau):
  m = len(tableau)-1
  n = len(tableau[0])-1
  primal_simplex(tableau, n,m)
  integer = False
  while not integer:
    integer = True
    for row in range(1, m+1):
      tableau[row][0][1] = round_off(tableau[row][0][1])
      if not check_integer(tableau[row][0][1]):
        integer = False
        tableau[0][0][1] = round_off(tableau[0][0][1])
        if not check_integer(tableau[0][0][0]):
          generate_cut(tableau, 0, n, m)
        else:
          generate_cut(tableau, row, n, m)
        n += 1
        m +=1
        dual_simplex(tableau, n, m)
        break
  return tableau




def tableau_setup(A, b, c, n, m):
  for row in range(m):
    if b[row] < 0:
      b[row] *= -1
      for column in range(n):
        A[row][column] *= -1
  tableau = []
  tableau_row = [[0,0]]
  for column in range(n):
    tableau_row.append(c[column])
  for column in range(n):
    tableau_row.append(0)
  tableau.append(tableau_row)
  for row in range(1, m+1):
    tableau_row = []
    tableau_row.append([row+n, b[row-1]])
    for column in range(n):
      tableau_row.append(A[row-1][column])
    for column in range(1, n+1):
      if column == row:
        tableau_row.append(1)
      else:
        tableau_row.append(0)
    tableau.append(tableau_row)
  return tableau

def primal_simplex(tableau, n, m):
  optimal = False
  while not optimal:
    optimal = True
    for column in range(1, n+1):
      tableau[0][column] = round_off(tableau[0][column])
      if tableau[0][column] < 0:
        optimal = False
        primal_simplex_iteration(tableau, n, m, column)
        break
  return tableau

def primal_simplex_iteration(tableau, n, m, pivot_column):
  minimum = -1
  pivot_row = -1
  for row in range(1, m+1):
    tableau[row][pivot_column] = round_off(tableau[row][pivot_column])
    if tableau[row][pivot_column]<=0:
      continue
    if tableau[row][0][1]/tableau[row][pivot_column] < minimum or minimum == -1:
      minimum = tableau[row][0][1]/tableau[row][pivot_column]
      pivot_row = row
  simplex_pivot(tableau, pivot_row, pivot_column, n, m)
  return

def dual_simplex(tableau,n, m):
  feasible = False
  while not feasible:
    feasible = True
    for row in range(1, m+1):
      tableau[row][0][1] = round_off(tableau[row][0][1])
      if tableau[row][0][1] < 0:
        feasible = False
        dual_simplex_iteration(tableau, row, n, m)
  return tableau

def dual_simplex_iteration(tableau, pivot_row, n, m):
  minimum = -1
  pivot_column = -1
  for column in range(1, n+1):
    tableau[pivot_row][column] = round_off(tableau[pivot_row][column])
    if tableau[pivot_row][column] >= 0:
      continue;
    if (tableau[0][column]/abs(tableau[pivot_row][column])) < minimum or minimum == -1:
      minimum = tableau[0][column]/abs(tableau[pivot_row][column])
      pivot_column = column
  simplex_pivot(tableau, pivot_row, pivot_column, n,m)
  


def simplex_pivot(tableau, pivot_row, pivot_column, n, m):
  factor = tableau[pivot_row][pivot_column]
  tableau[pivot_row][0][0] = pivot_column
  tableau[pivot_row][0][1] /= tableau[pivot_row][pivot_column]
  for column in range(1, n+1):
    tableau[pivot_row][column] /= factor
  for row in range(m+1):
    if row == pivot_row:
      continue
    factor = tableau[row][pivot_column]
    tableau[row][0][1] -= factor* tableau[pivot_row][0][1]
    for column in range(1, n+1):
      tableau[row][column] -= factor * tableau[pivot_row][column]
  return


# A = [[[0, 1], 0.0, 0.0, 0.0, 0.0, 1.0, 0], [[1, 0.6666666666666667], 1, 0, 0, -0.3333333333333333, 0.6666666666666666, 0], [[2, 1.0], 0.0, 1.0, 0.0, 0.0, 1.0, 0], [[3, 2.0], -0.0, -0.0, 1.0, 1.0, -4.0, 0], [[6, -0.6666666666666667], 0, 0, 0, -0.6666666666666666, -0.6666666666666666, 1]]

# print(dual_simplex(A, 6, 4))

print(gomory("input.txt"))