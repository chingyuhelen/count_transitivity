import json
from collections import defaultdict
from find_patterns_reduce import main as reduce


def formatting(verb_tok, prep_tok, noun_tok, lines, ckip_sents):
    # from ckip format to 我 [對] 這件 [事] 很 ＋＋關心＋＋
    for verb, noun, prep, sent_id in lines:
        try:
            line = ckip_sents[sent_id]
            words = [token[:-1].rsplit('(', 1)[0] for token in line.split()]
            words[int(verb)-1] = f"++{words[int(verb)-1]}++"
            words[int(noun)-1] = f"[{words[int(noun)-1]}]"
            if prep:
                words[int(prep)-1] = f"[{words[int(prep)-1]}]"
            yield ' '.join(words)
        except:
            print(verb, noun, prep, sent_id)


def main(iterable, ckip_sents):
    cna_cont = defaultdict(lambda: defaultdict(lambda: defaultdict(list)))
    cna_head = defaultdict(lambda: defaultdict(lambda: defaultdict(list)))
    udn = defaultdict(lambda: defaultdict(lambda: defaultdict(list)))

    for dataset, verb, prep, patt, noun, *lines in iterable:
        for sent in formatting(verb, prep, noun, lines, ckip_sents):
            if dataset == 'cna_content':
                cna_cont[patt][verb][prep].append(sent)
            elif dataset == 'cna_headline':
                cna_head[patt][verb][prep].append(sent)
            elif dataset == 'udn':
                udn[patt][verb][prep].append(sent)

    json.dump(cna_cont, open('../data/test/cna_cont.json', 'w'))
    json.dump(cna_head, open('../data/test/cna_head.json', 'w'))
    json.dump(udn, open('../data/test/udn.json', 'w'))


if __name__ == "__main__":
    import fileinput
    iterable = list(map(lambda x: x.strip().split('\t'), fileinput.input()))
    texts = list(reduce(iterable))
    ckip_sents = dict(map(lambda x: x.strip().split(' ', 1), open('../data/sents.txt').readlines()))
    main(texts, ckip_sents)

    # news, verb, prep, pattern, noun, sents, sents, ...
    # sents: verb_loc, prep_loc, noun_loc, sent_id
