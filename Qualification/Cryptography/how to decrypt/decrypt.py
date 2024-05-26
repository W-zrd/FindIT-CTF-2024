def caesar_decrypt(ciphertext):
    plaintext = ""
    for char in ciphertext:
        if char.isalpha():
            ascii_offset = ord('A') if char.isupper() else ord('a')
            decrypted_char = chr((ord(char) - ascii_offset - 4) % 26 + ascii_offset)
            plaintext += decrypted_char
        else:
            plaintext += char
    return plaintext

encrypted_flag = "JmrhMXGXJ{al4x_h03w_G43w4v_Hs_57lnkrzh8x5}"
decrypted_flag = caesar_decrypt(encrypted_flag)
print(decrypted_flag)
