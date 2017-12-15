"""
Created on Jul 7, 2017

@author: alvarna
"""
import pytest
import codecs
import os
import inspect
from sanskrit_parser.lexical_analyzer.sandhi import Sandhi
from sanskrit_parser.base.sanskrit_base import SanskritObject, SLP1, DEVANAGARI
import logging
import json

logger = logging.getLogger(__name__)

@pytest.fixture(scope="module")
def sandhiobj():
    return Sandhi()

def test_sandhi_join(sandhiobj, join_reference):
    objs = map(lambda x:SanskritObject(x, encoding=DEVANAGARI), (join_reference[0]))
    joins = sandhiobj.join(*objs)
    expected = SanskritObject(join_reference[1], encoding=DEVANAGARI).canonical()
    assert expected in joins, u"Join, {}, {}, {}, {}".format(*join_reference)

def test_sandhi_split(sandhiobj, split_reference):
    obj = SanskritObject(split_reference[0], encoding=DEVANAGARI)
    splits = sandhiobj.split_all(obj)
    expected = tuple(map(lambda x:SanskritObject(x, encoding=DEVANAGARI).canonical(), split_reference[1]))
    assert expected in splits, u"Split, {}, {}, {}, {}".format(*split_reference)

def load_file(filename, xfail=False):
    references = []
    with codecs.open(filename, "rb", encoding="utf-8") as f:
        for line in f:
            test = json.loads(line)
            if isinstance(test["input"], list): test["input"] = tuple(test["input"])
            if isinstance(test["expected"], list): test["expected"] = tuple(test["expected"])
            ref = (test["input"], test["expected"], test["file"], test["line"])
            if xfail: ref = pytest.mark.xfail(ref)
            references.append(ref)
    return references

def load_reference_data(passing, failing):
    base_dir = os.path.dirname(os.path.abspath(inspect.getfile(inspect.currentframe())))
    directory = os.path.join(base_dir, "sandhi_test_data")
    
    references = load_file(os.path.join(directory, passing))
    references.extend(load_file(os.path.join(directory, failing), xfail=True))
    return references

def pytest_generate_tests(metafunc):
    if 'join_reference' in metafunc.fixturenames:
        join_references = load_reference_data("sandhi_join_passing.txt", "sandhi_join_failing.txt")
        metafunc.parametrize("join_reference", join_references)
    if 'split_reference' in metafunc.fixturenames:
        split_references = load_reference_data("sandhi_split_passing.txt", "sandhi_split_failing.txt")
        metafunc.parametrize("split_reference", split_references)
