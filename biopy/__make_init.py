import os

files = [f for f in os.listdir('.')]
files.sort()
with open('__init__.py', 'w') as initpy:
    for f in files:
        if ".py" in f and "__" not in f:
            initpy.write("from ." + f[:-3] + " import *\n")
