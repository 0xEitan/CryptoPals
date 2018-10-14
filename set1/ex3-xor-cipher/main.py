import string


def score_english_sentence(s):
    # not the best way to score a sentencte
    # repeated 'E' will score the highest...
    # http://pi.math.cornell.edu/~mec/2003-2004/cryptography/subs/frequencies.html
    FREQUENCY = {
        'E': 12.02,
        'T': 9.10,
        'A': 8.12,
        'O': 7.68,
        'I': 7.31,
        'N': 6.95,
        'S': 6.28,
        'R': 6.02,
        'H': 5.92,
        'D': 4.32,
        'L': 3.98,
        'U': 2.88,
        'C': 2.71,
        'M': 2.61,
        'F': 2.30,
        'Y': 2.11,
        'W': 2.09,
        'G': 2.03,
        'P': 1.82,
        'B': 1.49,
        'V': 1.11,
        'K': 0.69,
        'X': 0.17,
        'Q': 0.11,
        'J': 0.10,
        'Z': 0.07,
    }

    # assume an english sentence has at least two words in it
    if ' ' not in s:
        return 0

    score = 0
    for word in s.split(' '):
        for letter in word:
            if letter.upper() in FREQUENCY:
                score += FREQUENCY.get(letter.upper(), 0)
    return score


def xor_string(s, key):
    return ''.join(chr(ord(s[i]) ^ key) for i in xrange(len(s)))


def main(xored):
    possibilities = dict()
    for key in xrange(0x100):
        decoded = xor_string(xored, key)
        if any(c not in string.printable for c in decoded):
            continue

        score = score_english_sentence(decoded)
        possibilities[score] = (key, decoded)

    best_score = max(possibilities)
    best_guess = possibilities[best_score]
    print "Best guess with score {0} and xor key {1}: {2}".format(best_score,
                                                                  best_guess[0],
                                                                  best_guess[1])


if __name__ == '__main__':
    xored = '1b37373331363f78151b7f2b783431333d78397828372d363c78373e783a393b3736'
    main(xored.decode('hex'))
