import fileinput


def get_noun(iterable):
    n_pnv = set()
    n_vn = set()
    for _, _, _, _, noun, _, _, _, pattern in iterable:
        if pattern == 'pnv':
            n_pnv.add(noun)
        else:
            n_vn.add(noun)
    return n_pnv, n_vn


def main(iterable):
    n_pnv, n_vn = get_noun(iterable)
    for tokens in iterable:
        _, _, _, _, noun, _, _, _, pattern = tokens
        if pattern == 'pnv' and noun in n_vn:
            yield tokens
        elif pattern == 'vn' and noun in n_pnv:
            yield tokens
            

if __name__ == '__main__':
    iterable = list(map(lambda x: x.strip().split('\t'), fileinput.input()))
    #  ['dataset', 'vloc', 'verb', 'nloc', 'noun', 'ploc', 'prep', 'sent_id', 'pattern']
    main(iterable)

# python filter_patterns.py > filtered_data.txt
