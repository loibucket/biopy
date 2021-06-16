import os
import pathlib
from shutil import copyfile

files = [f for f in os.listdir('.')]
files.sort()
with open('__init__.py', 'w') as initpy:
    for f in files:
        if ".py" in f and "__" not in f:
            initpy.write("from ." + f[:-3] + " import *\n")

for f in files:
    if ".py" in f:
        src = os.path.join(pathlib.Path(__file__).parent.absolute(),f)
        dst = os.path.join(pathlib.Path(__file__).parent.absolute(),"biopy",f)
        copyfile(src, dst)

