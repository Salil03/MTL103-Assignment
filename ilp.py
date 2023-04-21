def gomory(filename):
  x=1
  # Take input from file "filename"
  return x # an array of n integers
def simplex(A,b,c,n,m,t):
  if t==0:
    #if tableau is not formed and we need to construct again
    #row n+1 will have reduced costs and negative of final costs, column m+n+1 will have B-1b and column m+n+2 will have the index of variable being used in the basis which starts from 0
    tableau=A
    for i in range(len(A)):
      for j in range(len(A)):
        if i==j:
          A[i].append(1)
        else:
          A[i].append(0)
      c.append(0)
    m=m+len(A)
    for i in range(len(A)):
      A[i].append(b[i])
      A[i].append(i+m-2)
    cost=0
    for i in range(n):
      cost+=A[i][m]*c[A[i][m+1]-1]
    c.append(-cost)
    c.append(0)
    A.append(c)
  #tableau is already fromed no need for re formation
  #iteration starts
  flag=True
  while flag:
    ctr=0
    for i in range(m):
      if A[n][i]<0:
        chk=Simp_iteration(A,i,n,m)
        if not(chk):
          return "-inf"
        ctr=1
        break
    if ctr==0:
      flag=False
  return A

def dual_simplex(A,b,c,n,m):
  return A

def Simp_iteration(A,i,n,m):
  l=[]
  for j in range(n):
    if A[j][i]>0:
      l.append((A[j][m]/A[j][i],j))
  if len(l)==0:
    return False
  t=min(l)[1]
  dum=A[t][i]
  for k in range(m+1):
    A[t][k]=A[t][k]/dum
  for j in range(n+1):
    if j!=t:
      dum2=A[j][i]
      for k in range(m+1):
        A[j][k]=A[j][k]-dum2*A[t][k]
  A[t][m+1]=i
  return True




#test case
A=[[1,2,3],[2,3,4],[5,6,8]]
n,m=3,3
b=[1,2,3]
c=[-1,-1,1]
print(simplex(A,b,c,n,m,0))