# -*- coding: utf-8 -*-
from sanskrit_parser import enable_console_logger, enable_file_logger
from sanskrit_parser.base.sanskrit_base import SLP1, DEVANAGARI
import sanskrit_parser.generator.sutra as sutra
from sanskrit_parser.generator.paninian_object import PaninianObject
from sanskrit_parser.generator.prakriya import Prakriya, PrakriyaVakya
from sanskrit_parser.generator.pratyaya import *
from sanskrit_parser.generator.dhatu import *
from sanskrit_parser.generator.pratipadika import *
from conftest import run_test, check_vibhakti, generate_vibhakti, test_prakriya

import logging
#logging.basicConfig(level=logging.INFO)
enable_console_logger()
enable_file_logger(level=logging.DEBUG)

test_list = [
    (ava, (AN, "ihi"), "avehi"),
    # [rAjan, wA, "rAjYA"], # 6.4.134
    # [yUza, wA, ["yUzRA", "yUzeRa"]], # 6.1.63, 6.4.134
    # [rAjan, ByAm, "rAjaByAm"], # 6.2.7
    # [yUza, ByAm, ["yUzaByAm", "yUzAByAm"]], # 6.2.7
    # [rAjan, Ni, ["rAjani", "rAjYi"]], # 6.4.136
    # [yUza, Ni, ["yUzaRi", "yUzRi", "yUze"]], # 6.1.63, 6.4.136
]

test_list_d = [
]


viBakti = {}
prAtipadika = {}
encoding = {}

# prAtipadika["rAma"] = rAma
# viBakti["rAma"] = [
#     ["रामः", "रामौ", "रामाः"],
#     ["रामम्", "रामौ", "रामान्"],
#     ["रामेण", "रामाभ्याम्", "रामैः"],
#     ["रामाय", "रामाभ्याम्", "रामेभ्यः"],
#     [["रामात्", "रामाद्"], "रामाभ्याम्", "रामेभ्यः"],
#     ["रामस्य", "रामयोः", "रामाणाम्"],
#     ["रामे", "रामयोः", "रामेषु"],
#     ["राम", "रामौ", "रामाः"],
# ]

# prAtipadika["sarva"] = sarva
# viBakti["sarva"] = [
#     ["सर्वः", "सर्वौ", "सर्वे"],
#     ["सर्वम्", "सर्वौ", "सर्वान्"],
#     ["सर्वेण", "सर्वाभ्याम्", "सर्वैः"],
#     ["सर्वस्मै", "सर्वाभ्याम्", "सर्वेभ्यः"],
#     [["सर्वस्मात्", "सर्वस्माद्"], "सर्वाभ्याम्", "सर्वेभ्यः"],
#     ["सर्वस्य", "सर्वयोः", "सर्वेषाम्"], 
#     ["सर्वस्मिन्", "सर्वयोः", "सर्वेषु "],
# ]

# prAtipadika["pAda"] = pAda
# viBakti["pAda"] = [
#     ["पादः", "पादौ", "पादाः"],
#     ["पादम्", "पादौ", ["पादान्", "पदः"]],
#     [["पादेन", "पदा"], ["पादाभ्याम्", "पद्भ्याम्"], ["पादैः", "पद्भिः"]],
#     [["पादाय", "पदे"], ["पादाभ्याम्", "पद्भ्याम्"], ["पादेभ्यः", "पद्भ्यः"]],
#     [["पादात्", "पादाद्", "पदः"], ["पादाभ्याम्", "पद्भ्याम्"], ["पादेभ्यः", "पद्भ्यः"]],
#     [["पादस्य", "पदः"], ["पादयोः", "पदोः"], ["पादानाम्", "पदाम्"]],
#     [["पादे", "पदि"], ["पादयोः", "पदोः"], ["पादेषु", "पत्सु"]],
#     ["पादः", "पादौ", "पादाः"],
# ]

# prAtipadika["yUza"] = yUza
# viBakti["yUza"] = [
#     ["यूषः", "यूषौ", "यूषाः"],
#     ["यूषम्", "यूषौ", ["यूषान्", "यूष्णः"]],
#     [["यूषेण", "यूष्णा"], ["यूषाभ्याम्", "यूषभ्याम्"], ["यूषैः", "यूषभिः"]],
#     [["यूषाय", "यूष्णे"], ["यूषाभ्याम्", "यूषभ्याम्"], ["यूषेभ्यः", "यूषभ्यः"]],
#     [["यूषात्", "यूषाद्", "यूष्णः"], ["यूषाभ्याम्", "यूषभ्याम्"], ["यूषेभ्यः", "यूषभ्यः"]],
#     [["यूषस्य", "यूष्णः"], ["यूषयोः", "यूष्णोः"], ["यूषाणाम्", "यूष्णाम्"]],
#     [["यूषे", "यूषणि", "यूष्णि"], ["यूषयोः", "यूष्णोः"], ["यूषेषु", "यूषसु"]],
#     ["यूष", "यूषौ", "यूषाः"],
# ]

