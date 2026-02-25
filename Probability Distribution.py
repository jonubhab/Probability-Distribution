import matplotlib.pyplot as plt
from scipy.special import assoc_laguerre as lag
from scipy.special import assoc_legendre_p as leg
import tkinter as tk
from tkinter import messagebox
import numpy as np
import sys
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

# --- Suggestion Data ---
SUGGESTIONS = {

    "1D box": """#Particle in a 1-D box
    #Set Lx=Ly=0
    if abs(x)<=dx/2 and abs(y)<=dx/2 and 0<=z<=Lz:
        psi=np.sin(n*np.pi*z/Lz)
    else: psi=0""",

    "2D box": """#Particle in a 2-D box
    #Set Lz=0
    if abs(z)<=dx/2 and 0<=x<=Lx and 0<=y<=Ly:
        psi=np.sin(n*np.pi*x/Lx)*np.sin(l*np.pi*y/Ly)
    else: psi=0""",

    "3D Box": """#Particle in a 3-D box
    if 0<=x<=Lx and 0<=y<=Ly and 0<=z<=Lz:
        psi=np.sin(n*np.pi*x/Lx)*np.sin(l*np.pi*y/Ly)*np.sin(m*np.pi*z/Lz)
    else: psi=0""",

    "Ring": """#Particle in a Ring
    R=max(Lx,Ly) #Set Lz=0
    if abs(r-R)<=dx/2: 
        psi=np.cos(m*phi)
    else: psi=0""",

    "Sphere": """#Particle in a Sphere
    R=max(Lx,Ly,Lz)
    if abs(r-R)<=dx/2: 
        psi=np.cos(m*phi)*leg(l, m, np.cos(theta))[0]
    else: psi=0""",

    "Hydrogen Atom": """#Electron in a Hydrogen Atom
    psi = lag(2*r/n, n-l-1, 2*l+1) * np.exp(-r/n) * np.cos(m*phi) * leg(l, m, np.cos(theta))[0]"""
}

def copy_to_text(code):
    """Clears the text box and inserts the suggestion."""
    psi_text.delete("1.0", tk.END)
    psi_text.insert("1.0", f"    {code}")

# --- GUI Setup ---
root = tk.Tk()
root.title("Probability Distribution ~ ASen")

def on_toggle():
    """Changes the color of the polar coordinate display based on checkbox state."""
    if polar_var.get():
        polar_display.config(fg="black")  # Active color
    else:
        polar_display.config(fg="#a0a0a0")  # Faded gray color

def get_inputs():
    global n, l, m, Lx, Ly, Lz, dx, f, canvas_frame, user_psi_logic,N
    try:
        # 1. Retrieve Numeric Inputs
        n, l, m, N = int(entry_n.get()), int(entry_l.get()), int(entry_m.get()), int(entry_N.get())
        Lx, Ly, Lz,  dx = float(entry_Lx.get()), float(entry_Ly.get()), float(entry_Lz.get()), float(entry_dx.get())

        # 2. Build the function string based on the UI state
        user_psi_logic = psi_text.get("1.0", tk.END).strip()

        code_lines = [
            "def f(p):",
            "    x, y, z = p[0], p[1], p[2]"
        ]

        if polar_var.get():
            code_lines.extend([
                "    phi = np.atan2(y, x)",
                "    theta = np.atan2((x**2 + y**2)**0.5, z)",
                "    r = (x**2 + y**2 + z**2)**0.5"
            ])

        code_lines.append(f"    {user_psi_logic}")
        code_lines.append("    return psi")

        full_code = "\n".join(code_lines)

        # 3. Execute and replace function f
        local_env = {
            'np': np,
            'lag': lag,
            'leg': leg,
            'n': n, 'l': l, 'm': m, 'N': N, # Pass the current quantum numbers into the scope
            'dx':dx, 'Lx':Lx, 'Ly':Ly, 'Lz':Lz
        }
        # Note: Add your actual 'lag' and 'leg' functions to this dictionary
        exec(full_code, local_env)
        f = local_env['f']

        for widget in root.winfo_children():
            widget.destroy()  # Clear all input fields

        root.title("Probability Distribution ~ ASen")
        root.geometry("1000x1400")
        console_text = tk.Text(root, bg="white", fg="black", height=10, font=("Consolas", 10))
        console_text.pack(expand=True, fill=tk.BOTH, padx=10, pady=10)

        # Bottom half: Plot Area
        canvas_frame = tk.Frame(root, bg="white")
        canvas_frame.pack(expand=True, fill=tk.BOTH, padx=10, pady=5)

        # This allows print() to show up in the text box
        class Redirector:
            def write(self, s):
                console_text.insert(tk.END, s)
                console_text.see(tk.END)
                root.update()

            def flush(self): pass

        sys.stdout = Redirector()

        # Stop the mainloop so the rest of your script (the math) can run
        root.quit()

    except Exception as e:
        messagebox.showerror("Code Error", f"There is an error in your psi expression:\n\n{e}")

