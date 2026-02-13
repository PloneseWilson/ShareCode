###ncat cs2107-ctfd-i.comp.nus.edu.sg 5003
from pwn import * # Import pwntools


ans = binascii.unhexlify("4353323130377b7768305f6e333364735f70616464316e675f7768336e5f7930755f683476335f6563627d0505050505")
print(ans)

r = remote("cs2107-ctfd-i.comp.nus.edu.sg", 5003)
'''
r.recvuntil(b"") 
r.sendline(b"")             
'''
r.interactive()
    

