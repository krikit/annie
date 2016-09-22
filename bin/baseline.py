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

import gazette
import sentence


#############
# functions #
#############
def _filter_dic_nes(dic_nes):
    """
    filter tagged(dictionary matched) NEs
    :param  dic_nes:  raw tagged NEs
    :return:          filtered NEs
    """
    filtered = [_ for _ in dic_nes if len(_.text()) > 1]    # filter out length 1
    for idx, entity in enumerate(filtered):
        entity.set_id(idx)    # reset id
        entity.set_category(entity.category()[0])    # select first type of list
    return filtered


########
# main #
########
def main():
    """
    baseline system which tag only with gazette
    """
    dic, max_key_len = gazette.load(_OPTS.gazette)

    json_obj = json.load(sys.stdin)
    for sent_obj in json_obj['sentence']:
        sent = sentence.Sentence(sent_obj)
        sent.tag_nes(dic, max_key_len)
        filtered = [_.json_obj for _ in _filter_dic_nes(sent.dic_nes)]
        sent_obj['NE'] = filtered
    json.dump(json_obj, sys.stdout, ensure_ascii=False, indent=2)


if __name__ == '__main__':
    _PARSER = optparse.OptionParser(description='baseline system which tag only with gazette')
    _PARSER.add_option('-g', dest='gazette', help='gazette', metavar='FILE')
    _PARSER.add_option('--input', help='input file <default: stdin>', metavar='FILE')
    _PARSER.add_option('--output', help='output file <default: stdout>', metavar='FILE')
    _OPTS, _ = _PARSER.parse_args()
    if not _OPTS.gazette:
        print('-g option is required\n', file=sys.stderr)
        _PARSER.print_help(sys.stderr)
        sys.exit(1)
    if _OPTS.input:
        sys.stdin = codecs.open(_OPTS.input, 'rt', encoding='UTF-8')
    if _OPTS.output:
        sys.stdout = codecs.open(_OPTS.output, 'wt', encoding='UTF-8')
    main()
