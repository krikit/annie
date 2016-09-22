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
from collections import defaultdict, namedtuple
import json
import logging
logging.basicConfig(level=logging.INFO)
import optparse
import sys

import sentence


###########
# options #
###########
ERR_CATE = set()    # list of NE categories to print error cases


#########
# types #
#########
NE = namedtuple('NE', ['begin', 'end', 'cate'])    # named entity in JSON to evaluate


#############
# functions #
#############
def _morp_dbg_str(sent, begin, end):
    """
    make debug string of morphemes
    :param  sent:   sentence object
    :param  begin:  morpheme begin ID (inclusive)
    :param  end:    morpheme end ID (inclusive)
    :return:        debug string
    """
    left_context = ' '.join(_.to_dbg_str() for _ in sent.morps[begin-2:begin])
    entity_str = ' '.join(_.to_dbg_str() for _ in sent.morps[begin:end+1])
    right_context = ' '.join(_.to_dbg_str() for _ in sent.morps[end+1:end+3])
    return '%20s    [[  %s  ]]    %s' % (left_context, entity_str, right_context)


def _count(gold, test):
    """
    count gold, test and matched NEs
    :param  gold:  gold standard
    :param  test:  test
    :return:       (gold, test, match) counter triple
    """
    gold_cnt = defaultdict(int)
    test_cnt = defaultdict(int)
    match_cnt = defaultdict(int)
    for gold_sent, test_sent in zip(gold['sentence'], test['sentence']):
        if len(gold_sent['text']) != len(test_sent['text']):
            logging.error('content of sentences are different:')
            logging.error('\tgold: %s', gold_sent['text'])
            logging.error('\ttest: %s', test_sent['text'])
            sys.exit(2)
        gold_nes = set([NE(_['begin'], _['end'], _['type']) for _ in gold_sent['NE']])
        # gold_cnt.update([_.cate for _ in gold_nes])    # Counter only in 2.7
        for entity in gold_nes:
            gold_cnt[entity.cate] += 1
        test_nes = set([NE(_['begin'], _['end'], _['type']) for _ in test_sent['NE']])
        # test_cnt.update([_.cate for _ in test_nes])    # Counter only in 2.7
        for entity in test_nes:
            test_cnt[entity.cate] += 1
        match_nes = gold_nes & test_nes
        # match_cnt.update([_.cate for _ in match_nes])    # Counter only in 2.7
        for entity in match_nes:
            match_cnt[entity.cate] += 1
        if ERR_CATE:
            gold_only_nes = set([_ for _ in (gold_nes - match_nes) if _.cate in ERR_CATE])
            test_only_nes = set([_ for _ in (test_nes - match_nes) if _.cate in ERR_CATE])
            if gold_only_nes or test_only_nes:
                sent = sentence.Sentence(gold_sent)
                print(sent.to_dbg_str(), file=sys.stderr)
            for ett in sorted(list(gold_only_nes)):
                print('\t[G] (%s) %s' % (ett.cate, _morp_dbg_str(sent, ett.begin, ett.end)),
                      file=sys.stderr)
            for ett in sorted(list(test_only_nes)):
                print('\t[T] (%s) %s' % (ett.cate, _morp_dbg_str(sent, ett.begin, ett.end)),
                      file=sys.stderr)
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
    _PARSER.add_option('--err-cate', help='list of NE categories to print error cases',
                       metavar='LIST')
    _PARSER.add_option('--error', help='error file <default: stderr>', metavar='FILE')
    _OPTS, _ = _PARSER.parse_args()
    if not _OPTS.gold:
        print('-g option is required\n', file=sys.stderr)
        _PARSER.print_help(sys.stderr)
        sys.exit(1)
    if _OPTS.input:
        sys.stdin = codecs.open(_OPTS.input, 'rt', encoding='UTF-8')
    if _OPTS.output:
        sys.stdout = codecs.open(_OPTS.output, 'wt', encoding='UTF-8')
    if _OPTS.error:
        sys.stderr = codecs.open(_OPTS.error, 'wt', encoding='UTF-8')
    if _OPTS.err_cate:
        ERR_CATE = set(_OPTS.err_cate.split(','))
    main()
