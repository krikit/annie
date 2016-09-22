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

import word2vec


#############
# constants #
#############
CRF_WINDOW = 2    # left/right window size for CRF feature extraction


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


def _get_position_feat(sent, morp_id, func, key_pfx):
    """
    get features of given morpheme position from sentence
    :param  sent:     sentence object
    :param  morp_id:  morpheme ID
    :param  func:     feature value function
    :param  key_pfx:  feature key prefix
    :return:          feature set
    """
    feat_dic = {}
    for win_idx in range(-CRF_WINDOW, CRF_WINDOW+1):
        morp_idx = morp_id + win_idx
        if morp_idx < 0:
            val = '<s>'
        elif morp_idx >= len(sent.morps):
            val = '</s>'
        else:
            val = func(sent, morp_idx)
        sign = _get_sign(win_idx)
        key = '%s%s%d' % (key_pfx, sign, win_idx)
        feat_dic[key] = val
    return feat_dic


def get_lemma_feat(sent, morp_id):
    """
    lemma features
    :param  sent:     sentence object
    :param  morp_id:  morpheme ID
    :return:          feature set
    """
    return _get_position_feat(sent, morp_id,
                              lambda sent, morp_id: sent.morps[morp_id].lemma(), 'L')


def get_tag_feat(sent, morp_id):
    """
    PoS tag features
    :param  sent:     sentence object
    :param  morp_id:  morpheme ID
    :return:          feature dictionary
    """
    return _get_position_feat(sent, morp_id,
                              lambda sent, morp_id: sent.morps[morp_id].tag(), 'T')


def get_dic_feat(sent, morp_id):
    """
    dic tag features
    :param  sent:     sentence object
    :param  morp_id:  morpheme ID
    :return:          feature dictionary
    """
    return _get_position_feat(sent, morp_id,
                              lambda sent, morp_id: sent.dic_label(morp_id), 'D')


def get_len_feat(sent, morp_id):
    """
    length features
    :param  sent:     sentence object
    :param  morp_id:  morpheme ID
    :return:          feature dictionary
    """
    return _get_position_feat(sent, morp_id,
                              lambda sent, morp_id: str(len(sent.morps[morp_id].lemma())), 'N')


def get_pfx_feat(sent, morp_id):
    """
    prefix features
    :param  sent:     sentence object
    :param  morp_id:  morpheme ID
    :return:          feature dictionary
    """
    feat_dic1 = _get_position_feat(sent, morp_id,
                                   lambda sent, morp_id: sent.morps[morp_id].lemma()[:1], 'P')
    feat_dic2 = _get_position_feat(sent, morp_id,
                                   lambda sent, morp_id: sent.morps[morp_id].lemma()[:2], 'PP')
    feat_dic1.update(feat_dic2)
    return feat_dic1


def get_sfx_feat(sent, morp_id):
    """
    suffix features
    :param  sent:     sentence object
    :param  morp_id:  morpheme ID
    :return:          feature dictionary
    """
    feat_dic1 = _get_position_feat(sent, morp_id,
                                   lambda sent, morp_id: sent.morps[morp_id].lemma()[-1:], 'S')
    feat_dic2 = _get_position_feat(sent, morp_id,
                                   lambda sent, morp_id: sent.morps[morp_id].lemma()[-2:], 'SS')
    feat_dic1.update(feat_dic2)
    return feat_dic1


def get_lex_form_feat(sent, morp_id):
    """
    lexical form features
    :param  sent:     sentence object
    :param  morp_id:  morpheme ID
    :return:          feature set
    """
    return _get_position_feat(sent, morp_id,
                              lambda sent, morp_id: sent.morps[morp_id].lex_form(), 'F')

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
        features['BOW'] = ''
    elif morp_id == len(sent.morps)-1:
        features['EOS'] = ''
        features['EOW'] = ''
    else:
        # BOW/MOW/EOW
        if sent.mid2wid[morp_id] == sent.mid2wid[morp_id-1]+1:
            features['BOW'] = ''
        elif sent.mid2wid[morp_id] == sent.mid2wid[morp_id+1]-1:
            features['EOW'] = ''
        else:
            features['MOW'] = ''
    # prev word's last lemma
    word_id = sent.mid2wid[morp_id]
    if word_id > 0:
        features['PWLL'] = sent.morps[sent.words[word_id-1].end()].lemma()
    else:
        features['PWLL'] = '<s>'
    # next word's prev lemma
    if word_id+1 < len(sent.words):
        features['NWFL'] = sent.morps[sent.words[word_id+1].begin()].lemma()
    else:
        features['NWFL'] = '</s>'
    return features


def _get_conjunction_feat(feat_dic, conjunctions):
    """
    get conjunction features
    :param  feat_dic:      previously extracted features
    :param  conjunctions:  list of conjunction(tuple of feature keys)
    :return:               conjunction features
    """
    conjunction_feat_dic = {}
    for conjunction in conjunctions:
        vals = []
        for key in conjunction:
            vals.append(feat_dic[key])
        conjunction_feat_dic['|'.join(conjunction)] = '|'.join(vals)
    return conjunction_feat_dic


