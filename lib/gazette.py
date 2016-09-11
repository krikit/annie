# -*- coding: utf-8 -*-


"""
gazette utility module
__author__ = 'krikit <krikit@naver.com>'
__copyright__ = 'No copyright, just copyleft! ;)'
"""


###########
# imports #
###########
from __future__ import unicode_literals

import codecs
import re


#############
# functions #
#############
def load(path):
    """
    load gazette file
    :param  path:  gazette file path
    :return:       (dictionary, maximum length of gazette keys) pair
    """
    dic = {}
    max_key_len = 0
    for line in codecs.open(path, 'rt', encoding='UTF-8'):
        line = line.rstrip('\r\n')
        if not line:
            continue
        key, val = line.rsplit('\t', 1)
        if len(key) > max_key_len:
            max_key_len = len(key)
        dic[key] = val.split(',')
    return dic, max_key_len


def make_dt_ti_ptn(text):
    """
    make pattern from date(DT) and time(TI) entity text
    :param  text:  entity text
    :return:       pattern
    """
    ptn = re.sub(r'\s+', '', text)    # remove spaces
    return re.sub(r'\d', '0', ptn)    # replace all numbers with zero


def make_text(sent, begin, end):
    """
    make text with morp list from 'begin' to 'end'
    :param  sent:     sentence
    :param  begin:    begin index (inclusive)
    :param  end:      end index (exclusive)
    :return:          text
    """
    lemmas = [sent.morps[begin].lemma(), ]
    for idx in range(begin+1, end):
        if sent.mid2wid[idx-1] != sent.mid2wid[idx]:    # if go over word boundary
            # insert space between words
            lemmas.append(' ')
        lemmas.append(sent.morps[idx].lemma())
    return ''.join(lemmas)


def _find_right_bound(morps, begin, max_key_len):
    """
    find right bound from 'begin' with maximum key length
    :param  morps:        morph list
    :param  begin:        begin index
    :param  max_key_len:  maximum key length
    :return:              right bound
    """
    len_sum = len(morps[begin].lemma())
    for idx in range(begin+1, len(morps)):
        len_sum += len(morps[idx].lemma())
        if len_sum > max_key_len:
            return idx
    return len(morps)


def tag_nes(dic, max_key_len, sent):
    """
    tag NEs in sentence with gazette
    :param  dic:          gazette dictionary
    :param  max_key_len:  maximum length of gazette keys
    :param  sent:         sentence JSON object
    :return:              tagged JSON object
    """
    dic_nes = []
    for begin in range(len(sent.morps)):
        right_bound = _find_right_bound(sent.morps, begin, max_key_len)
        # find pattern and key, longest first
        for end in range(right_bound, begin, -1):    # end is exclusive
            text = make_text(sent, begin, end)
            categories = []
            ptn = make_dt_ti_ptn(text)
            if ptn in dic:
                categories = dic[ptn]
            else:
                key = re.sub(r'\s+', '', text).lower()
                if key in dic:
                    categories = dic[key]
            if categories:
                dic_ne_obj = {}
                dic_ne_obj['id'] = len(dic_nes)
                dic_ne_obj['text'] = text
                dic_ne_obj['type'] = categories
                dic_ne_obj['begin'] = begin
                dic_ne_obj['end'] = end-1    # NE's end is inclusive
                dic_nes.append(dic_ne_obj)
                break
    return dic_nes
