
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
    compile_pattern.cache_clear()
    m = compile_pattern('.git')
    assert not m('.git/subdir/entry')
    m = compile_pattern('.git/**')
    assert m('.git/subdir/entry')
    m = compile_pattern('.git', subentries_match=True)
    assert m('.git/subdir/entry')


def test_glob_match_bytestring():
    compile_pattern.cache_clear()
    m = compile_pattern(b'.git', subentries_match=True)
    assert m(b'.git/subdir/entry')


def test_glob_match_incomplete_charpat():
    compile_pattern.cache_clear()
    m = compile_pattern('**/subdir[fe/*.ext')
    assert m('mydir/subdir[fe/myfile.ext')


def test_glob_match_sep_in_charpattern(needs_no_altsep):
    compile_pattern.cache_clear()
    # If \ is not a path sep, it should be valid in char pattern:
    m = compile_pattern(b'dir/mypa[ts][t\\]ern/file')
    assert m(b'dir/mypat\\ern/file')


def test_glob_match_root():
    compile_pattern.cache_clear()
    m = compile_pattern('**/.git')
    assert not m('/.git/gitconfig')
    m = compile_pattern('**/.git', subentries_match=True)
    assert m('/.git/gitconfig')

def test_glob_match_single_star_no_recurse():
    compile_pattern.cache_clear()
    m = compile_pattern('dir/*')
    assert m('dir/subentry')
    assert not m('dir/subentry/subsub')

_glob_patterns = (
    '.config',
    '**/coverage/**',
    '.git[ia]*',
)

def test_multi_glob_match_first():
    compile_pattern.cache_clear()
    # Check that first pattern of multiple will cause match
    assert glob_match('.config', _glob_patterns)
    assert glob_match('.config', _glob_patterns, subentries_match=True)
    assert glob_match('.config/', _glob_patterns)
    assert not glob_match('.config/subentry', _glob_patterns)
    assert glob_match('.config/subentry', _glob_patterns, subentries_match=True)
    assert not glob_match('foo/.config/subentry', _glob_patterns)

def test_multi_glob_match_second():
    compile_pattern.cache_clear()
    # Check that first pattern of multiple will cause match
    assert not glob_match('coverage', _glob_patterns)
    assert not glob_match('coverage/', _glob_patterns)
    assert glob_match('coverage/foo', _glob_patterns)
    assert glob_match('coverage/foo', _glob_patterns, subentries_match=True)
    assert not glob_match('foo/coverage', _glob_patterns)
    assert not glob_match('foo/coverage/', _glob_patterns)
    assert glob_match('foo/coverage/subkey', _glob_patterns)
    assert glob_match('foo/coverage/subkey', _glob_patterns, subentries_match=True)


def test_multi_glob_match_third():
    compile_pattern.cache_clear()
    # Check that first pattern of multiple will cause match
    assert glob_match('.gitignore', _glob_patterns)
    assert glob_match('.gitattributes', _glob_patterns)
    assert not glob_match('.git/config', _glob_patterns)
    assert not glob_match('foo/.gitignore', _glob_patterns)

def test_multi_glob_match_several():
    compile_pattern.cache_clear()
    # Matches **/coverage/** :
    assert glob_match('.config/coverage/foo', _glob_patterns)
    # Matches .config :
    assert glob_match('.config/coverage/foo', _glob_patterns, subentries_match=True)


def test_match_dot_files():
    compile_pattern.cache_clear()
    assert glob_match('foo/.dotfile', ["**/.*"])
    assert glob_match('.dotfile', ["**/.*"])
    assert glob_match('.dotfile', ["**/.dotfile"])
    assert not glob_match('foo/file.py', [r"**/.*"])

