from modexp import modexp
from long_multiplication import long_mul

# Extended Euclidean Algorithm
def egcd(a, b):
    if b == 0:
        return (a, 1, 0)
    g, x1, y1 = egcd(b, a % b)
    return (g, y1, x1 - (a // b) * y1)

# Modular inverse
def modinv(a, m):
    g, x, y = egcd(a, m)
    if g != 1:
        raise ValueError("No modular inverse: e and phi(n) not coprime")
    return x % m

# Encode string → integer (3-digit ASCII)
def message_to_int(msg):
    return int(''.join([f"{ord(c):03d}" for c in msg])) if msg else 0

# Decode integer → string (3-digit ASCII)
def int_to_message(m_int):
    s = str(m_int)
    if len(s) % 3 != 0:
        s = s.zfill(((len(s)//3)+1)*3)
    chars = [chr(int(s[i:i+3])) for i in range(0, len(s), 3)]
    return ''.join(chars).lstrip('\x00')

# Max characters per RSA block
def max_block_size_chars(n):
    if n <= 1:
        return 0
    return max(1, (len(str(n)) - 1)//3)

# Split message into blocks
def split_blocks(msg, k):
    return [msg[i:i+k] for i in range(0, len(msg), k)]

# RSA encryption with blocking
def rsa_encrypt_blocks(msg, e, n):
    k = max_block_size_chars(n)
    blocks = split_blocks(msg, k)
    cipher_blocks = []
    for blk in blocks:
        m_int = message_to_int(blk)
        if m_int >= n:
            while m_int >= n and k > 0:
                k -= 1
                blocks = split_blocks(msg, k)
                cipher_blocks = []
                for b in blocks:
                    ci = modexp(message_to_int(b), e, n)
                    cipher_blocks.append(ci)
                return cipher_blocks, k, blocks
        cipher_blocks.append(modexp(m_int, e, n))
    return cipher_blocks, k, blocks

# RSA decryption with blocking
def rsa_decrypt_blocks(cipher_blocks, d, n, block_char_size):
    plain = []
    for c in cipher_blocks:
        m_int = modexp(c, d, n)
        plain.append(int_to_message(m_int).rjust(block_char_size))
    return ''.join([p.strip() for p in plain])

# Demo
def demo(msg="HELLOWORLD"):
    p = 1000003
    q = 1000033
    n = p*q
    phi = (p-1)*(q-1)
    e = 65537
    d = modinv(e, phi)

    print(f"n = {n}")
    cipher_blocks, k_used, blocks = rsa_encrypt_blocks(msg, e, n)
    print("Block size:", k_used)
    print("Plain blocks:", blocks)
    print("Cipher blocks:", cipher_blocks)

    recovered = rsa_decrypt_blocks(cipher_blocks, d, n, k_used)
    print("Recovered:", recovered)

    return {
        "n":n, "e":e, "d":d,
        "blocks":blocks, "cipher":cipher_blocks, "recovered":recovered
    }

if __name__ == "__main__":
    print(demo("HELLOWORLD"))
