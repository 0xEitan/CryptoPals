from Crypto.Cipher import AES


def ecb_encrypt(block, key):
    aes = AES.new(key, mode=AES.MODE_ECB)
    return aes.encrypt(block)


def ecb_decrypt(block, key):
    aes = AES.new(key, mode=AES.MODE_ECB)
    return aes.decrypt(block)


def combine_blocks(b1, b2):
    return ''.join(chr(ord(c[0]) ^ ord(c[1])) for c in zip(b1, b2))


def iter_blocks(data, size):
    assert len(data) % size == 0

    for i in xrange(len(data) / size):
        yield data[i*size:(i+1)*size]


def cbc_encrypt(plaintext, iv, key):
    ciphertext = ''
    prev = iv
    for block in iter_blocks(plaintext, 16):
        prev = ecb_encrypt(combine_blocks(block, prev), key)
        ciphertext += prev

    return ciphertext


def cbc_decrypt(ciphertext, iv, key):
    plaintext = ''
    prev = iv
    for block in iter_blocks(ciphertext, 16):
        plaintext += combine_blocks(ecb_decrypt(block, key), prev)
        prev = block

    return plaintext


def main(ciphertext):
    key = 'YELLOW SUBMARINE'
    iv = '\x00' * 16

    plain1 = cbc_decrypt(ciphertext, iv, key)
    plain2 = AES.new(key, mode=AES.MODE_CBC, IV=iv).decrypt(ciphertext)

    # prove encryption and decryption actually
    assert plain1 == plain2
    assert ciphertext == cbc_encrypt(plain2, iv, key)

    return plain1


if __name__ == '__main__':
    with open('10.txt', 'r') as f:
        data = f.read()

    print main(data.decode('base64'))
