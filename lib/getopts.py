#!/usr/bin/env python2
# -*- coding: utf-8 -*-


"""
option parser utility
__author__ = 'krikit <krikit@naver.com>'
__copyright__ = 'No copyright, just copyleft! ;)'
"""


###########
# imports #
###########
from __future__ import unicode_literals
from __future__ import print_function

import getopt
import sys


########
# main #
########
def main():
    """
    option parser utility
    """
    if len(sys.argv) < 3:
        sys.exit(1)
    long_options = []
    for long_opt in sys.argv[2].split(','):
        long_opt = long_opt.strip()
        if not long_opt:
            continue
        if long_opt[-1] == ':':
            long_opt = long_opt[:-1] + '='
        long_options.append(long_opt)
    try:
        opts, args = getopt.gnu_getopt(sys.argv[3:], sys.argv[1], long_options)
        for key, val in opts:
            print(key, end=' ')
            if val:
                print(val, end=' ')
        print('--', ' '.join(args))
    except getopt.GetoptError:
        sys.exit(2)


if __name__ == '__main__':
    main()
