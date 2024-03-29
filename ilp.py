from fractions import Fraction
from math import floor


def gomory(filename):
  f = open(filename)
  n, m = [int(x) for x in f.readline().strip().split(' ')]
  b = [int(x) for x in f.readline().strip().split(' ')]
  c = [-int(x) for x in f.readline().strip().split(' ')]
  A = [[int(x) for x in f.readline().strip().split(' ')] for i in range(m)]
  f.close()
  tableau = tableau_setup(A, b,c,n, m)
  auxillary_simplex(tableau, n+2*m, m)
  tableau_switch(tableau, n, m)
  fractional_dual_simplex(tableau, n)
  x = [0 for x in range(n)]
  for row in tableau:
    if row[0][0] >= 1 and row[0][0] <= n:
      x[row[0][0]-1] = float(row[0][1])
  return x


def frac(num):
  return (num - Fraction(floor(num)))

def check_integer(num):
  return (frac(num)==0)

def generate_cut(tableau, cut_row, n, m):
  for row in range(0, m+1):
    tableau[row].append(Fraction(0))
  new_row = []
  new_row.append([Fraction(n+1), -frac(tableau[cut_row][0][1])])
  for column in range(1, n+1):
    new_row.append(-frac(tableau[cut_row][column]))
  new_row.append(Fraction(1))
  tableau.append(new_row)
  return None

def fractional_dual_simplex(tableau, variables):
  m = len(tableau)-1
  n = len(tableau[0])-1
  primal_simplex(tableau, n,m)
  integer = False
  while not integer:
    integer = True
    for row in range(1, m+1):
      if tableau[row][0][0] <= variables and not check_integer(tableau[row][0][1]):
        integer = False
        if not check_integer(tableau[0][0][1]):
          generate_cut(tableau, 0, n, m)
        else:
          generate_cut(tableau, row, n, m)
        n += 1
        m +=1
        dual_simplex(tableau, n, m)
        break
  return tableau


def tableau_switch(tableau, n, m):
  tableau.pop(1)
  for row in range(m+1):
    del tableau[row][1:m+1]
  return tableau

def tableau_setup(A, b, c, n, m):
  reversed = [1 for x in range(m)]
  for row in range(m):
    if b[row] < 0:
      b[row] *= -1
      reversed[row] = -1
      for column in range(n):
        A[row][column] *= -1
  tableau = []
  cost_row = [[Fraction(0),Fraction(0)]]
  for column in range(m):
    cost_row.append(Fraction(0))
  for column in range(n):
    cost_row.append(Fraction(c[column]))
  for column in range(m):
    cost_row.append(Fraction(0))
  tableau.append(cost_row)
  auxillary_row = [[Fraction(0), Fraction(0)]]
  for column in range(m):
    auxillary_row.append(Fraction(1))
  for column in range(n+m):
    auxillary_row.append(Fraction(0))
  tableau.append(auxillary_row)
  for row in range(1, m+1):
    tableau_row = []
    tableau_row.append([Fraction(-row), Fraction(b[row-1])])
    for column in range(1, m+1):
      if column == row:
        tableau_row.append(Fraction(1))
      else:
        tableau_row.append(Fraction(0))
    for column in range(n):
      tableau_row.append(Fraction(A[row-1][column]))
    for column in range(1, m+1):
      if column == row:
        tableau_row.append(Fraction(reversed[column-1]))
      else:
        tableau_row.append(Fraction(0))
    tableau.append(tableau_row)
  for row in range(2, m+2):
    tableau[1][0][1]-= tableau[row][0][1]
    for column in range(1, n+2*m+1):
      tableau[1][column] -= tableau[row][column]
  return tableau

def auxillary_simplex(tableau, n, m):
  optimal = False
  while not optimal:
    optimal = True
    for column in range(1, n+1):
      if tableau[1][column] < 0:
        optimal = False
        auxillary_simplex_iteration(tableau, n, m, column)
        break
  artificial = True
  while artificial:
    artificial = False
    for row in range(2, m+2):
      if tableau[row][0][0] < 0:
        artificial = True
        assert(tableau[row][0][1] == 0)
        for column in range(1, n):
          if tableau[row][column] !=0:
            auxillary_pivot(tableau, row, column, n, m)
            break
        break
  return tableau

def auxillary_simplex_iteration(tableau, n, m, pivot_column):
  minimum = -1
  pivot_row = -1
  for row in range(2, m+2):
    if tableau[row][pivot_column]<=0:
      continue
    if tableau[row][0][1]/tableau[row][pivot_column] < minimum or minimum == -1:
      minimum = tableau[row][0][1]/tableau[row][pivot_column]
      pivot_row = row
  auxillary_pivot(tableau, pivot_row, pivot_column, n, m)
  return

def auxillary_pivot(tableau, pivot_row, pivot_column, n, m):
  factor = tableau[pivot_row][pivot_column]
  if pivot_column <= m:
      tableau[pivot_row][0][0] = -pivot_column
  else:
      tableau[pivot_row][0][0] = pivot_column-m
  tableau[pivot_row][0][1] /= tableau[pivot_row][pivot_column]
  for column in range(1, n+1):
    tableau[pivot_row][column] /= factor
  for row in range(m+2):
    if row == pivot_row:
      continue
    factor = tableau[row][pivot_column]
    tableau[row][0][1] -= factor* tableau[pivot_row][0][1]
    for column in range(1, n+1):
      tableau[row][column] -= factor * tableau[pivot_row][column]
  return

def primal_simplex(tableau, n, m):
  optimal = False
  while not optimal:
    optimal = True
    for column in range(1, n+1):
      if tableau[0][column] < 0:
        optimal = False
        primal_simplex_iteration(tableau, n, m, column)
        break
  return tableau

def primal_simplex_iteration(tableau, n, m, pivot_column):
  minimum = -1
  pivot_row = -1
  for row in range(1, m+1):
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
      if tableau[row][0][1] < 0:
        feasible = False
        dual_simplex_iteration(tableau, row, n, m)
  return tableau

def dual_simplex_iteration(tableau, pivot_row, n, m):
  minimum = -1
  pivot_column = -1
  for column in range(1, n+1):
    if tableau[pivot_row][column] >= 0:
      continue
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


print(gomory("input3.txt"))