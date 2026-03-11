import numpy as np
import matplotlib.pyplot as plt
from functools import partial

nx=2
Lx=1
ny=3
Ly=3
nz=1
Lz=2

def f(x,n,L):
    return (2/L)**0.5*np.sin(n*np.pi*x/L)

def c(x,y,z):
    t=x*y*z
    return np.where(np.sign(t)==1,'b','r')

def P(x):
    return x**2

def seq(f,a,b):
    ele=np.arange(a,b,0.001)
    prob=f(ele)**2*0.001
    seq = np.random.choice(ele, size=5000, p=prob)
    return seq

x=seq(partial(f,n=nx,L=Lx),0,Lx)
y=seq(partial(f,n=ny,L=Ly),0,Ly)
z=seq(partial(f,n=nz,L=Lz),0,Lz)
c=c(f(x,nx,Lx),f(y,ny,Ly),f(z,nz,Lz))

fig = plt.figure()
ax = fig.add_subplot(111, projection='3d')
ax.scatter(x, y, z,c=c,s=5,alpha=0.2)
ax.set_xlabel('X')
ax.set_ylabel('Y')
ax.set_zlabel('Z')
ax.set_aspect('equal')
plt.show()