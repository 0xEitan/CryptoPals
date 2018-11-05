import sys


def main(data, block_lengt):
    if len(data) >= block_length:
        return data

    pad = block_length - len(data)
    pad_byte = chr(pad)

    return data + pad_byte * pad

if __name__ == '__main__':
    data = 'YELLOW SUBMARINE'
    block_length = 20

    if len(sys.argv) == 3:
        data = sys.argv[1]
        block_length = int(sys.argv[2])

    padded = main(data, block_length)
    pad_hex = padded[len(data):].encode('hex')
    print data + pad_hex