def on_closing():
    """Forcefully stops the entire script when the window is closed."""
    root.destroy()
    sys.exit()

root.protocol("WM_DELETE_WINDOW", on_closing)

# Create a Main Container to hold Left and Right columns
main_container = tk.Frame(root)
main_container.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)

# --- LEFT COLUMN (Inputs) ---
left_col = tk.Frame(main_container)
left_col.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=(0, 10))

fields = [
    ("Principal Quantum Number (n):", "3"),
    ("Azimuthal Quantum Number (l):", "2"),
    ("Magnetic Quantum Number (m):", "0"),
    ("Number of particles (N):", "5000"),
    ("Range of X-axis (Lx):", "10"),
    ("Range of Y-axis (Lx):", "10"),
    ("Range of Z-axis (Lx):", "10"),
    ("Resolution (dx):", "0.25")
]
entries = []
for label_text, default_val in fields:
    row = tk.Frame(left_col);
    row.pack(fill=tk.X, padx=10, pady=2)
    tk.Label(row, text=label_text, width=30).pack(side=tk.LEFT)
    ent = tk.Entry(row);
    ent.insert(0, default_val);
    ent.pack(side=tk.RIGHT, expand=True, fill=tk.X)
    entries.append(ent)
entry_n, entry_l, entry_m, entry_N, entry_Lx, entry_Ly, entry_Lz, entry_dx = entries

tk.Label(left_col, text="Define your wave function f(p) here:", font=('Arial', 10, 'bold')).pack(pady=(10, 0))



# --- Code Interface (The "Stitched" Look) ---
# Header
tk.Label(left_col, text="def f(p):\n    x, y, z = p[0], p[1], p[2]\n",
         anchor="w", justify="left", font=("Consolas", 10), fg="black").pack(fill=tk.X, padx=20)

# --- Coordinate Control ---
polar_var = tk.BooleanVar(value=True)
tk.Checkbutton(
    left_col,
    text="   #Use Polar Coordinates (Uncheck for cartesian coordinates)",
    variable=polar_var,
    command=on_toggle,
    anchor='w'
).pack(fill=tk.X, padx=20)

# The Polar Block (Color changes based on checkbox)
polar_code_text = """    # Transforming to polar coordinates 
    phi = np.atan2(y, x)
    theta = np.atan2((x**2 + y**2)**0.5, z)
    r = (x**2 + y**2 + z**2)**0.5"""

polar_display = tk.Label(left_col, text=polar_code_text, anchor="w", justify="left",
                         font=("Consolas", 10), fg="black")
polar_display.pack(fill=tk.X, padx=20)

# Editable Section
tk.Label(root, text="         #Define your psi here (Add constraints for your model):", font=("Arial", 9, "italic")).pack(anchor="w", padx=20, pady=(10, 0))
psi_text = tk.Text(root, height=5, width=100, font=("Consolas", 10), wrap=tk.NONE)
psi_text.insert("1.0", """    #Default function set for Hydrogen Atom Orbitals
    psi = lag(2*r/n, n-l-1, 2*l+1) * np.exp(-r/n) * np.cos(m*phi) * leg(l, m, np.cos(theta))[0]""")
