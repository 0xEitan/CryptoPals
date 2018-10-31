from utils import break_single_char_xor


def hamming_distance(s1, s2):
    # returns number of differing bits

    assert len(s1) == len(s2)

    b1 = ''.join(format(ord(c), '08b') for c in s1)
    b2 = ''.join(format(ord(c), '08b') for c in s2)

    diff = 0
    for i in xrange(len(b1)):
        if b1[i] != b2[i]:
            diff += 1

    return diff


def find_edit_distance(ciphertext, keysize):
    # finds the edit distance between each consecutive pair of KEYSIZE bytes in ciphertext
    # and returns their average

    blocks = [ciphertext[i:i+keysize] for i in xrange(0, len(ciphertext), keysize)]
    if len(blocks[0]) != len(blocks[-1]):
        blocks.pop()

    distances = []
    prev = blocks[0]
    for curr in blocks[1:]:
        distances.append(hamming_distance(prev, curr))
        prev = curr

    return sum(distances) / len(distances)


def find_best_keysize(ciphertext):
    # finds the keysize with the smallest edit distance

    sizes = []
    for keysize in range(2, 40):
        sizes.append((find_edit_distance(ciphertext, keysize) / keysize, keysize))

    sizes.sort()
    return sizes[0][1]


def main(ciphertext):
    keysize = find_best_keysize(ciphertext)

    blocks = [ciphertext[i:i+keysize] for i in xrange(0, len(ciphertext), keysize)]

    transposed = ['' for i in xrange(keysize)]
    for i in xrange(keysize):
        for block in blocks:
            if i < len(block):
                transposed[i] += block[i]

    key = ''
    for block in transposed:
        _, k, _ = break_single_char_xor(block)
        if k > 0:
            key += chr(k)

    decrypted = ''
    for i, c in enumerate(ciphertext):
        k = key[i % len(key)]
        x = chr(ord(c) ^ ord(k))
        decrypted += x

    return key, decrypted


if __name__ == '__main__':
    ciphertext = open('6.txt', 'rb').read().decode('base64')
    key, decrypted = main(ciphertext)
    print key
    print decrypted
