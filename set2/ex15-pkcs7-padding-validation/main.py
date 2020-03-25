VALID = ["ICE ICE BABY\x04\x04\x04\x04"]
INVALID = ["ICE ICE BABY\x05\x05\x05\x05", "ICE ICE BABY\x01\x02\x03\x04"]


def validate_pkcs7(s):
    pad_byte = s[-1]
    pad_count = ord(pad_byte)
    if s[-pad_count:] == pad_byte * pad_count:
        return True

    raise ValueError()


if __name__ == '__main__':
    for s in VALID:
        assert validate_pkcs7(s)

    for s in INVALID:
        invalid = False
        try:
            validate_pkcs7(s)
        except ValueError:
            invalid = True
        finally:
            assert invalid

    print('all good!')
