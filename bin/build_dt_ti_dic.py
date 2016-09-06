#!/usr/bin/env python2
# -*- coding: utf-8 -*-


"""
build date(DT) and time(TI) pattern dictionary
__author__ = 'krikit <krikit@naver.com>'
__copyright__ = 'No copyright, just copyleft! ;)'
"""


###########
# imports #
###########
from __future__ import unicode_literals
from __future__ import print_function

import codecs
from collections import Counter, defaultdict
import json
import logging
logging.basicConfig(level=logging.INFO)
import optparse
import re
import sys

import gazette


#############
# functions #
#############
def _proc_gazette(ptn_dic):
    """
    process gazette file
    :param  ptn_dic:  pattern dictionary
    """
    for line in codecs.open(_OPTS.gazette, 'rt', encoding='UTF-8'):
        line = line.rstrip('\r\n')
        if not line:
            continue
        key, val = line.rsplit('\t', 1)
        if val not in ['DT', 'TI']:
            continue
        ptn = gazette.make_dt_ti_ptn(key)
        ptn_dic[ptn][val] += 1


def _proc_corpus(ptn_dic):
    """
    process train corpus
    :param  ptn_dic:  pattern dictionary
    """
    json_obj = json.load(sys.stdin)
    for sent in json_obj['sentence']:
        for entity in sent['NE']:
            category = entity['type']
            if category not in ['DT', 'TI']:
                continue
            ptn = gazette.make_dt_ti_ptn(entity['text'])
            ptn_dic[ptn][category] += 1


########
# main #
########
def main():
    """
    build date(DT) and time(TI) pattern dictionary
    """
    ptn_dic = defaultdict(Counter)
    _proc_gazette(ptn_dic)
    _proc_corpus(ptn_dic)

    for ptn, cnt in ptn_dic.items():
        if re.match(r'^0+$', ptn):    # filter out only numbers
            continue
        categories = [category for category, _ in cnt.most_common(2)]
        print('%s\t%s' % (ptn, ','.join(categories)))


if __name__ == '__main__':
    _PARSER = optparse.OptionParser(description='build date(DT) and time(TI) pattern dictionary')
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
