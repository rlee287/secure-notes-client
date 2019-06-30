#from PySide2.scripts.uic import main

from concurrent.futures import ThreadPoolExecutor
import glob
import subprocess
import sys

def uic_to_py(filename):
    filename_out=filename.replace(".ui",".py")
    print("{} => {}".format(filename,filename_out))
    command_run=["pyside2-uic","-o",filename_out,filename]
    subprocess.run(command_run)

if __name__=="__main__":
    with ThreadPoolExecutor() as pool:
        pool.map(uic_to_py,glob.glob("*.ui"))
