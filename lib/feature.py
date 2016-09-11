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


#############
# constants #
#############
WINDOW = 2    # left/right window size for feature extraction


#############
# functions #
#############
def _get_sign(window):
    """
    get sign of window position for feature string
    :param  window:  window position
    :return:         '+' for plus, '_' for zero, '' for minus.
                     minus integers already have minus sign
    """
    if window < 0:
        return ''
    elif window == 0:
        plus_minus = '_'
    else:
        plus_minus = '+'
    return plus_minus


def get_lemma_feat(sent, morp_id):
    """
    get lemma features of given morpheme position from sentence
    :param  sent:     sentence object
    :param  morp_id:  morpheme ID
    :return:          feature set
    """
    feat_dic = {}
    for win_idx in range(-WINDOW, WINDOW+1):
        morp_idx = morp_id + win_idx
        if morp_idx < 0:
            lemma = '<s>'
        elif morp_idx >= len(sent.morps):
            lemma = '</s>'
        else:
            lemma = sent.morps[morp_id].lemma()
        sign = _get_sign(win_idx)
        key = 'L%s%d' % (sign, win_idx)
        feat_dic[key] = lemma
    return feat_dic


def get_conjuncted_feat(feat_dic, conjunctions):
    """
    get conjunction features
    :param  feat_dic:      previously extracted features
    :param  conjunctions:  list of conjunction(tuple of feature keys)
    :return:               conjuncted features
    """
    conjucted_feat_dic = {}
    for conjunction in conjunctions:
        vals = []
        for key in conjunction:
            vals.append(feat_dic[key])
        conjucted_feat_dic['|'.join(conjunction)] = '|'.join(vals)
    return conjucted_feat_dic


def get_tag_feat(sent, morp_id):
    """
    get PoS tag features of given morpheme position from sentence
    :param  sent:     sentence object
    :param  morp_id:  morpheme ID
    :return:          feature dictionary
    """
    feat_dic = {}
    for win_idx in range(-WINDOW, WINDOW+1):
        morp_idx = morp_id + win_idx
        if morp_idx < 0:
            tag = '<s>'
        elif morp_idx >= len(sent.morps):
            tag = '</s>'
        else:
            tag = sent.morps[morp_id].tag()
        sign = _get_sign(win_idx)
        key = 'T%s%d' % (sign, win_idx)
        feat_dic[key] = tag
    return feat_dic


def get_dic_feat(sent, morp_id):
    """
    get dic tag features of given morpheme position from sentence
    :param  sent:     sentence object
    :param  morp_id:  morpheme ID
    :return:          feature dictionary
    """
    feat_dic = {}
    for win_idx in range(-WINDOW, WINDOW+1):
        morp_idx = morp_id + win_idx
        if morp_idx < 0:
            dic_label = '<s>'
        elif morp_idx >= len(sent.morps):
            dic_label = '</s>'
        else:
            dic_label = sent.dic_label(morp_id)
        sign = _get_sign(win_idx)
        key = 'D%s%d' % (sign, win_idx)
        feat_dic[key] = dic_label
    return feat_dic


def get_other_feat(sent, morp_id):
    """
    get other features of given morpheme position from sentence
    :param  sent:     sentence object
    :param  morp_id:  morpheme ID
    :return:          feature set
    """
    features = {}
    # BOS/EOS
    if morp_id == 0:
        features['BOS'] = ''
    elif morp_id == len(sent.morps)-1:
        features['EOS'] = ''
    return features


def get_all_feat(sent, morp_id):
    """
    get all features of given morpheme position from sentence
    :param  sent:     sentence object
    :param  morp_id:  morpheme ID
    :return:          feature set
    """
    feat_dic = {}
    feat_dic.update(get_lemma_feat(sent, morp_id))
    lemma_bigrams = [('L-1', 'L_0'), ('L_0', 'L+1'), ('L-1', 'L+1')]
    feat_dic.update(get_conjuncted_feat(feat_dic, lemma_bigrams))
    feat_dic.update(get_tag_feat(sent, morp_id))
    tag_bigrams = [('T-2', 'T-1'), ('T-1', 'T_0'), ('T_0', 'T+1'), ('T+1', 'T+2'), ('T-1', 'T+1')]
    feat_dic.update(get_conjuncted_feat(feat_dic, tag_bigrams))
    feat_dic.update(get_dic_feat(sent, morp_id))
    feat_dic.update(get_other_feat(sent, morp_id))
    return ['%s=%s' % (key, val) for key, val in sorted(feat_dic.items())]
