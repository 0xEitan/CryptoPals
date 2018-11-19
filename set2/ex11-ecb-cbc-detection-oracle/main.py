import os
import random

from Crypto.Cipher import AES


KEY_SIZE = 16
PADDING_RANGE = [5, 10]
ECB = 'ECB'
CBC = 'CBC'


def random_key():
    return os.urandom(KEY_SIZE)


def random_iv():
    return random_key()


def random_padding():
    return os.urandom(random.randint(*PADDING_RANGE))


def encrypt_ecb(plaintext, key):
    aes = AES.new(key, mode=AES.MODE_ECB)
    return aes.encrypt(plaintext)


def encrypt_cbc(plaintext, key, iv):
    aes = AES.new(key, mode=AES.MODE_CBC, IV=iv)
    return aes.encrypt(plaintext)


def pad_pkcs7(data, block_size):
    pad_count = block_size - (len(data) % block_size)
    pad_byte = chr(pad_count)

    return data + pad_byte * pad_count


def encryption_oracle(plaintext):
    key = random_key()
    plaintext = random_padding() + plaintext + random_padding()
    plaintext = pad_pkcs7(plaintext, KEY_SIZE)

    if random.randint(0, 1):
        return ECB, encrypt_ecb(plaintext, key)
    else:
        return CBC, encrypt_cbc(plaintext, key, random_iv())


def detection_oracle(ciphertext):
    blocks = [ciphertext[i*KEY_SIZE:(i+1)*KEY_SIZE] for i in xrange(len(ciphertext) / KEY_SIZE)]

    if len(blocks) != len(set(blocks)):
        return ECB
    else:
        return CBC


def main(plaintext):
    mode, ciphertext = encryption_oracle(plaintext)
    detected_mode = detection_oracle(ciphertext)

    if mode != detected_mode:
        print "Detected {0} as {1} :(".format(mode, detected_mode)
    else:
        print "Successfully detected {0}".format(mode)


if __name__ == "__main__":
    plaintext = "It's over Anakin! I have the high ground" * 10
    main(plaintext)
