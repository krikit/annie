#!/usr/bin/env python2
# -*- coding: utf-8 -*-


"""
baseline system which tag only with gazette
__author__ = 'krikit <krikit@naver.com>'
__copyright__ = 'No copyright, just copyleft! ;)'
"""


###########
# imports #
###########
from __future__ import unicode_literals
from __future__ import print_function

import codecs
import json
import logging
logging.basicConfig(level=logging.INFO)
import optparse
import sys


#############
# functions #
#############
def norm_gazette_key(key):
    """
    normalize gazette key
    :param  key:  key
    :return:      normalized key
    """
    return ' '.join([_.lower() for _ in key.split()])


def load_gazette(path):
    """
    load gazette file
    :param  path:  gazette file path
    :return:       (dictionary, maximum length of gazette keys) pair
    """
    max_key_len = 0
    dic = {}
    for line in codecs.open(path, 'rt', encoding='UTF-8'):
        line = line.rstrip('\r\n')
        if not line:
            continue
        key, val = line.rsplit('\t', 1)
        key = norm_gazette_key(key)
        if key in dic:
            logging.warn('key: %s already exists, val: %s, but new val: %s', key, dic[key], val)
        elif len(key) > 1:
            dic[key] = val
        if len(key) > max_key_len:
            max_key_len = len(key)
    return dic, max_key_len


def tag_ne_with_gazette(gazette, max_key_len, sent):
    """
    tag NEs in sentence with gazette
    :param  gazette:      gazette dictionary
    :param  max_key_len:  maximum length of gazette keys
    :param  sent:         sentence JSON object
    :return:              tagged JSON object
    """
    del sent['NE'][:]    # remove if there already exist NEs
    lemmas = [_['lemma'] for _ in sent['morp']]
    lemmas_lower = [_.lower() for _ in lemmas]
    for begin in range(len(lemmas)):
        for end in range(len(lemmas), begin, -1):
            key = ' '.join(lemmas_lower[begin:end])
            if len(key) > max_key_len:
                continue
            if key in gazette:
                ne_obj = {}
                ne_obj['id'] = len(sent['NE'])
                ne_obj['text'] = ' '.join(lemmas[begin:end])
                ne_obj['type'] = gazette[key]
                ne_obj['begin'] = begin
                ne_obj['end'] = end-1
                sent['NE'].append(ne_obj)
                break
    return sent


########
# main #
########
def main():
    """
    baseline system which tag only with gazette
    """
    gazette, max_key_len = load_gazette(_OPTS.gazette)
    json_obj = json.load(sys.stdin)
    for sent in json_obj['sentence']:
        tag_ne_with_gazette(gazette, max_key_len, sent)
    json.dump(json_obj, sys.stdout, ensure_ascii=False, indent=2)


if __name__ == '__main__':
    _PARSER = optparse.OptionParser(description='baseline system which tag only with gazette')
    _PARSER.add_option('-g', dest='gazette', help='gazette', metavar='FILE')
    _PARSER.add_option('--input', help='input file <default: stdin>', metavar='FILE')
    _PARSER.add_option('--output', help='output file <default: stdout>', metavar='FILE')
    _OPTS, _ = _PARSER.parse_args()
    if not _OPTS.gazette:
        print('-g option is required', file=sys.stderr)
        _PARSER.print_usage()
        sys.exit(1)
    if _OPTS.input:
        sys.stdin = codecs.open(_OPTS.input, 'rt', encoding='UTF-8')
    if _OPTS.output:
        sys.stdout = codecs.open(_OPTS.output, 'wt', encoding='UTF-8')
    main()
