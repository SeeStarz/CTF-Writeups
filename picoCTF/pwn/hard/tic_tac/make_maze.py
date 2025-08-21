#!/bin/python3
import subprocess
import sys
import os

def run(args: str) -> str:
    return subprocess.run(args, shell=True, capture_output=True).stdout.decode()

def make_maze(exit_target: str, nchains: int, depth: int):
    run(f"ln -s {exit_target} exit")

    top = run("echo $PWD").strip()
    target = top+"/exit"
    for i in range(nchains):
        run(f"mkdir chains{i}")
        os.chdir(f"chains{i}")
        for j in range(depth):
            run(f"mkdir d")
            os.chdir("d")
        run(f"ln -s {target} lnk")
        target = run("echo $PWD").strip()
        os.chdir(top)

    run(f"ln -s {target} sentry")

if __name__ == "__main__":
    make_maze(sys.argv[1], int(sys.argv[2]), int(sys.argv[3]))
