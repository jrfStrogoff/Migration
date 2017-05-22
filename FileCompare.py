# -*- coding: cp1252 -*-

import difflib


def diff_files(file1, file2):
    return difflib.ndiff(open(file1).readlines(), open(file2).readlines())
    # return difflib.unified_diff(a=open(file1).readlines(), b=open(file2).readlines(), fromfile=file1, tofile=file2)
