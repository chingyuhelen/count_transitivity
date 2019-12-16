from glob import glob
from check_conditions import find_patterns
from collections import namedtuple
from tqdm import tqdm
import string
import re

Token = namedtuple('Token', ['loc', 'word', 'head_loc', 'head', 'dep', 'ckip_pos'])


def parse_stan(stan, ckips):
    # ckip:[(word, pos), (word, pos), ...]
    # stan:['dep(word-loc, parent-loc)', ...]
    for token in stan.strip().split('\t'):
        dep, words = token.split('(', 1)
        word_loc, parent_loc = words[:-1].split(', ')
        word, loc = word_loc.rsplit('-', 1)
        parent, par_loc = parent_loc.rsplit('-', 1)
        yield Token(int(loc), word, int(par_loc), parent, dep, ckips[int(loc)-1][1])


def parse(ckip, stan):
    ckips = [tuple(token[:-1].rsplit('(', 1)) for token in ckip.split()]
    return ckip, list(parse_stan(stan, ckips))


def preprocess(texts):
    eng = tuple(string.ascii_lowercase)
    for i, line in enumerate(texts):
        line = line.strip()
        if line and not line.startswith(eng):
            yield parse(line, texts[i+1])


def main(filename):
    with open('../data/sents.txt', 'w') as f:
        sent_id = 0
        for filename, tag in tqdm(filenames):
            texts = open(filename).readlines()
            for ckip, stan in preprocess(texts):    # preprocess
                pnv, vn = find_patterns(stan)       # find [v, n, p] and [v, n, '']
                if pnv or vn:
                    sent_id += 1
                    print(sent_id, ckip, file=f)    # save sents & id including vn, or pnv
                if pnv:
                    for tokens in pnv:  # [vloc, v, nloc, n, ploc, p]
                        print(tag, *tokens, sent_id, 'pnv', sep='\t')
                if vn:
                    for tokens in vn:   # [vloc, v, nloc, n]
                        print(tag, *tokens, '', '', sent_id, 'vn', sep='\t')


if __name__ == '__main__':
    paths = ['/home/nlplab/jocelyn/cna_processed/headline/*',          
             '/home/nlplab/jocelyn/cna_processed/content/*',
             '/home/nlplab/jocelyn/ucd_processed/*']
    tags = ['cna_headline', 'cna_content', 'udn']
    filenames = [(filename, tag) for path, tag in zip(paths, tags) for filename in glob(path)]
    main(filenames)

# python find_patterns_map.py > patterns.txt
