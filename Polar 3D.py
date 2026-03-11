import tkinter as tk
from tkinter import messagebox


def get_inputs():
    # Use global to ensure variables are accessible outside the function
    global n, l, m, L, dx

    try:
        # Retrieve and convert values from the entry fields
        n = int(entry_n.get())
        l = int(entry_l.get())
        m = int(entry_m.get())
        L = float(entry_L.get())
        dx = float(entry_dx.get())

        root.destroy()  # Close the window and resume code execution
    except ValueError:
        messagebox.showerror("Input Error",
                             "Please enter valid numbers.\n(n, l, m must be integers; L, dx must be decimals)")


# --- GUI Setup ---
root = tk.Tk()
root.title("Quantum Parameters")

# Define labels and default values
fields = [
    ("Principal Quantum Number (n):", "1"),
    ("Azimuthal Quantum Number (l):", "0"),
    ("Magnetic Quantum Number (m):", "0"),
    ("Size of cube (L):", "1.2"),
    ("Resolution (dx):", "0.05")
]

entries = []
for label_text, default_val in fields:
    row = tk.Frame(root)
    row.pack(side=tk.TOP, fill=tk.X, padx=10, pady=5)

    lbl = tk.Label(row, text=label_text, width=25, anchor='w')
    lbl.pack(side=tk.LEFT)

    ent = tk.Entry(row)
    ent.insert(0, default_val)  # Set default value
    ent.pack(side=tk.RIGHT, expand=tk.YES, fill=tk.X)
    entries.append(ent)

# Map entries to specific variables for the get_inputs function
entry_n, entry_l, entry_m, entry_L, entry_dx = entries

# Submit Button
btn = tk.Button(root, text="Submit", command=get_inputs, bg="#4CAF50", fg="white")
btn.pack(pady=10)

root.mainloop()

# --- Your Main Code Continues Here ---
print(f"Inputs Received: n={n}, l={l}, m={m}, L={L}, dx={dx}")

import numpy as np
import matplotlib.pyplot as plt
from functools import partial
from scipy.special import assoc_laguerre as lag
from scipy.special import assoc_legendre_p as leg
import math as math

def f(p):
    x=p[0]
    y=p[1]
    z=p[2]
    phi = np.atan2(y, x)
    theta=np.atan2((x**2 + y**2)**0.5,z)
    r=(x**2 + y**2 + z**2)**0.5

    #Define psi here
    return lag(2*r/n,n-l-1,2*l+1)*np.exp(-r/n)*np.cos(m*phi)*leg(l,m,np.cos(theta))[0]

def c(x):
    return np.where(np.sign(x)==1,'b','r')

def P(x):
    return x**2

def seq(f,a,b):
    ele=np.array([f"{i} {j} {k}" for i in np.arange(a-2*dx,b+3*dx,dx) for j in np.arange(a-2*dx,b+3*dx,dx) for k in np.arange(a-2*dx,b+3*dx,dx)])
    ele2=np.array(list(map(lambda str:list(map(float,str.split())),ele)))
    print("Identified the Space...")
    prob=np.array(list(map(f,ele2)))**2
    prob/=np.sum(prob)
    print("Analyzed Probability Density...")
    seq = np.random.choice(ele, size=5000, p=prob)
    seq=np.array(list(map(lambda str:list(map(float,str.split())),seq)))
    print("Observed electrons...")
    return seq

p=seq(f,-L,L)
c=c(list(map(f,p)))
print("Plotted the data...")

x,y,z=zip(*p.tolist())

fig = plt.figure()
ax = fig.add_subplot(111, projection='3d')
ax.scatter(x, y, z,c=c,s=5,alpha=0.2)
ax.set_xlabel('X')
ax.set_ylabel('Y')
ax.set_zlabel('Z')
ax.set_aspect('equal')
plt.show()
