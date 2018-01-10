from cx_Freeze import setup, Executable

# On appelle la fonction setup
setup(
    name = "Dofuk",
    version = "1",
    description = "Dofuk",
    executables = [Executable("Dofuk.py")],
)