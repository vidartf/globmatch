#!/usr/bin/env python
# coding: utf-8

# Copyright (c) Simula Research Laboratory.
# Distributed under the terms of the Modified BSD License.

import os
import sys

import pytest

from globmatch.pathutils import iexplode_path, explode_path, SEPARATORS


@pytest.fixture(params=SEPARATORS)
def sep(request):
    return request.param

@pytest.fixture(params=(iexplode_path, explode_path))
def explode_fn(request):
    return request.param


def test_explode_empty(explode_fn):
    v = tuple(explode_fn(''))
    assert v == ('',)


def test_explode_root(explode_fn, sep):
    v = tuple(explode_fn(sep))
    assert v == (sep,)


def test_explode_relative_single(explode_fn):
    v = tuple(explode_fn('mydir'))
    assert v == ('mydir',)


def test_explode_absolute_single(explode_fn, sep):
    v = tuple(explode_fn(sep + 'mydir'))
    assert v == (sep, 'mydir',)


def test_explode_relative_double(explode_fn, sep):
    v = tuple(explode_fn(sep.join(('mydir', 'myfile'))))
    assert v == ('mydir', 'myfile')


def test_explode_absolute_double(explode_fn, sep):
    v = tuple(explode_fn(sep + sep.join(('mydir', 'myfile'))))
    assert v == (sep, 'mydir', 'myfile')


def test_explode_relative_triplet(explode_fn, sep):
    v = tuple(explode_fn(sep.join(('mydir', 'subdir', 'myfile.ext'))))
    assert v == ('mydir', 'subdir', 'myfile.ext')


def test_explode_absolute_triplet(explode_fn, sep):
    v = tuple(explode_fn(sep + sep.join(('mydir', 'subdir', 'myfile.ext'))))
    assert v == (sep, 'mydir', 'subdir', 'myfile.ext')


def test_explode_triplet_mixed_sep_absolute_1(needs_altsep, explode_fn):
    v = tuple(explode_fn(os.sep + 'mydir' + os.altsep + 'subdir' + os.sep + 'myfile.ext'))
    assert v == (os.sep, 'mydir', 'subdir', 'myfile.ext')


def test_explode_triplet_mixed_sep_absolute_2(needs_altsep, explode_fn):
    v = tuple(explode_fn(os.altsep + 'mydir' + os.sep + 'subdir' + os.altsep + 'myfile.ext'))
    assert v == (os.altsep, 'mydir', 'subdir', 'myfile.ext')


def test_explode_triplet_mixed_sep_relative_1(needs_altsep, explode_fn):
    v = tuple(explode_fn('mydir' + os.altsep + 'subdir' + os.sep + 'myfile.ext'))
    assert v == ('mydir', 'subdir', 'myfile.ext')


def test_explode_triplet_mixed_sep_relative_2(needs_altsep, explode_fn):
    v = tuple(explode_fn('mydir' + os.sep + 'subdir' + os.altsep + 'myfile.ext'))
    assert v == ('mydir', 'subdir', 'myfile.ext')


def test_explode_relative_dots(explode_fn, sep):
    v = tuple(explode_fn(sep.join(('.', '..', 'sibling', '..', 'myfile.ext'))))
    assert v == ('.', '..', 'sibling', '..', 'myfile.ext')


def test_explode_absolute_triplet(explode_fn, sep):
    v = tuple(explode_fn(sep + sep.join(('.', '..', 'sibling', '..', 'myfile.ext'))))
    assert v == (sep, '.', '..', 'sibling', '..', 'myfile.ext')


def test_explode_incomplete_charpat(explode_fn, sep):
    v = tuple(explode_fn(sep.join(('mydir', 'subdir[fe', 'myfile.ext'))))
    assert v == ('mydir', 'subdir[fe', 'myfile.ext')


@pytest.mark.skipif(sys.platform != 'win32',
                    reason="windows specific test")
def test_explode_drive(explode_fn, sep):
    v = tuple(explode_fn('C:' + sep + 'myentry' + sep + 'sub'))
    assert v == ('C:' + sep, 'myentry', 'sub')


# TODO: Test against interesting characters and escapes