# prAtipadika["saKi"] = saKi
# viBakti["saKi"] = [
#     ["सखा", "सखायौ", "सखायः"],
#     ["सखायम्", "सखायौ", "सखीन्"],
#     ["सख्या", "सखिभ्याम्", "सखिभिः"],
#     ["सख्ये", "सखिभ्याम्", "सखिभ्यः"],
#     ["सख्युः", "सखिभ्याम्", "सखिभ्यः"],
#     ["सख्युः", "सख्योः", "सखीनाम्"],
#     ["सख्यौ", "सख्योः", "सखिषु"],
#     ["सखे", "सखायौ", "सखायः"],
# ]

# prAtipadika["tri"] = tri
# viBakti["tri"] = [
#     [None, None, "त्रयः"],
#     [None, None, "त्रीन्"],
#     [None, None, "त्रिभिः"],
#     [None, None, "त्रिभ्यः"],
#     [None, None, "त्रिभ्यः"],
#     [None, None, "त्रयाणाम्"],
#     [None, None, "त्रिषु"],
#     [None, None, "त्रयः"],
# ]

# prAtipadika["kati"] = kati
# viBakti["kati"] = [
#     [None, None, "कति"],
#     [None, None, "कति"],
#     [None, None, "कतिभिः"],
#     [None, None, "कतिभ्यः"],
#     [None, None, "कतिभ्यः"],
#     [None, None, "कतीनाम्"],
#     [None, None, "कतिषु"],
#     [None, None, "कति"],
# ]

# prAtipadika["ramA"] = ramA
# viBakti["ramA"] = [
#      ["रमा", "रमे", "रमाः"],
#      ["रमाम्", "रमे", "रमाः"],
#      ["रमया", "रमाभ्याम्", "रमाभिः"],
#      ["रमायै", "रमाभ्याम्", "रमाभ्यः"],
#      ["रमायाः", "रमाभ्याम्", "रमाभ्यः"],
#      ["रमायाः", "रमयोः", "रमाणाम्"],
#      ["रमायाम्", "रमयोः", "रमासु"],
#      ["रमे", "रमे", "रमाः"]
# ]

# prAtipadika["nAsikA"] = nAsikA
# encoding["nAsikA"] = SLP1
# viBakti["nAsikA"] = [
# ['nAsikA', 'nAsike', 'nAsikAH'],
# ['nAsikAm', 'nAsike', ['nasaH', 'nAsikAH']],
# [['nasA', 'nAsikayA'], ['nAsikAByAm', 'noByAm'], ['nAsikABiH', 'noBiH']],
# [['nase', 'nAsikAyE'], ['nAsikAByAm', 'noByAm'], ['nAsikAByaH', 'noByaH']],
# [['nasaH', 'nAsikAyAH'], ['nAsikAByAm', 'noByAm'], ['nAsikAByaH', 'noByaH']],
# [['nasaH', 'nAsikAyAH'], ['nasoH', 'nAsikayoH'], ['nasAm', 'nAsikAnAm']],
# [['nAsikAyAm', 'nasi'], ['nasoH', 'nAsikayoH'], ['nAsikAsu', 'naHsu', 'nassu']],
# ['nAsike', 'nAsike', 'nAsikAH'],
# ]
prAtipadika["Denu"] = Denu
viBakti["Denu"] = [
['धेनुः', 'धेनू', 'धेनवः'],
['धेनुम्', 'धेनू', 'धेनूः'],
['धेन्वा', 'धेनुभ्याम्', 'धेनुभिः'],
[['धेनवे', 'धेन्वै'], 'धेनुभ्याम्', 'धेनुभ्यः'],
[['धेनोः', 'धेन्वाः'], 'धेनुभ्याम्', 'धेनुभ्यः'],
[['धेनोः', 'धेन्वाः'], 'धेन्वोः', 'धेनूनाम्'],
[['धेनौ', 'धेन्वाम्'], 'धेन्वोः', 'धेनुषु'],
['धेनो', 'धेनू', 'धेनवः'],
]

