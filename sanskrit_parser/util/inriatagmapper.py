# -*- coding: utf-8 -*-
"""
Map tags generated by inriaxmlwrapper to a better set of names

@author: Karthik Madathil(@kmadathil)

"""

from __future__ import print_function
from indic_transliteration import sanscript
from indic_transliteration.sanscript import SCHEMES
from sanskrit_parser.base.sanskrit_base import SanskritImmutableString

inriatags = [('prim', 'प्राथमिकः'),
             ('ca', 'णिजन्तः'),
             ('int', 'यङन्तः'),
             ('des', 'सन्नन्तः'),
             ('prs', 'kartari'),
             ('pas', 'karmaRi'),
             ('sys-md-pr', 'लट्'),
             ('sys-md-ip', 'लोट्'),
             ('sys-md-op', 'विधिलिङ्'),
             ('sys-md-im', 'लङ्'),
             ('sys-tp-fut', 'लृट्'),
             ('sys-tp-prf', 'लिट्'),
             ('sys-tp-aor', 'लुङ्'),
             ('sys-tp-inj', 'आगमाभावयुक्तलुङ्'),
             ('sys-tp-cnd', 'लृङ्'),
             ('sys-tp-ben', 'आशीर्लिङ्'),
             ('sys-pef', 'लुट्'),
             ('fst', 'उत्तमपुरुषः'),
             ('snd', 'मध्यमपुरुषः'),
             ('trd', 'प्रथमपुरुषः'),
             ('na-nom', 'प्रथमाविभक्तिः'),
             ('na-voc', 'संबोधनविभक्तिः'),
             ('na-acc', 'द्वितीयाविभक्तिः'),
             ('na-ins', 'तृतीयाविभक्तिः'),
             ('na-dat', 'चतुर्थीविभक्तिः'),
             ('na-abl', 'पञ्चमीविभक्तिः'),
             ('na-gen', 'षष्ठीविभक्तिः'),
             ('na-loc', 'सप्तमीविभक्तिः'),
             ('sg', 'एकवचनम्'),
             ('du', 'द्विवचनम्'),
             ('pl', 'बहुवचनम्'),
             ('mas', 'पुंल्लिङ्गम्'),
             ('fem', 'स्त्रीलिङ्गम्'),
             ('neu', 'नपुंसकलिङ्गम्'),
             ('dei', 'सङ्ख्या'),
             ('uf', 'अव्ययम्'),
             ('ind', 'क्रियाविशेषणम्'),
             ('interj', 'उद्गारः'),
             ('parti', 'निपातम्'),
             ('prep', 'karmapravacanIyaH'),
             ('conj', 'संयोजकः'),
             ('tasil', 'तसिल्'),
             ('vu', 'अव्ययधातुरूप'),
             ('vu', 'अव्यय'),
             ('iv-inf', 'तुमुन्'),
             ('iv-per', 'per'),
             ('ab', 'अव्ययधातुरूप'),
             ('ab', 'ktvA'),
             ('abs', 'lyap'),
             ('kr', 'kfdantaH'),
             ('ppp', 'karmaRi'),
             ('ppp', 'kta'),
             ('ppa', 'ktavatu'),
             ('ppa', 'kartari'),
             ('pprp', 'SAnac'),
             ('pprp', 'karmaRi'),
             ('ppr', 'kartari'),
             ('ppr-para', 'Satf'),
             ('ppr-atma', 'SAnac'),
             ('ppr', 'kartari'),
             ('ppft', 'kartari'),
             ('ppft-para', 'kvasu'),
             ('ppft-atma', 'kAnac'),
             ('pfutp', 'karmaRi'),
             ('pfutp', 'kftya'),
             ('pfut', 'kartari'),
             ('pfut', 'Bavizyat'),
             ('pfut-para', 'Satf'),
             ('pfut-atma', 'SanaC'),
             ('gya', 'य'),
             ('iya', 'ईय'),
             ('tav', 'तव्य'),
             ('para', 'परस्मैपदम्'),
             ('atma', 'आत्मनेपदम्'),
             ('pas', 'आत्मनेपदम्'),  # ('pa', 'कृदन्तः'),
             ('iic', 'समासपूर्वपदनामपदम्'),
             ('iip', 'समासपूर्वपदकृदन्तः'),
             ('iiv', 'समासपूर्वपदधातुः'),
             ('upsrg', 'उपसर्गः')]


def _inriaTagsToDb(tag):
    # ('tag','ourtag)
    itag = tag[0]
    otag = tag[1]
    if itag.find('-') != -1:
        iset = set(itag.split('-'))
    else:
        iset = set([itag])
    return (iset, SanskritImmutableString(otag, encoding=sanscript.DEVANAGARI))


inriatagdb = list(map(_inriaTagsToDb, inriatags))


def inriaMapTag(tag):
    ''' Map an INRIA tag to our format

    Params:
       tag(tuple) : (<stem>,set([inria tags]))
    Returns
       tuple : (<stem>,set([our tags]))
    '''
    stem = tag[0]
    tset = tag[1]
    olist = []
    for s in inriatagdb:
        if s[0] <= tset:
            olist.append(s[1])
    return (SanskritImmutableString(stem, sanscript.SLP1), set(olist))


def inriaTagMapper(tags):
    ''' Map an INRIA tag to our format

    Params:
       tags: List of INRIA format tags
    Returns
       list[(<stem>,set([our tags])) ...]
    '''
    return list(map(inriaMapTag, tags))


if __name__ == "__main__":
    import sys

    if len(sys.argv) >= 2:
        print(list(map(lambda x: inriaMapTag(eval(x)), sys.argv[1:])))
    else:
        print("Need at least one argument to convert")
