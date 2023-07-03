from ast import Lambda
from os import name
from time import perf_counter

def greedy_knapsack(ks,b,n):
    factors={} #współczynniki masy
    knapsack=[]
    suma=0
    masa=0
    for i in range(n):
        factors[str(i+1)]=float(int(ks[i+1][1])/int(ks[i+1][0]))
    factors=dict(sorted(factors.items(), key=lambda x:x[1], reverse=True)) 
    for i in range(n):
        factors[str(i+1)]=ks[i+1]
    for i in factors:
        if b>0:
            if factors[i][0]<=b:
                b=b-factors[i][0]
                suma=suma+factors[i][1]
                knapsack.append(factors[i][0])
    for i in knapsack:
        masa=masa+ks[i][0]
    return knapsack,suma,masa


def brute_force_knapsack(ks,b,n):
    x=1
    wx=[0 for i in range(pow(2,n)-1)]
    fx=[0 for i in range(pow(2,n)-1)]
    knapsack=[0 for i in range(pow(2,n)-1)]
    while(x<pow(2,n)-1):
        pom=bin(x)[2:].zfill(n)
        pom2=[] 
        for i in range(1,len(pom)+1):
            if pom[len(pom)-i]=='1':
                wx[x-1]=wx[x-1]+ks[i][0]
                fx[x-1]=fx[x-1]+ks[i][1]
                pom2.append(int(i))
        knapsack[x-1]=pom2        
        x=x+1
    max_fx=0
    res_knapsack=[]
    res_wx=0
    pom3=[]
    for i in range(1,len(pom)+1):
        wx[pow(2,n)-2]=wx[pow(2,n)-2]+ks[i][0]
        fx[pow(2,n)-2]=fx[pow(2,n)-2]+ks[i][1]
        pom3.append(i)
    knapsack[pow(2,n)-2]=pom3
    for i in range(pow(2,n)-1):
        if fx[i]>max_fx:
            if wx[i]<=b:
                max_fx=fx[i]
                res_knapsack=knapsack[i]
                res_wx=wx[i]
    return res_knapsack,max_fx,res_wx

def dynamic_programming_knapsack(ks,b,n):
    tab=[[0 for i in range(b+1)] for i in range(n+1)]
    pom=[[0 for i in range(b+1)] for i in range(n+1)]
    res_w=0
    res_ks=[]
    res=0
    for i in range(1,n+1):
        for j in range(1,b+1):
            if(ks[i][0]>j):
                tab[i][j]=tab[i-1][j]
                pom[i][j]=0
            else:
                tmp1=tab[i-1][j]
                tmp2=tab[i-1][j-ks[i][0]]+ks[i][1]
                tab[i][j]=max(tmp1,tmp2)
                pom[i][j]=1
    j=b
    for i in range(n,0,-1):
        if(pom[i][j-1]==1):
            res_ks.append(i)
            j=j-ks[i][0]
    for i in res_ks:
        res_w=res_w+ks[i][0]
    res_ks.reverse()    
    return res_ks,tab[n][b],res_w

inputMethod: int = 0
while True:
	print( '\033cWczytaj dane:' )
	print( '1. Z klawiatury' )
	print( '2. Z pliku' )
	try:
		inputMethod = int( input( '>' ) )
		if inputMethod == 1 or inputMethod == 2:
			break
	except ValueError:
		pass
print( '\033c', end='' )

if inputMethod==1:
    while True:
        try:
            n, b = int(input("Liczba przedmiotów: ")), int(input('Pojemność plecaka: '))
            break
        except ValueError:
            pass
    n=int(n)
    b=int(b)
    ks={} #pusty plecak
    for i in range(n):
        while True:
            try:
                r,w= int(input(f"Podaj rozmiar {i+1} przedmiotu: ")), int(input(f'Podaj wartość {i+1} przedmiotu: '))
                break
            except ValueError:
                pass
        pom=[]
        pom.append(int(r))  #[0] na rozmiar, [1] na wartość
        pom.append(int(w))
        ks[i+1]=pom #id przedmiotu
    print( '\033c', end='' )

if inputMethod==2:
        file=open('file.txt')
        data=list(map(str.strip,file.readlines()))
        data=[x.replace(' ','') for x in data]
        n,b=data[0]
        ks={}
        n=int(n)
        b=int(b)
        for i in range(1,n+1):
            pom=[]
            r=data[i][0]
            w=data[i][1]
            pom.append(int(r))
            pom.append(int(w))
            ks[i]=pom
        
inputMethod=0
while True:
    print ('1. Algortym zachłanny')
    print ('2. Brute-force')
    print ('3. Dynamic programming')
    try:
        inputMethod = int(input(' > '))
        if inputMethod==1 or inputMethod == 2 or inputMethod == 3:
            break
    except ValueError:
        pass
print('\033c', end=' ')

if inputMethod==1:
    start = perf_counter()
    bag,value,size=greedy_knapsack(ks,b,n)
    end = perf_counter()
    print('Wybrane przedmioty: ',bag)
    print('Wartość przedmiotów: ',value)  
    print('Sumaryczny rozmiar: ',size) 
    print(f'Czas: {round(( end - start ) * 1000000)} μs')
if inputMethod==2:
    start = perf_counter()
    bag,value,size=brute_force_knapsack(ks,b,n)
    end = perf_counter()
    print('Wybrane przedmioty: ',bag)
    print('Wartość przedmiotów: ',value)  
    print('Sumaryczny rozmiar: ',size) 
    print(f'Czas: {round(( end - start ) * 1000000)} μs')     
if inputMethod==3:
    start = perf_counter()
    bag,value,size=dynamic_programming_knapsack(ks,b,n)
    end = perf_counter()
    print('Wybrane przedmioty: ',bag)
    print('Wartość przedmiotów: ',value)  
    print('Sumaryczny rozmiar: ',size)    
    print(f'Czas: {round(( end - start ) * 1000000)} μs')    