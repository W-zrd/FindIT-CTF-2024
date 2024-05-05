def bin2ascii(binary):
    flag = ""
    for b in binary.split():
        ascii = chr(int(b, 2))
        flag += ascii
    return flag

def decrypt():
    with open("flag.txt", "r") as f:
        file = f.read()

    binary = ""
    for character in file:
        digits = '1' if character == ' ' else '0'
        binary += digits

    binary = ' '.join([binary[i:i+8] for i in range(0, len(binary), 8)])
    return bin2ascii(binary)

flag = decrypt()
print("Flag:", flag)