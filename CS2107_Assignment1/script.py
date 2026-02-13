###ncat cs2107-ctfd-i.comp.nus.edu.sg 5002
from pwn import * # Import pwntools

r = remote("cs2107-ctfd-i.comp.nus.edu.sg", 5002)

r.recvuntil(b"Today's magic number is: ")
s = r.recvline().strip().decode()
num = int(s)

r.recvuntil(b"4. Read flag") 
r.sendline(b"1")             

r.recvuntil(b"Enter username:") 
r.sendline(b"test")  

r.recvuntil(b"4. Read flag") 
r.sendline(b"2")             

r.recvuntil(b"Which user are you using?") 
r.sendline(b"test")    

r.recvuntil(b"Enter password") 
ans = (num + 20273) % 65793
r.sendline(str(ans).encode())

r.recvuntil(b"4. Read flag") 
r.sendline(b"4")
r.interactive()
    
