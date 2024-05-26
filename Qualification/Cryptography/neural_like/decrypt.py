import base64
from Crypto.Cipher import AES
from Crypto.Util.number import long_to_bytes

def chinese_remainder_theorem(ciphertexts, moduli):
    M = 1
    for m in moduli:
        M *= m
    
    result = 0
    for c, m in zip(ciphertexts, moduli):
        Mi = M // m
        Mi_inv = pow(Mi, -1, m)
        result += c * Mi * Mi_inv
    
    return result % M

def cube_root(n):
    lo = 0
    hi = n
    while lo < hi:
        mid = (lo + hi) // 2
        if mid ** 3 < n:
            lo = mid + 1
        else:
            hi = mid
    return lo

# Encrypted message
encrypted_message = "/mcZBbbHDypRP3bcgHnz4Uxx4ouLVLQ+SOJb0+3IR/aIMp7p+quFgANv+2rWaIxZfNg6pNQvIjRBEALWt2Ltog=="

# Initialization Vector (IV)
iv = base64.b64decode("MTQ5MDI0ODk3NjYyODY1Mw==")

# Ciphertexts
ciphertexts = [base64.b64decode(ct) for ct in [
    'ATMkxDJEm2v/c/lTq/5vwpDbEreqTO9TMPhJy2LdbQhz6TYBPpm5IJdYKTA4QSTMkpEFq710KQUPmQdKfIOAn3x7gDHKqz760YxZhiNhI+qa9sP3Jl5seeN1CwUk6D1T',
    'ATMkxDJEm2v/c/lTq/5vwpDbEreqTO9TMPhJy2LdbQhz6TYBPpm5IJdYKTA4QSTMkpEFq710KQUPmQdKfIOAn3x7gDHKqz760YxZhiNhI+qa9sP3Jl5seeN1CwUk6D1T',
    'ATMkxDJEm2v/c/lTq/5vwpDbEreqTO9TMPhJy2LdbQhz6TYBPpm5IJdYKTA4QSTMkpEFq710KQUPmQdKfIOAn3x7gDHKqz760YxZhiNhI+qa9sP3Jl5seeN1CwUk6D1T'
]]

# Public Keys
public_keys = [
    (3, 71133758437006038056326172091721299053609445980066813533097450396882000263183799198334958634674350750364337062526840438247431341987014528669429220686257714936583334363551142340079498956283087185959015797539142708931737856085159674190900999308444949727291116184742764329875860331877990032609387154336948007463),
    (3, 125941037778323291862181710137279566520507783337269181617438481976673153096352231005001269298590265483741776227907173891288068230359909790427621939632966925613197250042001429866919367235598617037223833210192706336684268168284412261695214574281327836845269118313635153767786284267264522161308296572085413709307),
    (3, 94367108756513647846862299793403299930242645546085334894581075152164127523540295475710466034627931299443141702561946726197412688973006421667952239462299564714317521701006495867745002883414985183756381904918340610167590875954520157144644993889898982254580024164794730076274449307240869151872616289417359703771)
]

# Extract moduli from public keys
moduli = [n for _, n in public_keys]

# Convert ciphertexts to integers
ciphertext_ints = [int.from_bytes(ct, byteorder='big') for ct in ciphertexts]

# Combine the ciphertexts using Chinese Remainder Theorem
combined_ciphertext = chinese_remainder_theorem(ciphertext_ints, moduli)

# Take the cube root of the combined ciphertext to get the AES key
aes_key = long_to_bytes(cube_root(combined_ciphertext))

# Decrypt the encrypted message using AES
cipher = AES.new(aes_key, AES.MODE_CBC, iv)
decrypted_message = cipher.decrypt(base64.b64decode(encrypted_message))

# Extract the flag from the decrypted message
flag = decrypted_message.decode('utf-8').strip().split("XXXXXXXXXXXX")[1]
print("Flag:", flag)