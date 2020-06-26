import sys

if __name__ == '__main__':
    result = set()
    for line in sys.stdin:
        tokens = line.strip().split('|')
        score = float(tokens[2])
        metamap_id = tokens[4]
        locs = tokens[8].split(';')
        if score / len(locs) > 1:
            result.add(metamap_id)
    print(' '.join(sorted(result)))