psi_text.pack(padx=20, pady=5)

# Footer
tk.Label(root, text="    return psi", anchor="w", font=("Consolas", 10), fg="black").pack(fill=tk.X, padx=20)

tk.Button(root, text="PROCEED", command=get_inputs, bg="#4CAF50", fg="white", font=("Arial", 10, "bold")).pack(
    pady=15)

# --- RIGHT COLUMN (Suggestions) ---
right_col = tk.LabelFrame(main_container, text=" Quick Suggestions ", padx=10, pady=10)
right_col.pack(side=tk.RIGHT, fill=tk.Y)

tk.Label(right_col, text="\nYou may choose from any\n of the standard models,\nor define your own model.\nin the text box below.\n"
                         "\nClick a button to paste\nthe model to the editor:\n",
         font=("Arial", 9, "italic"), justify=tk.LEFT).pack(pady=(0,10))

for name, code in SUGGESTIONS.items():
    btn = tk.Button(right_col, text=name, width=20, anchor="w",
                    command=lambda c=code: copy_to_text(c))
    btn.pack(pady=2, fill=tk.X)

root.mainloop()

try:
    print(f"Inputs Received: n={n}, l={l}, m={m}\n"
          f"                 Lx={Lx}, Ly={Ly}, Lz={Lz}\n"
          f"                 N={N}, dx={dx}")
    print(f"Logic for wave function received:\n    {user_psi_logic}\n")

except NameError:
    print("Window was closed without submitting.")

def display_plot(fig):
    """Call this function instead of plt.show()"""
    canvas = FigureCanvasTkAgg(fig, master=canvas_frame)
    canvas.draw()
    canvas.get_tk_widget().pack(side=tk.TOP, fill=tk.BOTH, expand=1)
    root.update()

'''
def f(p):
    x=p[0]
    y=p[1]
    z=p[2]
    phi = np.atan2(y, x)
    theta=np.atan2((x**2 + y**2)**0.5,z)
    r=(x**2 + y**2 + z**2)**0.5

    #Define psi here
    return lag(2*r/n,n-l-1,2*l+1)*np.exp(-r/n)*np.cos(m*phi)*leg(l,m,np.cos(theta))[0]
'''


def c(x):
    return np.where(np.sign(x) == 1, 'b', 'r')


def P(x):
    return x ** 2


def seq(f, a, b, c):
    ele=[]
    prob=[]
    print("Identifying the Space...")
    for i in np.arange(-a - 2 * dx, a + 3 * dx, dx):
        for j in np.arange(-b - 2 * dx, b + 3 * dx, dx):
            for k in np.arange(-c - 2 * dx, c + 3 * dx, dx):
                p=f([i,j,k])
                if p!=0:
                    ele.append(f"{i} {j} {k}")
                    prob.append(p**2)
    prob=np.array(prob)
    prob /= np.sum(prob)
    print("Analyzing Probability Density...")
    seq = np.random.choice(ele, size=N, p=prob)
    seq = np.array(list(map(lambda str: list(map(float, str.split())), seq)))
    print("Throwing electrons...")
    return seq

a=(0.24-0.23*np.exp(-1.17*((Lx+Ly+Lz)/max(Lx,Ly,Lz)-1)))*(np.log(5000)/np.log(N))**10
if a>1: a=1
#1-np.exp(-((Lx+Ly+Lz)/dx)/(N**(4-((Lx+Ly+Lz)/max(Lx,Ly,Lz))**2))*8)*0.99
p = seq(f, Lx, Ly, Lz)
c = c(list(map(f, p)))

x, y, z = zip(*p.tolist())

fig = plt.figure()
ax = fig.add_subplot(111, projection='3d')
ax.scatter(x, y, z, c=c, s=200*dx/max((Lx+dx),(Ly+dx),(Lz+dx)), alpha=a)
print("Plotted the data...")
print("Blue: Phase is positive.\nRed: Phase is negative.")
ax.set_xlabel('X')
ax.set_ylabel('Y')
ax.set_zlabel('Z')
ax.set_aspect('equal')
display_plot(fig)
root.mainloop()