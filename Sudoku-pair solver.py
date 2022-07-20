from pysat.card import *

def id_generator(i,j,l,n):#function to create ids for the non-zero elements of the input sudoku
    return (int)(i*n*n+j*n+l); 
cnf=CNF()
k=int(input("Enter the dimension of the sudoku: "))
file_name=input("Enter the name of the file along with .csv extension: ")
n=k**2
my_list=[]
assump=[]#list that will store all the assumptions that will be fed to the SAT solver
#exactly one number in each cell


 #checking condition for first sudoku
v=1
for i in range(1,n+1,1):
 for j in range(1,n+1,1):
     for l in range(1,n+1,1):
       my_list.append(v)
       v=v+1
     cnf.extend(CardEnc.equals(lits=my_list,encoding=EncType.pairwise))
     my_list=[]
 #checking condition for second sudoku
v=1
for i in range(1,n+1,1):
 for j in range(1,n+1,1):
     for l in range(1,n+1,1):
       my_list.append(v+n*n*n)
       v=v+1
     cnf.extend(CardEnc.equals(lits=my_list,encoding=EncType.pairwise))
     my_list=[]

#one number appears exactly once in every row
 #checking condition for first sudoku
for i in range(1,n+1,1):
    for l in range(1,n+1,1):
        for j in range(1,n+1,1):
            my_list.append((i-1)*n*n+(j-1)*n+l)
        cnf.extend(CardEnc.equals(lits=my_list,encoding=EncType.pairwise))
    
        my_list=[]
 
 
 #checking condition for second sudoku
for i in range(1,n+1,1):
    for l in range(1,n+1,1):
        for j in range(1,n+1,1):
            my_list.append(n*n*n+(i-1)*n*n+(j-1)*n+l)
        cnf.extend(CardEnc.equals(lits=my_list,encoding=EncType.pairwise))
    
        my_list=[]

#one number appears exactly once in every column
 #checking condition for first sudoku
for j in range(1,n+1,1):
    for l in range(1,n+1,1):
        for i in range(1,n+1,1):
            my_list.append((i-1)*n*n+(j-1)*n+l)
        cnf.extend(CardEnc.equals(lits=my_list,encoding=EncType.pairwise))
    
        my_list=[]            
 #checking condition for second sudoku
for j in range(1,n+1,1):
    for l in range(1,n+1,1):
        for i in range(1,n+1,1):
            my_list.append(n*n*n+(i-1)*n*n+(j-1)*n+l)
        cnf.extend(CardEnc.equals(lits=my_list,encoding=EncType.pairwise))
    
        my_list=[]          
#one number appears exactly once in every sub-group

 #checking condition for first sudoku
for l in range(1,n+1,1):
    for p in range(0,k,1):
        for q in range(0,k,1):
            for i in range(p*k+1,k*(p+1)+1,1):
               for j in range(q*k+1,(q+1)*k+1,1):
                 my_list.append((i-1)*n*n+(j-1)*n+l)
            
            cnf.extend(CardEnc.equals(lits=my_list,encoding=EncType.pairwise))
        
            my_list=[] 
 #checking condition for second sudoku              
for l in range(1,n+1,1):
    for p in range(0,k,1):
        for q in range(0,k,1):
            for i in range(p*k+1,k*(p+1)+1,1):
               for j in range(q*k+1,(q+1)*k+1,1):
                 my_list.append(n*n*n+(i-1)*n*n+(j-1)*n+l)
            
            cnf.extend(CardEnc.equals(lits=my_list,encoding=EncType.pairwise))
        
            my_list=[]   
#corresponding elements are not equal
for i in range(1,n+1,1):
    for j in range(1,n+1,1):
        for l in range(1,n+1,1):
            cnf.append([-((i-1)*n*n+(j-1)*n+l),-(n*n*n+(i-1)*n*n+(j-1)*n+l)])

from numpy import genfromtxt
data=genfromtxt(file_name,delimiter=',',dtype=int)


count=0
for i in range(0,2*n,1):
    for j in range(0,n,1):
        if data[i][j]!=0:
           assump.append(id_generator(i,j,data[i][j],n))





from pysat.solvers import Solver
g = Solver(bootstrap_with=cnf.clauses)
if g.solve(assumptions= assump)==True:
    model=g.get_model()
    
    for i in range (0,2*n*n*n,1):
        if model[i]>0:
            if model[i]%n!=0:
              print(model[i]%n,end=" ")
            else:
                print(n,end=" ")
            count=count+1
            if count%n==0:
                print("\n")
if g.solve(assumptions= assump)==False:
    print("None")

