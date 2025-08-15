import sys
import itertools
from copy import deepcopy
from subprocess import run
from ast import literal_eval

def exit():
    sys.exit(0)

def scramble(L):
    A = L
    i = 2
    while (i < len(A)):
        A[i-2] += A.pop(i-1)
        A[i-1].append(A[:i-2])
        i += 1

    return L

def unfuck(A: list, i):
    while (i >= 2):
        A[i-1].pop()
        A.insert(i-1, [A[i-2].pop()])
        i -= 1

    return A

def get_flag():
    flag = open('flag.txt', 'r').read()
    flag = flag.strip()
    hex_flag = []
    for c in flag:
        hex_flag.append([str(hex(ord(c)))])

    return hex_flag

# def main():
#     flag = get_flag()
#     cypher = scramble(flag)
#     print(cypher)

def main():
    proc = run("nc verbal-sleep.picoctf.net 63779".split(), capture_output=True)
    result = literal_eval(proc.stdout.decode())

    # print(unfuck(deepcopy(result), len(result)))

    # This one is correct
    result = unfuck(deepcopy(result), len(result) - 1)
    print("".join(chr(int(x[0][2:], 16)) for x in result))

if __name__ == '__main__':
    main()
