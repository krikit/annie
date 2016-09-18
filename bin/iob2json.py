#!/usr/bin/env python2
# -*- coding: utf-8 -*-


"""
convert from CRFsuite IOB tagged to JSON
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
def _load_iob_sentences(fin):
    """
    load IOB tagged file
    :param  fin:  input file object
    :return:       list of sentences(sentence = IOB tag sequences)
    """
    iobs = []
    iob = []
    for line in fin:
        line = line.rstrip('\r\n')
        if not line:
            if iob:
                iobs.append(iob)
                iob = []
            continue
        iob.append(line)
    return iobs


def _make_nes(sent, iob):
    """
    make JSON NEs object from sentence with IOB tag sequence
    :param  sent:  sentence
    :param  iob:   IOB tag sequence
    :return:       NE JSON object
    """
    nes = []
    category = ''
    begin = -1
    end = -1
    for idx, label in enumerate(iob):
        if label == 'O':
            continue
        elif label.startswith('B-'):
            if category:
                ne_obj = {}
                ne_obj['id'] = len(nes)
                ne_obj['text'] = gazette.make_text(sent, begin, end+1)    # NE's end is inclusive
                ne_obj['type'] = category
                ne_obj['begin'] = begin
                ne_obj['end'] = end
                nes.append(ne_obj)
            category = label[2:]
            begin = idx
            end = idx
        elif label.startswith('I-'):
            if not category:
                raise RuntimeError('I- tag without B- tag')
            if label[2:] != category:
                logging.warn('I- category is different from B-')
                category = label[2:]
            end = idx
    if category:
        ne_obj = {}
        ne_obj['id'] = len(nes)
        ne_obj['text'] = gazette.make_text(sent, begin, end+1)    # NE's end is inclusive
        ne_obj['type'] = category
        ne_obj['begin'] = begin
        ne_obj['end'] = end
        nes.append(ne_obj)
    return nes


########
# main #
########
def main():
    """
    convert from CRFsuite IOB tagged to JSON
    """
    json_obj = json.load(codecs.open(_OPTS.json, 'rt', encoding='UTF-8'))
    iobs = _load_iob_sentences(sys.stdin)
    if len(json_obj['sentence']) != len(iobs):
        logging.error('# of sentences are different %d vs %d', len(json_obj['sentence']), len(iobs))
        sys.exit(1)

    for sent_obj, iob in zip(json_obj['sentence'], iobs):
        sent = sentence.Sentence(sent_obj)
        if len(sent.morps) != len(iob):
            logging.error('morpheme lengths in sentence are different:')
            logging.error('\tjson: %s', len(sent.morps))
            logging.error('\tiob : %s', len(iob))
            sys.exit(2)
        sent_obj['NE'] = _make_nes(sent, iob)
    json.dump(json_obj, sys.stdout, ensure_ascii=False, indent=2)


if __name__ == '__main__':
    _PARSER = optparse.OptionParser(description='convert from CRFsuite IOB tagged to JSON')
    _PARSER.add_option('-j', dest='json', help='JSON file', metavar='FILE')
    _PARSER.add_option('--input', help='input file <default: stdin>', metavar='FILE')
    _PARSER.add_option('--output', help='output file <default: stdout>', metavar='FILE')
    _OPTS, _ARGS = _PARSER.parse_args()
    if not _OPTS.json:
        print('-j option is required', file=sys.stderr)
        _PARSER.print_usage()
        sys.exit(1)
    if _OPTS.input:
        sys.stdin = codecs.open(_OPTS.input, 'rt', encoding='UTF-8')
    if _OPTS.output:
        sys.stdout = codecs.open(_OPTS.output, 'wt', encoding='UTF-8')
    main()
