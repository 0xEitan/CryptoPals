import os
import sys
import base64
import string

from Crypto.Cipher import AES


KEY_SIZE = 16
KEY = os.urandom(KEY_SIZE)
EXTRA = base64.b64decode('Um9sbGluJyBpbiBteSA1LjAKV2l0aCBteSByYWctdG9wIGRvd24gc28gbXkgaGFpciBjYW4gYmxvdwpUaGUgZ2lybGllcyBvbiBzdGFuZGJ5IHdhdmluZyBqdXN0IHRvIHNheSBoaQpEaWQgeW91IHN0b3A/IE5vLCBJIGp1c3QgZHJvdmUgYnkK')
print 'len(EXTRA)', len(EXTRA)

############### encryption oracle # start ###############
def ecb_encrypt(data, key):
    aes = AES.new(key, AES.MODE_ECB)
    return aes.encrypt(data)


def pad_pkcs7(data, block_size):
    pad_count = block_size - (len(data) % block_size)
    pad_byte = chr(pad_count)

    return data + pad_byte * pad_count


def oracle(plaintext):
    data = pad_pkcs7(plaintext + EXTRA, KEY_SIZE)
    return ecb_encrypt(data, KEY)
############### encryption oracle # end ###############


def discover_key_size():
    size1 = len(oracle(''))
    i = 1
    while True:
        size2 = len(oracle('A' * i))
        if size2 != size1:
            key_size = size2 - size1
            remainder = key_size - i
            return key_size, remainder
        i += 1


def is_oracle_using_ecb(key_size):
    enc = oracle('A' * key_size * 10)
    return enc[:key_size] == enc[key_size:key_size*2]


def calc_char(key_size, char_num, block_num, known):
    short = 'A' * (key_size - char_num)
    for char in string.printable:
        if oracle(short + known + char)[key_size*block_num:key_size*(block_num+1)] == \
                oracle(short)[key_size*block_num:key_size*(block_num+1)]:
            return char

    raise ValueError("No matching character")


def calc_char(i, key_size, found):
    short = 'A' * (key_size - (i % key_size + 1))
    block = i / key_size * key_size + key_size
    for char in string.printable:
        if oracle(short + found + char)[:block] == oracle(short)[:block]:
            return char

    raise ValueError("No matching character")


def decrypt_unknown_string():
    key_size, remainder = discover_key_size()
    unknown_length = (len(oracle('')) / key_size - 1) * key_size + remainder

    assert is_oracle_using_ecb(key_size)

    found = ''
    for i in range(unknown_length):
        found += calc_char(i, key_size, found)

    print found


if __name__ == '__main__':
    decrypt_unknown_string()
