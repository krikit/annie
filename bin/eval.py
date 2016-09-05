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
import json
import logging
logging.basicConfig(level=logging.INFO)
import optparse
import sys


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

    total_gold_nes = 0
    total_test_nes = 0
    total_match_nes = 0
    for gold_sent, test_sent in zip(gold['sentence'], test['sentence']):
        if len(gold_sent['text']) != len(test_sent['text']):
            logging.error('content of sentences are different:')
            logging.error('\tgold: %s', gold_sent['text'])
            logging.error('\ttest: %s', test_sent['text'])
            sys.exit(2)
        gold_nes = set([(_['text'], _['type'], _['begin'], _['end']) for _ in gold_sent['NE']])
        total_gold_nes += len(gold_nes)
        test_nes = set([(_['text'], _['type'], _['begin'], _['end']) for _ in test_sent['NE']])
        total_test_nes += len(test_nes)
        total_match_nes += len(gold_nes & test_nes)
    print('Total # of NEs in gold standard:', total_gold_nes)
    print('Total # of NEs in test file    :', total_test_nes)
    print('Total # of NEs in both(matched):', total_match_nes)
    precision = float(total_match_nes) / total_test_nes
    recall = float(total_match_nes) / total_gold_nes
    f1_score = 2.0 * precision * recall / (precision + recall)
    print('Precision: %.4f' % precision)
    print('Recall:    %.4f' % recall)
    print('F1-score:  %.4f' % f1_score)


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
