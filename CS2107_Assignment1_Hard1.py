###nc cs2107-ctfd-i.comp.nus.edu.sg 5001
from pwn import * # Import pwntools



r = remote("cs2107-ctfd-i.comp.nus.edu.sg", 5001)

r.recvuntil(b"Choice > ")
r.sendline(b"1") 

r.recvuntil(b"iv =")
IV = base64.b64decode(r.recvline().strip().decode())
iv = bytearray(IV)

r.recvuntil(b"ct =")
CT = base64.b64decode(r.recvline().strip().decode())
ct = bytearray(CT)




IV = ct[0:16] # change IV / 0~15 / 16~31
iv = bytearray(IV)

ans = bytearray(16)
fake_IV = bytearray(IV)




for target_idx in range(1, 17): #negative index -i
    fake_pad = 0x67 + target_idx

    fake_IV = bytearray(IV)
    for i in range(1, target_idx):
        fake_IV[-i] ^= (ans [-i] ^ fake_pad)

    for t in range(256):
        fake_IV[-target_idx] = iv[-target_idx] ^ t

        r.recvuntil(b"Choice > ")
        r.sendline(b"2") 
        r.recvuntil(b"iv in base64 > ")
        r.sendline(base64.b64encode(fake_IV)) 
        r.recvuntil(b"ct in base64 > ")
        r.sendline(base64.b64encode(ct[16:32])) # change 0~15 / 16~31 / 32~47

        res = r.recvline()
        print(t, res)
        if b"incorrect." in res:
            continue
        else:
            ans[-target_idx] = fake_pad ^ t
            print(target_idx, ":", ans[-target_idx])
            break

print(ans)

'''
r.recvuntil(b"") 
r.sendline(b"")             
'''

r.interactive()
    
