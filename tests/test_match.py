
#!/usr/bin/env python
# coding: utf-8

# Copyright (c) Simula Research Laboratory.
# Distributed under the terms of the Modified BSD License.

import os

import pytest

from globmatch import glob_match
from globmatch.pathutils import SEPARATORS
from globmatch.translation import compile_pattern


def test_glob_match_subentries():
    m = compile_pattern('.git')
    assert m('.git/subdir/entry')


def test_glob_match_bytestring():
    m = compile_pattern(b'.git')
    assert m(b'.git/subdir/entry')

def test_glob_match_incomplete_charpat():
    m = compile_pattern('**/subdir[fe/*.ext')
    assert m('mydir/subdir[fe/myfile.ext')


def test_glob_match_sep_in_charpattern(needs_no_altsep):
    # If \ is not a path sep, it should be valid in char pattern:
    m = compile_pattern(b'dir/mypa[ts][t\\]ern/file')
    assert m(b'dir/mypat\\ern/file')


_glob_patterns = (
    '.config',
    '**/coverage',
    '.git[ia]*',
)

def test_multi_glob_match_first():
    # Check that first pattern of multiple will cause match
    assert glob_match('.config', _glob_patterns)
    assert glob_match('.config/', _glob_patterns)
    assert glob_match('.config/subentry', _glob_patterns)
    assert not glob_match('foo/.config/subentry', _glob_patterns)

def test_multi_glob_match_second():
    # Check that first pattern of multiple will cause match
    assert glob_match('coverage', _glob_patterns)
    assert glob_match('coverage/', _glob_patterns)
    assert glob_match('coverage/foo', _glob_patterns)
    assert glob_match('foo/coverage', _glob_patterns)
    assert glob_match('foo/coverage/subkey', _glob_patterns)


def test_multi_glob_match_third():
    # Check that first pattern of multiple will cause match
    assert glob_match('.gitignore', _glob_patterns)
    assert glob_match('.gitattributes', _glob_patterns)
    assert not glob_match('.git/config', _glob_patterns)
    assert not glob_match('foo/.gitignore', _glob_patterns)

def test_multi_glob_match_several():
    assert glob_match('.config/coverage/foo', _glob_patterns)
