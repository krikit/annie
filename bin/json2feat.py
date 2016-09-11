#!/usr/bin/env python2
# -*- coding: utf-8 -*-


"""
convert from JSON to CRFsuite feature format
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
import optparse
import sys

import feature
import gazette
import sentence


########
# main #
########
def main():
    """
    convert from JSON to CRFsuite feature format
    """
    dic, max_key_len = gazette.load(_OPTS.gazette)

    json_obj = json.load(sys.stdin)
    for sent_obj in json_obj['sentence']:
        sent = sentence.Sentence(sent_obj)
        sent.tag_nes(dic, max_key_len)
        for morp in sent.morps:
            features = feature.get_all_feat(sent, morp.id())
            print('%s\t%s' % (sent.label(morp.id()), '\t'.join(features)))
        print()


if __name__ == '__main__':
    _PARSER = optparse.OptionParser(description='convert from JSON to CRFsuite feature format')
    _PARSER.add_option('-g', dest='gazette', help='gazette', metavar='FILE')
    _PARSER.add_option('--input', help='input file <default: stdin>', metavar='FILE')
    _PARSER.add_option('--output', help='output file <default: stdout>', metavar='FILE')
    _OPTS, _ARGS = _PARSER.parse_args()
    if not _OPTS.gazette:
        print('-g option is required', file=sys.stderr)
        _PARSER.print_usage()
        sys.exit(1)
    if _OPTS.input:
        sys.stdin = codecs.open(_OPTS.input, 'rt', encoding='UTF-8')
    if _OPTS.output:
        sys.stdout = codecs.open(_OPTS.output, 'wt', encoding='UTF-8')
    main()
