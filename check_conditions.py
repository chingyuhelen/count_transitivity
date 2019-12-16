from find_words import is_noun, is_prep, is_verb
import itertools


def is_vn(verbs, pnv, punts, tokens):
    nouns = list(is_noun(verbs, tokens, ('obj')))
    for verb, noun in itertools.product(verbs, nouns):
        vloc, v = verb
        # 1. n.head == v; 2. v n; 3.(x) v punt n
        if vloc == noun.head_loc and vloc < noun.loc and check_punts(vloc, noun.loc, punts):
            # n cannot be the n in pnv
            if not any(map(lambda x: noun.loc == x[2], pnv)):
                yield vloc, v, noun.loc, noun.word


def check_punts(token1, token2, punts):
    return True if not any(map(lambda x: token1 < x < token2, punts)) else False


def check_precedence(loc1, loc2, prep_loc=-1):
    return True if prep_loc < loc1 < loc2 else False


def is_good_pair(vloc, prep, noun, punts):
    # head->dep:  1. v->n->p or v->p->n; 2. (x)p punt n; (3)p n v
    return True if ((vloc == prep.head_loc and prep.loc == noun.head_loc)
                    or (vloc == noun.head_loc and noun.loc == prep.head_loc))\
                    and check_punts(prep.loc, noun.loc, punts)\
                    and check_precedence(noun.loc, vloc, prep_loc=prep.loc)\
                    else False


def is_pnv(verbs, preps, punts, tokens):
    nouns = list(is_noun(verbs, tokens))  # nouns: Tokens
    for verb, prep, noun in itertools.product(verbs, preps, nouns):
        vloc, v = verb
        if is_good_pair(vloc, prep, noun, punts):
            # p n punt v if prep is '對' or '對於' else (x)
            if prep.word in ['對', '對於'] or check_punts(noun.loc, vloc, punts):
                yield vloc, v, noun.loc, noun.word, prep.loc, prep.word


def find_patterns(tokens):
    # Tokens: nametuple ('Token', ['loc', 'word', 'par_loc', 'parent', 'dep', 'ckip_pos'])
    punts = [token.loc for token in tokens if token.word in ('。', '，', '?')]
    verbs = is_verb(tokens)
    # verbs: [(loc, verb), ...]
    
    if verbs:
        preps = list(is_prep(verbs, tokens)) # preps: Tokens
        pnv = list(is_pnv(verbs, preps, punts, tokens))
        vn = list(is_vn(verbs, pnv, punts, tokens))
        return pnv, vn

    return [], []
