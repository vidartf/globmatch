#!/usr/bin/env python
# coding: utf-8

# Copyright (c) Simula Research Laboratory.
# Distributed under the terms of the Modified BSD License.

from globmatch.pathutils import SEPARATORS
from globmatch.translation import translate_glob, translate_glob_part, double_start_re

NON_SEP_CHAR = '[^%s]' % SEPARATORS


def test_part_doublestar():
    assert translate_glob_part('**') == double_start_re


def test_part_star():
    assert translate_glob_part('*') == '%s*' % NON_SEP_CHAR


def test_part_question():
    assert translate_glob_part('?') == '%s?' % NON_SEP_CHAR


# For blocks, only check that they integrate correctly
# with other parts. Trust python implementation.

def test_part_block():
    assert translate_glob_part('[!]sder]') == '[^]sder]'

def test_part_block_hat():
    assert translate_glob_part('[^sder]') == '[\\^sder]'


def test_mixed_parts():
    t = translate_glob_part('bob*cat??tree**[ty]free')
    assert t == 'bob{nsc}*cat{nsc}?{nsc}?tree{nsc}*{nsc}*[ty]free'.format(nsc=NON_SEP_CHAR)