def get_all_conjunction_features(feat_dic):
    """
    get all conjunction features
    :param  feat_dic:  previously extracted features
    :return:           conjunction features
    """
    conjunction_feat_dic = {}
    lemma_bigrams = [('L-2', 'L-1'), ('L-1', 'L_0'), ('L-1', 'L+1'), ('L_0', 'L+1'), ('L+1', 'L+2')]
    conjunction_feat_dic.update(_get_conjunction_feat(feat_dic, lemma_bigrams))
    tag_bigrams = [('T-2', 'T-1'), ('T-1', 'T_0'), ('T-1', 'T+1'), ('T_0', 'T+1'), ('T+1', 'T+2')]
    conjunction_feat_dic.update(_get_conjunction_feat(feat_dic, tag_bigrams))
    tag_trigrams = [('T-2', 'T-1', 'T_0'), ('T-1', 'T_0', 'T+1'), ('T_0', 'T+1', 'T+2')]
    conjunction_feat_dic.update(_get_conjunction_feat(feat_dic, tag_trigrams))
    dic_bigrams = [('D-2', 'D-1'), ('D-1', 'D_0'), ('D-1', 'D+1'), ('D_0', 'D+1'), ('D+1', 'D+2')]
    conjunction_feat_dic.update(_get_conjunction_feat(feat_dic, dic_bigrams))
    dic_trigrams = [('D-2', 'D-1', 'D_0'), ('D-1', 'D_0', 'D+1'), ('D_0', 'D+1', 'D+2')]
    conjunction_feat_dic.update(_get_conjunction_feat(feat_dic, dic_trigrams))
    dic_len = [('D-2', 'N-2'), ('D-1', 'N-1'), ('D_0', 'N_0'), ('D+1', 'N+1'), ('D+2', 'N+2')]
    conjunction_feat_dic.update(_get_conjunction_feat(feat_dic, dic_len))
    pfx1_len = [('P-2', 'N-2'), ('P-1', 'N-1'), ('P_0', 'N_0'), ('P+1', 'N+1'), ('P+2', 'N+2')]
    conjunction_feat_dic.update(_get_conjunction_feat(feat_dic, pfx1_len))
    pfx2_len = [('PP-2', 'N-2'), ('PP-1', 'N-1'), ('PP_0', 'N_0'), ('PP+1', 'N+1'), ('PP+2', 'N+2')]
    conjunction_feat_dic.update(_get_conjunction_feat(feat_dic, pfx2_len))
    sfx1_len = [('S-2', 'N-2'), ('S-1', 'N-1'), ('S_0', 'N_0'), ('S+1', 'N+1'), ('S+2', 'N+2')]
    conjunction_feat_dic.update(_get_conjunction_feat(feat_dic, sfx1_len))
    sfx2_len = [('SS-2', 'N-2'), ('SS-1', 'N-1'), ('SS_0', 'N_0'), ('SS+1', 'N+1'), ('SS+2', 'N+2')]
    conjunction_feat_dic.update(_get_conjunction_feat(feat_dic, sfx2_len))
    conjunction_feat_dic.update(_get_conjunction_feat(feat_dic, [('PWLL', 'NWFL'), ]))
    return conjunction_feat_dic


def remove_features(feat_dic):
    """
    remove  features
    :param  feat_dic:  extracted all features
    """
    for key in ['N-2', 'N-1', 'N_0', 'N+1', 'N+2']:
        del feat_dic[key]


def get_all_feat(sent, morp_id):
    """
    get all CRF features of given morpheme position from sentence
    :param  sent:     sentence object
    :param  morp_id:  morpheme ID
    :return:          feature set
    """
    feat_dic = {}
    feat_dic.update(get_lemma_feat(sent, morp_id))
    feat_dic.update(get_tag_feat(sent, morp_id))
    feat_dic.update(get_dic_feat(sent, morp_id))
    feat_dic.update(get_len_feat(sent, morp_id))
    feat_dic.update(get_pfx_feat(sent, morp_id))
    feat_dic.update(get_sfx_feat(sent, morp_id))
    feat_dic.update(get_lex_form_feat(sent, morp_id))
    feat_dic.update(get_other_feat(sent, morp_id))
    feat_dic.update(get_all_conjunction_features(feat_dic))
    remove_features(feat_dic)
    return ['%s=%s' % (key, val) for key, val in sorted(feat_dic.items())]


def get_svm_feat(w2v_dic, window, sent, morp_id):
    """
    get SVM features of given morpheme position from sentence
    :param  w2v_dic:  word2vec dictionary
    :param  sent:     sentence object
    :param  morp_id:  morpheme ID
    :return:          feature vector
    """
    feat_vec = []
    morp = sent.morps[morp_id]
    for win_idx in range(-window, window+1):
        morp_idx = morp.id() + win_idx
        if morp_idx < 0 or morp_idx >= len(sent.morps):
            vec = word2vec.eos(w2v_dic)
        else:
            vec = word2vec.get(w2v_dic, sent.morps[morp_idx].lemma(), sent.morps[morp_idx].tag())
        feat_vec += vec
    return feat_vec
