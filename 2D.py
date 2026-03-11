import numpy as np
import matplotlib.pyplot as plt
from functools import partial

nx=2
Lx=10
ny=10
Ly=1

def f(x,n,L):
    return (2/L)**0.5*np.sin(n*np.pi*x/L)

def c(x,y):
    t=x*y
    return np.where(np.sign(t)==1,'b','r')

def P(x):
    return x**2

def seq(f,a,b):
    ele=np.arange(a,b,0.001)
    prob=f(ele)**2*0.001
    seq = np.random.choice(ele, size=10000, p=prob)
    return seq

x=seq(partial(f,n=nx,L=Lx),0,Lx)
y=seq(partial(f,n=ny,L=Ly),0,Ly)
c=c(f(x,nx,Lx),f(y,ny,Ly))

plt.scatter(x, y,c=c,s=5,alpha=0.2)
plt.xlabel('X')
plt.ylabel('Y')
plt.axis('equal')
plt.show()