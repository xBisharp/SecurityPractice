#!/usr/bin/env python3

from pwn import *

# The address you found in GDB (this is the address that was overwritten)
crash_address = 0x4012fb 

# Use cyclic_find to find the offset where the return address gets overwritten
offset = cyclic_find(crash_address)
print(f"The offset to the return address is: {offset}")
