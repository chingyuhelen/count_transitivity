import json
from functools import partial
from collections import defaultdict


def print_predict(trans):
    # [cna_content, cna_headline, udn]
    if not all(map(lambda x: x == -1, trans)):
        print('matched prediction: ', end='')
        if trans[1] > trans[0]:
            print('標題 > 內文', end=' ')
        if trans[2] > trans[0]:
            print('年代近 > 年代遠', end='')
        print('\n')


def get_counts(verb, preps, dataset):
    # {patt:{v:{prep: sent}}}
    vn_count, pnv_count = [0, 0]
    if dataset['vn'][verb]:
        vn_count = len(dataset['vn'][verb][''])
    if dataset['pnv'][verb]:
        pnv_count = sum([len(dataset['pnv'][verb][prep]) for prep in preps])
    return vn_count, pnv_count



def get_trans(verb, preps, datasets):
    trans = []
    for dataset, name in datasets:
        vn_count, pnv_count = get_counts(verb, preps, dataset)
        if vn_count or pnv_count:
            tran = vn_count/(vn_count+pnv_count)
            print(f"{name} {verb} vn: {vn_count}; pnv: {pnv_count}; transitivity: {tran}")
        else:
            tran = -1
        trans.append(tran)
    return trans


def to_defaultdict(datasets):
    for dataset in datasets:
        yield json.loads(json.dumps(dataset), object_pairs_hook=partial(defaultdict, lambda: defaultdict(lambda: [])))


def main():
    verb_prep = json.load(open('v_prep.json'))
    cna_cont = json.load(open('../data/test/cna_cont.json'))
    cna_head = json.load(open('../data/test/cna_head.json'))
    udn = json.load(open('../data/test/udn.json'))
    cna_cont, cna_head, udn = list(to_defaultdict([cna_cont, cna_head, udn]))

    for verb, preps in verb_prep.items():
        trans = get_trans(verb, preps, ([cna_cont, 'cna_cont'], [cna_head, 'cna_head'], [udn, 'udn']))
        print_predict(trans)


if __name__ == '__main__':
    main()
