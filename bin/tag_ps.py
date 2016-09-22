#!/usr/bin/env python2
# -*- coding: utf-8 -*-


"""
tag person(PS) with SVM classifier
__author__ = 'krikit <krikit@naver.com>'
__copyright__ = 'No copyright, just copyleft! ;)'
"""


###########
# imports #
###########
from __future__ import unicode_literals
from __future__ import print_function

import codecs
import cPickle
import json
import logging
logging.basicConfig(level=logging.INFO)
import optparse
import sys

import feature
import sentence
import word2vec


#############
# constants #
#############
SVM_WINDOW = 2    # SVM classifier context window


#############
# functions #
#############
def _tag_ps(w2v_dic, svm_model, sent):
    """
    tag PS in sentence with SVM model
    :param  w2v_dic:    word2vec dictionary
    :param  svm_model:  SVM model
    :param  sent:       Sentence object
    :return:            PS NEs
    """
    ps_nes = []
    for morp in sent.morps:
        if len(morp.lemma()) != 3 or morp.tag() != 'NNP' or sent.label(morp.id()) != 'O':
            continue
        feat_vec = feature.get_svm_feat(w2v_dic, SVM_WINDOW, sent, morp.id())
        is_ps = svm_model.predict([feat_vec, ])[0]
        if is_ps:
            ps_ne_obj = {}
            ps_ne_obj['id'] = len(ps_nes)
            ps_ne_obj['text'] = morp.lemma()
            ps_ne_obj['type'] = 'PS'
            ps_ne_obj['begin'] = morp.id()
            ps_ne_obj['end'] = morp.id()
            ps_nes.append(ps_ne_obj)
    return ps_nes


def _merge_ne(sent, ps_nes):
    """
    merge PS NEs with existing NEs in sentence
    :param  sent:    Sentence object
    :param  ps_nes:  PS NEs
    :return:         merged NEs
    """
    merged = sent.json_obj['NE'] + ps_nes
    merged.sort(key=lambda entity: entity['begin'])
    for idx, entity in enumerate(merged):
        entity['id'] = idx
    return merged


########
# main #
########
def main(w2v_path, model_path):
    """
    tag person(PS) with SVM classifier
    :param  w2v_path:    word2vec file path
    :param  model_path:  model path
    """
    w2v_dic = word2vec.load(w2v_path)
    svm_model = cPickle.load(open(model_path, 'rb'))

    json_obj = json.load(sys.stdin)
    for sent_obj in json_obj['sentence']:
        sent = sentence.Sentence(sent_obj)
        ps_nes = _tag_ps(w2v_dic, svm_model, sent)
        sent_obj['NE'] = _merge_ne(sent, ps_nes)
    json.dump(json_obj, sys.stdout, ensure_ascii=False, indent=2)


if __name__ == '__main__':
    _PARSER = optparse.OptionParser(description='tag person(PS) with SVM classifier')
    _PARSER.add_option('-w', dest='w2v', help='word2vec file', metavar='FILE')
    _PARSER.add_option('-m', dest='model', help='SVM model', metavar='FILE')
    _PARSER.add_option('--input', help='input file <default: stdin>', metavar='FILE')
    _PARSER.add_option('--output', help='output file <default: stdout>', metavar='FILE')
    _OPTS, _ = _PARSER.parse_args()
    if not _OPTS.model:
        print('-w option is required\n', file=sys.stderr)
        _PARSER.print_help(sys.stderr)
        sys.exit(1)
    if not _OPTS.model:
        print('-m option is required\n', file=sys.stderr)
        _PARSER.print_help(sys.stderr)
        sys.exit(2)
    if _OPTS.input:
        sys.stdin = codecs.open(_OPTS.input, 'rt', encoding='UTF-8')
    if _OPTS.output:
        sys.stdout = codecs.open(_OPTS.output, 'wt', encoding='UTF-8')
    main(_OPTS.w2v, _OPTS.model)
