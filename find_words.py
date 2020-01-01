import json
v_prep = json.load(open('v_prep.json'))


def is_verb(tokens):
    # v is a target verb, ckip_pos 'V'
    '''If the word happens to be the root of the sentences, it will be presented as 'ROOT instead of the word itself. 
    Therefore, I check whether its parent is one of the target verb instead of the word, and save the info of the parents and its index if it fullfill the requirment.
    I find the position in the sentence by substracting one the index of the parent to take the correct token, which includes the ckip pos. 
    Then, We can check whether it is a verb.
    
    e.g., assuming the target verb is '談論'
    [[1, '錢復', 2, '談論', 'nsubj', 'Nba'],  
     [0, 'ROOT', 2, '談論', 'root', 'VE2'],
     [3, '鄧小平', 4, '回憶', 'advmod', 'Nb'],
    ...]
    
    [1, '錢復', 2, '談論', 'nsubj', 'Nba'] ==> the parent '談論' is one of the target verb, its index is 2
    To find the ckip pos of '談論', we have to find the token which includes '談論' as the word. 
    We subtract 1 from the the index of the parent '談論'(i.e., 2), and find the index of the target token (i.e., 2). 
    [0, 'ROOT', 2, '談論', 'root', 'VE2']
 
    '''
    
    unchecks = set([(token.head_loc, token.head) for token in tokens if token.head in v_prep])
    verbs = [verb for verb in unchecks if tokens[verb[0]-1].ckip_pos.startswith('V')]    
    return verbs


def is_prep(verbs, tokens, deps=('case', 'acl')):
    # the head of p is one of the verb in v_prep, with certain deps
    '''TO DO:
    We should include the posibility that prep does not directly depend on the verb,
    but dependent on a noun directly depending the verb.
    '''
    
    for token in tokens:
        if any(map(lambda x: token.word in v_prep[x[1]], verbs)) and token.dep in deps:
            yield token


def is_noun(verbs, tokens, deps=('obj', 'obl', 'nmod')):
    # n: ckip_pos == 'n', with certain deps
    for token in tokens:
        if token.ckip_pos.startswith('N') and token.dep in deps:
            yield token

# tokens: [['loc', 'word', 'par_loc', 'parent', 'dep', 'ckip_pos'], ...]

'''
An instruction of the format:

Ckip: 錢復(Nba) 談論(VE2) 鄧小平(Nb) 回憶(VK1) 中美(Nca) 斷交(VH11) 過往(Nad) 。(PERIODCATEGORY)

standford universal dependency:
nsubj(錢復-1, 談論-2)	root(ROOT-0, 談論-2)	advmod(鄧小平-3, 回憶-4)	amod(回憶-4, 中美-5)	nsubj(中美-5, 斷交-6)	ccomp(斷交-6, 談論-2)	obj(過往-7, 斷交-6)	punct(。-8, 談論-2)

Each token includes the information of dependence, a word, its index in the sentences (starting from 1), its parent and the index of the parent.
e.g., nsubj(錢復-1, 談論-2): dep(word-loc, parent-parentloc)
      1. a word: 錢復
      2. the index of the word in the sentence (錢復 談論 鄧小平 回憶 中美 斷交 過往 。): 1
      3. the parent: 談論
      4. the index of the parent: 2
      5. the universal dependency of the word and its parent: nsubj (it means 錢復 is the subject of 談論)

These tokens is listed according to the sequence of words in the sentences.
錢復 談論 鄧小平 回憶 中美 斷交 過往 。
nsubj(錢復-1, 談論-2)
root(ROOT-0, 談論-2)
advmod(鄧小平-3, 回憶-4)
amod(回憶-4, 中美-5)
nsubj(中美-5, 斷交-6)
ccomp(斷交-6, 談論-2)

The standford format is reformatted as ['loc', 'word', 'par_loc', 'parent', 'dep', 'ckip_pos']:
[[1, '錢復', 2, '談論', 'nsubj', 'Nba'],
 [0, 'ROOT', 2, '談論', 'root', 'VE2'],
 [3, '鄧小平', 4, '回憶', 'advmod', 'Nb'],
 ...]
 
If the word happens to be the root of the sentence (e.g., '談論'), the word is presented as 'ROOT' and the location is '0'.
The actual word and its relative position in the sentence is shown by its parent (i.e., '談論') and the index of the parent (i.e., 2).


'''
