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


def _index_mid_to_wid(sent):
    """
    make index map from morp ID to word ID
    :param  sent:  sentence JSON object
    :return:       index
    """
    index = {}
    for word in sent['word']:
        begin = word['begin']
        end = word['end']
        word_id = word['id']
        for morp_id in range(begin, end+1):
            index[morp_id] = word_id
    return index


def make_dt_ti_ptn(text):
    """
    make pattern from date(DT) and time(TI) entity text
    :param  text:  entity text
    :return:       pattern
    """
    ptn = re.sub(r'\s+', '', text)    # remove spaces
    return re.sub(r'\d', '0', ptn)    # replace all numbers with zero


def make_text(mid2wid, morps, begin, end):
    """
    make text with morp list from 'begin' to 'end'
    :param  mid2wid:  morp ID to word ID index
    :param  morps:    morp list
    :param  begin:    begin index (inclusive)
    :param  end:      end index (exclusive)
    :return:          text
    """
    lemmas = [morps[begin]['lemma'], ]
    for idx in range(begin+1, end):
        if mid2wid[idx-1] != mid2wid[idx]:    # if go over word boundary
            lemmas.append(' ')
        lemmas.append(morps[idx]['lemma'])
    return ''.join(lemmas)


def _find_left_bound(morps, begin, max_key_len):
    """
    find left bound from 'begin' with maximum key length
    :param  morps:        morph list
    :param  begin:        begin index
    :param  max_key_len:  maximum key length
    :return:              left bound
    """
    len_sum = len(morps[begin]['lemma'])
    for idx in range(begin+1, len(morps)):
        len_sum += len(morps[idx]['lemma'])
        if len_sum > max_key_len:
            return idx
    return len(morps)


def tag_nes(gazette, max_key_len, sent):
    """
    tag NEs in sentence with gazette
    :param  gazette:      gazette dictionary
    :param  max_key_len:  maximum length of gazette keys
    :param  sent:         sentence JSON object
    :return:              tagged JSON object
    """
    nes = []
    mid2wid = _index_mid_to_wid(sent)
    morps = sent['morp']
    for begin in range(len(morps)):
        left_bound = _find_left_bound(morps, begin, max_key_len)
        # find pattern and key, longest first
        for end in range(left_bound-1, begin, -1):
            text = make_text(mid2wid, morps, begin, end)
            categories = []
            ptn = make_dt_ti_ptn(text)
            if ptn in gazette:
                categories = gazette[ptn]
            else:
                key = re.sub(r'\s+', '', text).lower()
                if key in gazette:
                    categories = gazette[key]
            if categories:
                ne_obj = {}
                ne_obj['id'] = len(nes)
                ne_obj['text'] = text
                ne_obj['type'] = categories
                ne_obj['begin'] = begin
                ne_obj['end'] = end - 1
                nes.append(ne_obj)
                break
    return nes
