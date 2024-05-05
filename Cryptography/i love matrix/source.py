import secrets

import numpy as np
import sympy as sp
from secret import FLAG


def enc1(message, key):
    return bytes([message[i] ^ key[i % len(key)] for i in range(len(message))])


def encryption1():
    enc1_list = []
    key = secrets.token_bytes(10)
    enc1_result = int(enc1(FLAG.encode(), key).hex(), 16)

    for _ in str(enc1_result):
        enc1_list.append(int(_))

    return enc1_list


def is_coprime(a, b):
    return sp.gcd(a, b) == 1


def generate_key(size):
    while True:
        matrix = np.random.randint(1, 100, size=(size, size))
        det = np.linalg.det(matrix)
        if det != 0 and det % 2 != 0 and det % 13 != 0:
            return matrix


def encryption2():
    enc2_key = generate_key(4)
    v, w = np.linalg.eig(enc2_key)
    np.savetxt("data/v.txt", v)
    np.savetxt("data/w.txt", w)

    temp = []
    enc2_list = []
    for _ in enc1_list:
        temp.append(_)
        if len(temp) == 4:
            matrix = np.array(temp).reshape(4, 1)
            enc2_list.append(matrix)
            temp = []

    enc2_result = []
    for _ in enc2_list:
        enc2_vec = np.dot(enc2_key, _)
        temp = enc2_vec % 26
        enc2_result.append(temp)
    return enc2_result


while True:
    enc1_list = encryption1()
    if len(enc1_list) % 4 == 0:
        break

enc2_result = encryption2()

i = 1
for _ in enc2_result:
    np.savetxt("data/encrypted_flag" + str(i) + ".txt", _)
    i += 1
