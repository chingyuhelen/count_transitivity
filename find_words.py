import json
v_prep = json.load(open('v_prep.json'))


def is_verb(tokens):
    # v is a target verb, ckip_pos 'V'
    unchecks = set([(token.head_loc, token.head) for token in tokens if token.head in v_prep])
    verbs = [verb for verb in unchecks if tokens[verb[0]-1].ckip_pos.startswith('V')]    
    return verbs


def is_prep(verbs, tokens, deps=('case', 'acl')):
    # the head of p is one of the verb in v_prep, with certain deps
    for token in tokens:
        if any(map(lambda x: token.word in v_prep[x[1]], verbs)) and token.dep in deps:
            yield token


def is_noun(verbs, tokens, deps=('obj', 'obl', 'nmod')):
    # n: ckip_pos == 'n', with certain deps
    for token in tokens:
        if token.ckip_pos.startswith('N') and token.dep in deps:
            yield token

# Token: nametuple ('Token', ['loc', 'word', 'par_loc', 'parent', 'dep', 'ckip_pos'])
