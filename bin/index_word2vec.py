#!/usr/bin/env python2
# -*- coding: utf-8 -*-


"""
index word2vec file (wikiCorpus_word2vector.hr)
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
import cPickle
import logging
logging.basicConfig(level=logging.INFO)
import optparse
import sys


#############
# functions #
#############
def _merge_tag_dic(word_dic):
    """
    make tag dictionary with word-vector dictionary and merge tag dic with word dic
    :param  word_dic:  word-vector dictionary
    """
    tag_dic = {}
    cnt_dic = Counter()
    for item in word_dic.items():
        try:
            (_, tag), vec = item
            if tag in tag_dic:
                vec_sum = [lhs + rhs for lhs, rhs in zip(tag_dic[tag], vec)]
            else:
                vec_sum = vec
            tag_dic[tag] = vec_sum
            cnt_dic[tag] += 1
        except ValueError:
            continue
    logging.info('%d number of tags', len(tag_dic))
    for tag, vec_sum in tag_dic.items():
        cnt = cnt_dic[tag]
        vec_avg = [_ / cnt for _ in vec_sum]
        word_dic[tag, ] = vec_avg


########
# main #
########
def main(output):
    """
    index word2vec file (wikiCorpus_word2vector.hr)
    :param  output:  output file path
    """
    word_dic = {}
    for line_num, line in enumerate(sys.stdin, start=1):
        if line_num <= 2:
            continue
        line = line.rstrip('\r\n')
        if not line:
            continue
        if '\t' not in line:
            logging.warn('invalid format (%d): %s', line_num, line)
            continue
        try:
            word, vec_str = line.rsplit('\t', 1)
        except ValueError:
            logging.warn('no word/vector delimiter (%d): %s', line_num, line)
            continue
        vec = [float(_) for _ in vec_str.split()]
        if len(vec) != 50:
            logging.warn('invalid vector dimension (%d): %s', line_num, line)
            continue
        if word == '</s>':
            word_dic[word, ] = vec
        try:
            lemma, tag = word.rsplit('/', 1)
        except ValueError:
            logging.warn('no lemma/tag delimiter (%d): %s', line_num, line)
            continue
        if '/' in lemma and lemma != '/':
            logging.warn('lemma/tag delimiter in lemma (%d): %s', line_num, line)
            continue
        word_dic[lemma, tag] = vec
    logging.info('%d number of words', len(word_dic))

    _merge_tag_dic(word_dic)
    logging.info('writing %d number of entries dictionary', len(word_dic))
    with open(output, 'wb') as fout:
        cPickle.dump(word_dic, fout, 2)
    logging.info('done')


if __name__ == '__main__':
    _PARSER = optparse.OptionParser(description='index word2vec file (wikiCorpus_word2vector.hr)')
    _PARSER.add_option('-o', dest='output', help='output file', metavar='FILE')
    _PARSER.add_option('--input', help='input file <default: stdin>', metavar='FILE')
    _OPTS, _ = _PARSER.parse_args()
    if _OPTS.input:
        sys.stdin = codecs.open(_OPTS.input, 'rt', encoding='UTF-8')
    if not _OPTS.output:
        print('-o option is required', file=sys.stderr)
        _PARSER.print_help(sys.stderr)
        sys.exit(1)
    main(_OPTS.output)
