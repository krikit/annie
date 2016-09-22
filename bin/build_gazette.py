#!/usr/bin/env python2
# -*- coding: utf-8 -*-


"""
build integrated gazette dictionary
__author__ = 'krikit <krikit@naver.com>'
__copyright__ = 'No copyright, just copyleft! ;)'
"""


###########
# imports #
###########
from __future__ import unicode_literals
from __future__ import print_function

import codecs
from collections import defaultdict
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
def _proc_gazette(dic):
    """
    process gazette file
    :param  dic:  dictionary
    :return:      category counter
    """
    category_cnt = defaultdict(int)
    for line in codecs.open(_OPTS.gazette, 'rt', encoding='UTF-8'):
        line = line.rstrip('\r\n')
        if not line:
            continue
        key, category = line.rsplit('\t', 1)
        if category in ['DT', 'TI']:
            ptn = gazette.make_dt_ti_ptn(key)
            dic[ptn][category] += 1
        else:
            key = re.sub(r'\s+', '', key).lower()
            dic[key][category] += 1
        category_cnt[category] += 1
    return category_cnt


def _proc_corpus(dic):
    """
    process train corpus
    :param  dic:  dictionary
    :return:      category counter
    """
    category_cnt = defaultdict(int)
    json_obj = json.load(codecs.open(_OPTS.corpus, 'rt', encoding='UTF-8'))
    for sent in json_obj['sentence']:
        for entity in sent['NE']:
            category = entity['type']
            if category in ['DT', 'TI']:
                ptn = gazette.make_dt_ti_ptn(entity['text'])
                dic[ptn][category] += 1
            else:
                key = re.sub(r'\s+', '', entity['text']).lower()
                dic[key][category] += 1
            category_cnt[category] += 1
    return category_cnt


########
# main #
########
def main():
    """
    build integrated gazette dictionary
    """
    dic = defaultdict(lambda: defaultdict(int))
    total_cat_cnt = _proc_gazette(dic)
    # total_cat_cnt.update(_proc_corpus(dic))    # Counter only in 2.7
    for key, val in _proc_corpus(dic).items():
        total_cat_cnt[key] += val

    for key, cnt in dic.items():
        if re.match(r'^0+$', key) and set(cnt.keys()) <= set(['DT', 'TI']):
            # filter out only numbers of DT/TI
            continue
        # freq_cat_pairs = [(freq + total_cat_cnt[cat] / 1000000.0, cat)
        #                   for cat, freq in cnt.most_common()]    # Counter only in 2.7
        cnt_srt = sorted(cnt.items(), key=lambda itm: itm[1], reverse=True)
        freq_cat_pairs = [(freq + total_cat_cnt[cat] / 1000000.0, cat) for cat, freq in cnt_srt]
        categories = [cat for freq, cat in sorted(freq_cat_pairs, reverse=True)]
        print('%s\t%s' % (key, ','.join(categories)))


if __name__ == '__main__':
    _PARSER = optparse.OptionParser(description='build integrated gazette dictionary')
    _PARSER.add_option('-g', dest='gazette', help='gazette', metavar='FILE')
    _PARSER.add_option('-c', dest='corpus', help='corpus', metavar='FILE')
    _PARSER.add_option('--output', help='output file <default: stdout>', metavar='FILE')
    _OPTS, _ = _PARSER.parse_args()
    if not _OPTS.gazette:
        print('-g option is required\n', file=sys.stderr)
        _PARSER.print_help(sys.stderr)
        sys.exit(1)
    if not _OPTS.corpus:
        print('-c option is required\n', file=sys.stderr)
        _PARSER.print_help(sys.stderr)
        sys.exit(2)
    if _OPTS.output:
        sys.stdout = codecs.open(_OPTS.output, 'wt', encoding='UTF-8')
    main()
