# -*- coding: utf-8 -*-


"""
feature utility module
__author__ = 'krikit <krikit@naver.com>'
__copyright__ = 'No copyright, just copyleft! ;)'
"""


###########
# imports #
###########
from __future__ import unicode_literals

from collections import defaultdict
import cPickle
import logging
logging.basicConfig(level=logging.INFO)
import re


#############
# constants #
#############
DIMENSION = 50    # dimension of vector


#############
# functions #
#############
def _merge_tag_dic(w2v_dic):
    """
    make tag dictionary with word-vector dictionary and merge tag dic with word dic
    :param  w2v_dic:  word-vector dictionary
    """
    tag_dic = {}
    cnt_dic = defaultdict(int)
    for item in w2v_dic.items():
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
        w2v_dic[tag, ] = vec_avg


def index(fin, fout):
    """
    index word2vec file
    :param  fin:   input file
    :param  fout:  output file
    """
    w2v_dic = {}
    for line_num, line in enumerate(fin, start=1):
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
        if len(vec) != DIMENSION:
            logging.warn('invalid vector dimension (%d): %s', line_num, line)
            continue
        if word == '</s>':
            w2v_dic[word, ] = vec
        try:
            lemma, tag = word.rsplit('/', 1)
        except ValueError:
            logging.warn('no lemma/tag delimiter (%d): %s', line_num, line)
            continue
        if '/' in lemma and lemma != '/':
            logging.warn('lemma/tag delimiter in lemma (%d): %s', line_num, line)
            continue
        w2v_dic[lemma, tag] = vec
    logging.info('%d number of words', len(w2v_dic))

    _merge_tag_dic(w2v_dic)
    logging.info('writing %d number of entries dictionary', len(w2v_dic))
    cPickle.dump(w2v_dic, fout, 2)
    logging.info('done')


def load(path):
    """
    load indexed word2vec dictionary
    :param  path:  file path
    :return:       word2vec dictionary
    """
    return cPickle.load(open(path, 'rb'))


def get(w2v_dic, lemma, tag):
    """
    get vector with lemma and tag
    :param  w2v_dic:  word2vec dictionary
    :param  lemma:    lemma
    :param  tag:      tag
    :return:          vector
    """
    if re.match(r'^\d+$', lemma):
        lemma = 'NUM'
    if (lemma, tag) in w2v_dic:
        return w2v_dic[lemma, tag]
    if (tag, ) in w2v_dic:
        return w2v_dic[tag, ]
    return [0.0, ] * DIMENSION


def eos(w2v_dic):
    """
    get vector of BOS/EOS(begin/end of sentence)
    :param  w2v_dic:  word2vec dictionary
    :return:          vector
    """
    return w2v_dic['</s>', ]
