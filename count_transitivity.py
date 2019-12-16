import json
from collections import defaultdict
from argparse import ArgumentParser


def print_predict(trans, names):
    # [cna_content, cna_headline, udn]
    trans = defaultdict(int, dict(list(zip(names, trans))))
    if not all(map(lambda x: x == -1, trans.values())):
        print('matched prediction: ', end='')
        if trans['cna_head'] > trans['cna_cont'] > -1:
            print('標題 > 內文', end=' ')     
        if trans['udn'] > trans['cna_cont'] > -1:
            print('年代近 > 年代遠', end='')
        print('\n')


def get_counts(verb, preps, dataset, filtered):
    # {patt:{v:{prep: sent}}}
    vn_count, pnv_count = [0, 0]
    vn_count = len(dataset['vn'][verb][''])
    pnv_count = sum([len(dataset['pnv'][verb][prep]) for prep in preps])
    if filtered == 'yes' and vn_count and pnv_count:
        return vn_count, pnv_count
    elif filtered == 'no' and (vn_count or pnv_count):
        return vn_count, pnv_count


def get_trans(verb, preps, datasets, filtered):
    trans = []
    for dataset, name in datasets:
        result = get_counts(verb, preps, dataset, filtered)
        if result:
            vn_count, pnv_count = result
            tran = vn_count/(vn_count+pnv_count)
            print(f"{name} {verb} vn: {vn_count}; pnv: {pnv_count}; transitivity: {tran}")
        else:
            tran = -1
        trans.append(tran)
    return trans


def to_defaultdict(dataset):
    result = defaultdict(lambda: defaultdict(lambda: defaultdict(list)))
    for patt, tokens in dataset.items():
        for verb, prep_sents in tokens.items():
            for prep, sents in prep_sents.items():
                result[patt][verb][prep] = sents
    return result


def main(data, names, filtered):
    verb_prep = json.load(open('v_prep.json'))
    datasets = [to_defaultdict(dataset) for dataset in data]
    for verb, preps in verb_prep.items():
        trans = get_trans(verb, preps, zip(datasets, names), filtered)
        print_predict(trans, names)


def parse_command():
    parser = ArgumentParser()
    parser.add_argument("-d", "--data", nargs='*', default=['cna_cont', 'cna_head', 'udn'],
                        help='Enter the datasets (cna_cont, cna_head, udn) to compare.')
    parser.add_argument("-f", "--filtered", default = 'no',
                        help='Filter patterns if the counts is zero. (yes/no)')
    arg = parser.parse_args()
    return arg.data, arg.filtered


if __name__ == '__main__':
    names, filtered = parse_command()
    data = [json.load(open(f'../data/{name}.json')) for name in names]
    main(data, names, filtered)
