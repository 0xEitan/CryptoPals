import os
import urllib

from Crypto.Cipher import AES


PREFIX = "comment1=cooking%20MCs;userdata="
SUFFIX = ";comment2=%20like%20a%20pound%20of%20bacon"

KEY_SIZE = 16
KEY = os.urandom(KEY_SIZE)
IV = os.urandom(KEY_SIZE)


#################################################################
def encrypt_cbc(plaintext, key, iv):
    aes = AES.new(key, mode=AES.MODE_CBC, IV=iv)
    return aes.encrypt(plaintext)


def decrypt_cbc(ciphertext, key, iv):
    aes = AES.new(key, mode=AES.MODE_CBC, IV=iv)
    return aes.decrypt(ciphertext)


def pad_pkcs7(data, block_size):
    pad_count = block_size - (len(data) % block_size)
    pad_byte = chr(pad_count)

    return data + pad_byte * pad_count


def escape_data(data):
    return urllib.quote(data)


def build_plaintext(userdata):
    return escape_data(PREFIX + userdata + SUFFIX)


def oracle(userdata):
    return encrypt_cbc(pad_pkcs7(build_plaintext(userdata), KEY_SIZE), KEY, IV)


def validate(ciphertext):
    return ';admin=true;' in decrypt_cbc(ciphertext, KEY, IV)
#################################################################


def break_crypto():
    # pad the prefix to a block size
    pad = 'A' * (KEY_SIZE - (len(escape_data(PREFIX)) % KEY_SIZE))

    # the block of data we'll manipulate, can be any random data
    target_block = 'A' * KEY_SIZE
    target_block_offset = len(escape_data(PREFIX)) + len(pad)

    # ';' ^ 2 = '9'
    # '=' ^ 4 = '9'
    crafted_input = '9admin9true9'
    semicolon1_pos = 0
    eq_sign_pos = 6
    semicolon2_pos = 11

    ciphertext = bytearray(oracle(pad + target_block + crafted_input))

    ciphertext[target_block_offset + semicolon1_pos] ^= ord('9') ^ ord(';')
    ciphertext[target_block_offset + eq_sign_pos] ^= ord('9') ^ ord('=')
    ciphertext[target_block_offset + semicolon2_pos] ^= ord('9') ^ ord(';')

    print('validation result: {0}'.format(validate(str(ciphertext))))


if __name__ == '__main__':
    break_crypto()
