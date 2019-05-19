# program asks for a name, than prints
#   "my name is {name}, my role is user"
# but since it uses ECB we can craft a name that will reveal to us
# how the message we want to be printed in encrypted, so we send
#   'eitan, my role is admin' + '\x0e' * 0xe
# as the name, then take the first 3 blocks at the input
# block 1 - my name is eitan
# block 2 - , my role is adm
# block 3 - in + pkc7 pad
# and so the final decrypted message is
#   my name is eitan, my role is admin

import os
from binascii import hexlify, unhexlify
from Crypto.Cipher import AES



def pad_pkcs7(data):
    mod = (len(data) % AES.block_size)
    if mod == 0:
        return data

    pad_count = AES.block_size - mod
    pad_byte = chr(pad_count)

    return data + pad_byte * pad_count


def main(key):
    aes = AES.new(key, AES.MODE_ECB)

    name = raw_input("enter plain name to encrypt... ")
    plain = "my name is {0}, my role is user".format(name)
    enc = aes.encrypt(pad_pkcs7(plain))
    blocks = " ".join([hexlify(enc[i*AES.block_size:(i+1)*AES.block_size]) for i in range(len(enc) / AES.block_size)])
    print("{0!r} encrpyted is {1!r}".format(plain, blocks))

    cipher = raw_input("enter cipher name to decrypt... ")
    dec = aes.decrypt(unhexlify(cipher))
    print("decrypted: {!r}".format(dec))


if __name__ == '__main__':
    key = os.urandom(16)
    main(key)
