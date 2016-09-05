# -*- coding: utf-8 -*-


"""
gazette utility module
__author__ = 'krikit <krikit@naver.com>'
__copyright__ = 'No copyright, just copyleft! ;)'
"""


###########
# imports #
###########
from collections import defaultdict
import codecs


#############
# functions #
#############
def load(path):
    """
    load gazette file
    :param  path:  gazette file path
    :return:       (dictionary, maximum length of gazette keys) pair
    """
    dic = defaultdict(list)
    max_key_len = 0
    for line in codecs.open(path, 'rt', encoding='UTF-8'):
        line = line.rstrip('\r\n')
        if not line:
            continue
        key, val = line.rsplit('\t', 1)
        key = key.lower()
        if val not in dic[key]:
            dic[key].append(val)
        if len(key) > max_key_len:
            max_key_len = len(key)
    return dic, max_key_len


def tag_nes(gazette, max_key_len, sent):
    """
    tag NEs in sentence with gazette
    :param  gazette:      gazette dictionary
    :param  max_key_len:  maximum length of gazette keys
    :param  sent:         sentence JSON object
    :return:              tagged JSON object
    """
    nes = []
    lemmas = [_['lemma'] for _ in sent['morp']]
    lemmas_lower = [_.lower() for _ in lemmas]
    for begin in range(len(lemmas)):
        for end in range(len(lemmas), begin, -1):
            key = ' '.join(lemmas_lower[begin:end])
            if len(key) > max_key_len:
                continue
            if key in gazette:
                ne_obj = {}
                ne_obj['id'] = len(nes)
                ne_obj['text'] = ' '.join(lemmas[begin:end])
                ne_obj['type'] = gazette[key]
                ne_obj['begin'] = begin
                ne_obj['end'] = end-1
                nes.append(ne_obj)
                break
    return nes
