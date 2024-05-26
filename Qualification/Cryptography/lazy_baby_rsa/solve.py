#!/usr/bin/python3

from sympy.ntheory import discrete_log
from Crypto.Cipher import AES
from Crypto.Util.number import getPrime, long_to_bytes
from Crypto.Util.Padding import pad, unpad
from function import *
from base64 import b64decode
import hashlib

exec(open("output.txt").read())

def decode(p):
    n = 0
    while True:
        try:
            p = b64decode(p)
            n += 1
        except:
            break

    return p, n

p, x = decode(p)
g, y = decode(g)

p = int(p, 16)
g = int(g, 16)

a = discrete_log(p, A, g)
b = discrete_log(p, B, g)

C = pow(A, b, p)
assert C == pow(B, a, p)

key = hashlib.sha256(long_to_bytes(C)).digest()[:16]

iiv = pow(x, y)
iiv = modify_digit(iiv, rules)
iv = iiv.to_bytes(16, byteorder="little")

cipher = AES.new(key, AES.MODE_CBC, iv)
flag = cipher.decrypt(c)

print(unpad(flag, 16 ** 2))
# b'FindITCTF{1_4m_4_l4zy_b4by_4nd_1_4m_proud_of_1t}'