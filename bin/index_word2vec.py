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
import optparse
import sys

import word2vec


########
# main #
########
def main(output):
    """
    index word2vec file (wikiCorpus_word2vector.hr)
    :param  output:  output file path
    """
    with open(output, 'wb') as fout:
        word2vec.index(sys.stdin, fout)


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
