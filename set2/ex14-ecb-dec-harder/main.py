import os
import random
import string
import base64

from Crypto.Cipher import AES


################################ oracle ################################
KEY_SIZE = 16
KEY = os.urandom(KEY_SIZE)
TARGET_BYTES = base64.b64decode('Um9sbGluJyBpbiBteSA1LjAKV2l0aCBteSByYWctdG9wIGRvd24gc28gbXkgaGFpciBjYW4gYmxvdwpUaGUgZ2lybGllcyBvbiBzdGFuZGJ5IHdhdmluZyBqdXN0IHRvIHNheSBoaQpEaWQgeW91IHN0b3A/IE5vLCBJIGp1c3QgZHJvdmUgYnkK')
PREFIX = os.urandom(random.randint(1,255))


def ecb_encrypt(data, key):
    aes = AES.new(key, AES.MODE_ECB)
    return aes.encrypt(data)


def pad_pkcs7(data, block_size):
    pad_count = block_size - (len(data) % block_size)
    pad_byte = chr(pad_count)

    return data + pad_byte * pad_count


def oracle(plaintext):
    data = pad_pkcs7(PREFIX + plaintext + TARGET_BYTES, KEY_SIZE)
    return ecb_encrypt(data, KEY)
################################ oracle ################################


def discover_key_size(padding=0):
    """
    Say the block size is 8 bytes. Then encrypting any message shorter than 8, would result
    in an encrypted message of size 8.
    However, encrypting a message of size 9, would result in an encrypted chunk of size 16.

    By feeding the oracle one byte at a time, we can easily discover the block size, by subtracting
    the length of two encrypted message that differ by exactly 1 block :)

    If padding is the correct amount of bytes needed to pad len(PREFIX) to a block size,
    then the remainder is basically just len(TARGET_BYTES) % KEY_SIZE.
    """

    size1 = len(oracle('A' * padding))
    i = 1
    while True:
        size2 = len(oracle('A' * (padding + i)))
        if size2 != size1:
            key_size = size2 - size1
            remainder = key_size - i
            return key_size, remainder
        i += 1


def calc_oracle_ecb_params(key_size):
    """
    Generate a message that should produce several identical and continuous blocks at known offsets
    of the ciphertext, if and only if the oracle is using ECB.

    Returns whether or not the oracle uses ECB, and if so, also returns the offset at which a full
    block of user data begins, and the amount of data needed to pad the random prefix to a full
    block size.
    """

    count = 9
    enc = oracle('A' * key_size * (count + 1))

    # find the identical and countinuous blocks
    block = ''
    offset = 0
    # import ipdb; ipdb.set_trace()
    for i in range(0, len(enc), key_size):
        curr = enc[i:i+key_size]
        if all(curr == enc[(i+key_size*j):(i+key_size*(j+1))] for j in range(1, count)):
            block = curr
            offset = i
            break

    if block == '':
        return False, None, None

    i = 0
    while enc.count(block) >= 9:
        i += 1
        enc = oracle('A' * (key_size * (count + 1) - i))
    padding = key_size - i + 1

    return True, offset, padding


def calc_target_string_length(key_size, offset, padding):
    pass

def calc_char(i, key_size, known, padding, offset):
    """
    The final stretch.

    Say the key lenght is 8. Sending 'A' * 7 to the oracle would result in the encryption of
    'A' * 7 + the first byte of the target string.
    Matching that result to all possible results of sending the oracle 'A' * 7 + <random_byte>,
    would reveal the first byte of the data.

    Repeating this process by each time encrypting more and more bytes from target string reveals
    the entire string :)
    """

    pad = 'A' * padding
    prefix = 'A' * (key_size - (i % key_size + 1))
    block = i / key_size * key_size + key_size
    for char in string.printable:  # replace with range(256) for arbitrary data
        if oracle(pad + prefix + known + char)[offset:offset+block] \
                == oracle(pad + prefix)[offset:offset+block]:
            return char

    raise ValueError("No matching character from string.printable")


def decrypt_unknown_string():
    # remainder is incorrect, because we don't know the padding
    print('Attempting to decrypt...')

    key_size, _ = discover_key_size()
    print('\n[1] key size is {0}'.format(key_size))

    ecb, offset, padding = calc_oracle_ecb_params(key_size)
    assert ecb
    print('\n[2] encryption scheme is ecb.')
    print('[2] {0} bytes are needed to pad the random prefix to a block size.'.format(padding))
    print('[2] after padding, encrypted user data begins at offset {0}'.format(offset))

    # now we know the required padding, and can calculate the remainder
    _, remainder = discover_key_size(padding)

    # disregard the prefix+padding, calculate the length of the target string by calculating
    # the amount of blocks in its cipher (minus 1, the padded last block), plus the remainder.
    target_length = ((len(oracle('A' * padding)) - offset) / key_size - 1) * key_size + remainder
    print('\n[3] target string\'s lenght is {0}'.format(target_length))

    known = ''
    for i in range(target_length):
        known += calc_char(i, key_size, known, padding, offset)

    print('\n[4] finished decrypting. result:\n')
    print(known)


if __name__ == '__main__':
    decrypt_unknown_string()
