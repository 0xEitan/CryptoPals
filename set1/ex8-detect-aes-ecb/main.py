def main():
    with open('8.txt', 'r') as f:
        d = f.read()

    for ciphertext in d.splitlines():
        blocks = [ciphertext[i*16:(i+1)*16] for i in range(len(ciphertext) / 16)]

        # the problem with ECB is that it is stateless and deterministic
        # the same 16 byte plaintext block will always produce the same 16 byte ciphertext
        if len(blocks) != len(set(blocks)):
            print 'found ciphertext encrypted with aes ecb:', ciphertext


if __name__ == '__main__':
    main()
