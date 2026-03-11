import numpy as np
import matplotlib.pyplot as plt
from functools import partial
import random
random.seed(1)

n=10
L=1

def f(p,n,L):
    x=p[0]
    y=p[1]
    if 0 < x**2 + y**2 - L**2 < 0.01:
        phi = np.atan2(y, x)
        t=0
        for i in range(1,n+1):
            t+=random.random()*np.cos(i*phi)
        return t
    else: return 0

def c(x):
    return np.where(np.sign(x)==1,'b','r')

def P(x):
    return x**2

def seq(f,a,b):
    ele=np.array([f"{i} {j}" for i in np.arange(a-0.02,b+0.03,0.01) for j in np.arange(a-0.02,b+0.03,0.01)])
    ele2=np.array(list(map(lambda str:list(map(float,str.split())),ele)))
    prob=np.array(list(map(f,ele2)))**2
    prob/=np.sum(prob)
    seq = np.random.choice(ele, size=1000, p=prob)
    seq=np.array(list(map(lambda str:list(map(float,str.split())),seq)))
    return seq

p=seq(partial(f,n=n,L=L),-L,L)
random.seed(1)
c=c(list(map(partial(f,n=n,L=L),p)))

x,y=zip(*p.tolist())

plt.scatter(x,y,c=c,s=5,alpha=0.2)
plt.xlabel('X')
plt.ylabel('Y')
plt.axis('equal')
plt.show()
