from Crypto.Cipher import AES


def main(encrypted, key):
    aes = AES.new(key, mode=AES.MODE_ECB)
    return aes.decrypt(encrypted)


if __name__ == '__main__':
    with open('7.txt', 'r') as f:
        encrypted = f.read().decode('base64')

    decrypted = main(encrypted, b'YELLOW SUBMARINE')
    print decrypted
