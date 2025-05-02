import sys, os, subprocess

scr = 'echo "Failed to find build script!"'
this = os.path.dirname(os.path.abspath(__file__))

if sys.platform != "win32":
    scr = os.path.abspath(f"{this}/scripts/build-{"mac" if sys.platform == "darwin" else "linux"}.sh")
else:
    scr = os.path.abspath(f"{this}\\scripts\\build-win.bat")

print(f"Running: {scr}")
subprocess.call([scr])