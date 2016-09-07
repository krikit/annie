#!/usr/bin/env python2
# -*- coding: utf-8 -*-


"""
evaluation program
__author__ = 'krikit <krikit@naver.com>'
__copyright__ = 'No copyright, just copyleft! ;)'
"""


###########
# imports #
###########
from __future__ import unicode_literals
from __future__ import print_function

import codecs
from collections import Counter
import json
import logging
logging.basicConfig(level=logging.INFO)
import optparse
import sys


#############
# functions #
#############
def _count(gold, test):
    """
    count gold, test and matched NEs
    :param  gold:  gold standard
    :param  test:  test
    :return:       (gold, test, match) counter triple
    """
    gold_cnt = Counter()
    test_cnt = Counter()
    match_cnt = Counter()
    for gold_sent, test_sent in zip(gold['sentence'], test['sentence']):
        if len(gold_sent['text']) != len(test_sent['text']):
            logging.error('content of sentences are different:')
            logging.error('\tgold: %s', gold_sent['text'])
            logging.error('\ttest: %s', test_sent['text'])
            sys.exit(2)
        gold_nes = set([(_['text'], _['type'], _['begin'], _['end']) for _ in gold_sent['NE']])
        gold_cnt.update([category for _, category, _, _ in gold_nes])
        test_nes = set([(_['text'], _['type'], _['begin'], _['end']) for _ in test_sent['NE']])
        test_cnt.update([category for _, category, _, _ in test_nes])
        match_nes = gold_nes & test_nes
        match_cnt.update([category for _, category, _, _ in match_nes])
    return gold_cnt, test_cnt, match_cnt


def _print_precision_recall(gold_num, test_num, match_num):
    """
    print precision and recall
    :param  gold_num:   number of NEs in gold standard
    :param  test_num:   number of NEs in test
    :param  match_num:  number of matched NEs
    """
    print('# of NEs in gold standard:', gold_num)
    print('# of NEs in test file    :', test_num)
    print('# of NEs in both(matched):', match_num)
    precision = (float(match_num) / test_num) if test_num > 0 else 0.0
    recall = (float(match_num) / gold_num) if gold_num > 0 else 0.0
    f1_score = (2.0 * precision * recall / (precision + recall)) \
        if precision > 0.0 and recall > 0.0 else 0.0
    print('Precision: %.4f' % precision)
    print('Recall:    %.4f' % recall)
    print('F1-score:  %.4f' % f1_score)
    print()


########
# main #
########
def main():
    """
    evaluation program
    """
    gold = json.load(open(_OPTS.gold))
    test = json.load(sys.stdin)
    if len(gold['sentence']) != len(test['sentence']):
        logging.error('# of sentences are different %d vs %d', len(gold['sentence']),
                      len(test['sentence']))
        sys.exit(1)

    gold_cnt, test_cnt, match_cnt = _count(gold, test)

    categories = sorted(list(set(gold_cnt.keys() + test_cnt.keys())))
    for category in categories:
        print('======== %s ========' % category)
        _print_precision_recall(gold_cnt[category], test_cnt[category], match_cnt[category])
    print('======== TOTAL ========')
    _print_precision_recall(sum(gold_cnt.values()), sum(test_cnt.values()),
                            sum(match_cnt.values()))


if __name__ == '__main__':
    _PARSER = optparse.OptionParser(description='evaluation program')
    _PARSER.add_option('-g', dest='gold', help='gold standard', metavar='FILE')
    _PARSER.add_option('--input', help='input file <default: stdin>', metavar='FILE')
    _PARSER.add_option('--output', help='output file <default: stdout>', metavar='FILE')
    _OPTS, _ = _PARSER.parse_args()
    if not _OPTS.gold:
        print('-g option is required', file=sys.stderr)
        _PARSER.print_usage()
        sys.exit(1)
    if _OPTS.input:
        sys.stdin = codecs.open(_OPTS.input, 'rt', encoding='UTF-8')
    if _OPTS.output:
        sys.stdout = codecs.open(_OPTS.output, 'wt', encoding='UTF-8')
    main()
