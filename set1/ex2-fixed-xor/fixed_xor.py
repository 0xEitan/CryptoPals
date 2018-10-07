import sys


def main(str1, str2):
    raw1 = str1.decode('hex')
    raw2 = str2.decode('hex')
    l = len(raw1)

    xor = ''.join(chr(ord(raw1[i]) ^ ord(raw2[i])) for i in xrange(l))
    xor = xor.encode('hex')

    print 'xor-ing', str1
    print '...with', str2
    print 'result:', xor


if __name__ == '__main__':
    if len(sys.argv) != 3 or len(sys.argv[1]) != len(sys.argv[2]):
        print('usage: {0} str1 str2 (two equal-length hex-encoded strings)'.format(sys.argv[0]))
        sys.exit(1)

    main(sys.argv[1], sys.argv[2])
