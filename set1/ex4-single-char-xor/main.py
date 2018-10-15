from utils import score_english_sentence, xor_string


ENCRYPTED_FILE = '4.txt'


def decode_line(line):
    possibilities = dict()

    for key in xrange(0x100):
        xored = xor_string(line, key)
        score = score_english_sentence(xored);
        possibilities[score] = (key, xored)

    best_score = max(possibilities)
    best_guess = possibilities[best_score]

    return best_score, best_guess[0], best_guess[1]


def main():
    with open(ENCRYPTED_FILE, 'r') as f:
        lines = f.read().splitlines()

    possibilities = dict()
    for index, line in enumerate(lines):
        score, key, decoded = decode_line(line.decode('hex'))
        possibilities.update({score: (index, key, decoded)})

    best_score = max(possibilities)
    best_guess = possibilities[best_score]
    print "Best guess at line {line} with score {score} and xor key {key}: {decoded}".format(
        line=best_guess[0],
        score=best_score,
        key=best_guess[1],
        decoded=best_guess[2])


if __name__ == '__main__':
    main()
