def main(data, key):
    encrypted = []

    for i, c in enumerate(data):
        k = key[i % len(key)]
        x = chr(ord(c) ^ ord(k))
        encrypted.append(x)

    return ''.join(encrypted).encode('hex')


if __name__ == '__main__':
    data = ("Burning 'em, if you ain't quick and nimble\n"
            "I go crazy when I hear a cymbal")
    key = 'ICE'

    print main(data, key)
