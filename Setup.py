from cx_Freeze import setup, Executable


build_exe_options = {
    "packages": ["numpy", "matplotlib", "scipy", "tkinter", "PIL"],
    "excludes": [
        "pytest",
        "unittest",
        "email.test",
        "setuptools"
    ],
    "zip_include_packages": ["numpy", "scipy"],
    "zip_exclude_packages": ["tkinter", "matplotlib", "PIL"]
}




setup(
    name = "Probability Distribution",
    version = "1.0",
    description = "3D Plot",
    options = {"build_exe": build_exe_options},
    executables = [Executable("Probability Distribution.py", base="gui")]
)
