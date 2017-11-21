#!/usr/bin/env python
# coding: utf-8

# Copyright (c) Simula Research Laboratory.
# Distributed under the terms of the Modified BSD License.

"""Utilities for matching a path against globs."""

from functools import lru_cache
import os
import re

from .pathutils import iexplode_path


SEPARATORS = os.sep if os.sep == os.altsep else os.sep + os.altsep


@lru_cache(maxsize=256, typed=True)
def compile_pattern(pat):
    """Translate and compile a glob pattern to a regular expression matcher."""
    if isinstance(pat, bytes):
        pat_str = pat.decode('ISO-8859-1')
        res_str = translate_glob(os.path.normcase(pat_str))
        res = res_str.encode('ISO-8859-1')
    else:
        res = translate_glob(os.path.normcase(pat))
    return re.compile(res).match


def translate_glob(pat):
    """Translate a glob PATTERN to a regular expression."""
    translated_parts = []
    for part in iexplode_path(pat):
        translated_parts.append(translate_glob_part(part))
    os_sep_class = '[%s]' % re.escape(SEPARATORS)
    res = os_sep_class.join(translated_parts)
    res = '{res}({os_sep_class}?.*)?\\Z(?ms)'.format(res=res, os_sep_class=os_sep_class)
    # in the future (py 3.6+):
    # res = f'{res}({os_sep_class}?.*)?\\Z(?ms)'
    return res


def translate_glob_part(pat):
    """Translate a glob PATTERN PART to a regular expression."""
    # Code modified from Python 3 standard lib fnmatch:
    if pat == '**':
        return '.*'
    i, n = 0, len(pat)
    res = []
    while i < n:
        c = pat[i]
        i = i+1
        if c == '*':
            # Match anything but path separators:
            res.append('[^%s]*' % SEPARATORS)
        elif c == '?':
            res.append('[^%s]?' % SEPARATORS)
        elif c == '[':
            j = i
            if j < n and pat[j] == '!':
                j = j+1
            if j < n and pat[j] == ']':
                j = j+1
            while j < n and pat[j] != ']':
                j = j+1
            if j >= n:
                res.append('\\[')
            else:
                stuff = pat[i:j].replace('\\', '\\\\')
                i = j+1
                if stuff[0] == '!':
                    stuff = '^' + stuff[1:]
                elif stuff[0] == '^':
                    stuff = '\\' + stuff
                res.append('[%s]' % stuff)
        else:
            res.append(re.escape(c))
    return ''.join(res)
