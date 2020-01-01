import fileinput
from itertools import groupby
from operator import itemgetter
from check_alternations import main as check


def main(data):
    iterable = list(check(data))
    texts = sorted(iterable, key=lambda x: (x[0], x[2], x[6], x[8], x[4]))
    tags = ('', '', '', '', '')
    sents = []
    for keys, text in (groupby(texts, key=itemgetter(0, 2, 6, 8, 4))):
        if keys == tags:
            sents.extend([tokens[1::2] for tokens in text])
        else:
            if sents:
                results = []
                results.extend([tag for tag in tags])
                results.extend(sents)
                yield results
                
            tags = keys
            sents = [tokens[1::2] for tokens in text]


if __name__ == '__main__':
    texts = list(map(lambda x: x.strip().split('\t'), fileinput.input()))
    #  ['dataset', 'verb_loc', 'verb', 'noun_loc', 'noun', 'prep_loc', 'prep', 'sent_id', 'pattern']
    main(texts)
