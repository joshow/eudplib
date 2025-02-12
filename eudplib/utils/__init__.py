#!/usr/bin/python
# -*- coding: utf-8 -*-

"""
Copyright (c) 2014 trgk

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in
all copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN
THE SOFTWARE.
"""

from .ubconv import u2b, b2u, u2utf8
from .binio import b2i1, b2i2, b2i4, i2b1, i2b2, i2b4, bits
from .blockstru import (
    EUDCreateBlock,
    EUDGetLastBlock,
    EUDGetLastBlockOfName,
    EUDPeekBlock,
    EUDPopBlock,
    EUDGetBlockList,
)
from .etc import (
    EPD,
    FlattenList,
    List2Assignable,
    Assignable2List,
    SCMD2Text,
    cachedfunc,
    isStrict,
    setStrict,
    RandList,
)

from .eperror import EPError, EPWarning, ep_assert, ep_eprint, ep_warn

from .exprproxy import ExprProxy, unProxy, isUnproxyInstance
from .etc import find_data_file