prAtipadika["svayamBU"] = svayamBU
viBakti["svayamBU"] = [
['स्वयम्भूः', 'स्वयम्भुवौ', 'स्वयम्भुवः'],
['स्वयम्भुवम्', 'स्वयम्भुवौ', 'स्वयम्भुवः'],
['स्वयम्भुवा', 'स्वयम्भूभ्याम्', 'स्वयम्भूभिः'],
[['स्वयम्भुवे', 'स्वयम्भुवै'], 'स्वयम्भूभ्याम्', 'स्वयम्भूभ्यः'],
[['स्वयम्भुवः', 'स्वयम्भुवाः'], 'स्वयम्भूभ्याम्', 'स्वयम्भूभ्यः'],
[['स्वयम्भुवः', 'स्वयम्भुवाः'], 'स्वयम्भुवोः', ['स्वयम्भुवाम्', 'स्वयम्भूनाम्']],
[['स्वयम्भुवाम्', 'स्वयम्भुवि'], 'स्वयम्भुवोः', 'स्वयम्भूषु'],
['स्वयम्भूः', 'स्वयम्भुवौ', 'स्वयम्भुवः'],
]

prAtipadika["varzABU"] = varzABU
viBakti["varzABU"] = [
     ["वर्षाभूः", "वर्षाभ्वौ", "वर्षाभ्वः"],
     ["वर्षाभ्वम्", "वर्षाभ्वौ", "वर्षाभ्वः"],
     ["वर्षाभ्वा", "वर्षाभूभ्याम्", "वर्षाभूभिः"],
     ["वर्षाभ्वे", "वर्षाभूभ्याम्", "वर्षाभूभ्यः"],
     ["वर्षाभ्वः", "वर्षाभूभ्याम्", "वर्षाभूभ्यः"],
     ["वर्षाभ्वः", "वर्षाभ्वोः", "वर्षाभ्वाम्"],
     ["वर्षाभ्वि", "वर्षाभ्वोः", "वर्षाभूषु"],
     ["वर्षाभूः", "वर्षाभ्वौ", "वर्षाभ्वः"],
]

prAtipadika["KalapU"] = KalapU
viBakti["KalapU"] = [
     ["खलपूः", "खलप्वौ", "खलप्वः"],
     ["खलप्वम्", "खलप्वौ", "खलप्वः"],
     ["खलप्वा", "खलपूभ्याम्", "खलपूभिः"],
     ["खलप्वे", "खलपूभ्याम्", "खलपूभ्यः"],
     ["खलप्वः", "खलपूभ्याम्", "खलपूभ्यः"],
     ["खलप्वः", "खलप्वोः", "खलप्वाम्"],
     ["खलप्वि", "खलप्वोः", "खलपूषु"],
     ["खलपूः", "खलप्वौ", "खलप्वः"],
]

prAtipadika["senAnI"] = senAnI
viBakti["senAnI"] = [
     ["senAnIH", "senAnyO", "senAnyaH"],
     ["senAnyam", "senAnyO", "senAnyaH"],
     ["senAnyA", "senAnIByAm", "senAnIBiH"],
     ["senAnye", "senAnIByAm", "senAnIByaH"],
     ["senAnyaH", "senAnIByAm", "senAnIByaH"],
     ["senAnyaH", "senAnyoH", "senAnyAm"],
     ["senAnyAm", "senAnyoH", "senAnIzu"],
     ["senAnIH", "senAnyO", "senAnyaH"],
]
encoding["senAnI"] = SLP1

prAtipadika["nI"] = nI
viBakti["nI"] = [
['नीः', 'नियौ', 'नियः'],
['नियम्', 'नियौ', 'नियः'],
['निया', 'नीभ्याम्', 'नीभिः'],
[['निये', 'नियै'], 'नीभ्याम्', 'नीभ्यः'],
[['नियः', 'नियाः'], 'नीभ्याम्', 'नीभ्यः'],
[['नियः', 'नियाः'], 'नियोः', ['नियाम्', 'नीनाम्']],
[['नियाम्', 'नियाम्'], 'नियोः', 'नीषु'],
['नीः', 'नियौ', 'नियः'],
]

from sutras_yaml import sutra_list
test_prakriya(sutra_list, test_list, test_list_d)
for v in viBakti:
    if v in encoding:
        check_vibhakti(generate_vibhakti(prAtipadika[v], viBakti[v],
                                         encoding[v]), sutra_list, encoding[v])
    else:
        check_vibhakti(generate_vibhakti(prAtipadika[v], viBakti[v]),
                       sutra_list)


