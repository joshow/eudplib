#!/usr/bin/python
# -*- coding: utf-8 -*-

'''
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
'''

from .eudfuncn import EUDFuncN
from ... import utils as ut
from .eudv import (
    _VProc,
    EUDVariable,
    SetVariables,
)
from .eudstruct import EUDStruct
from .. import rawtrigger as rt
from ..allocator import Forward


#
# Common argument / returns storage
#

def getArgStorage(argn, _argstorage_dict={}):
    """ Get common arguments storage for argn """
    if argn not in _argstorage_dict:
        _argstorage_dict[argn] = [EUDVariable() for _ in range(argn)]
    return _argstorage_dict[argn]


def getRetStorage(retn, _retstorage_dict={}):
    """ Get common returns storage for retn """
    if retn not in _retstorage_dict:
        _retstorage_dict[retn] = [EUDVariable() for _ in range(retn)]
    return _retstorage_dict[retn]


def fillArguments(f):
    """ Copy values from common argument storage to f._args """
    if f._argn:
        argStorage = getArgStorage(f._argn)
        for farg, arg in zip(f._fargs, argStorage):
            _VProc(arg, arg.QueueAssignTo(farg))


def fillReturns(f):
    """ Copy values from f_rets to common returns storage """
    if f._retn:
        retStorage = getRetStorage(f._retn)
        for fret, ret in zip(f._frets, retStorage):
            _VProc(fret, fret.QueueAssignTo(ret))


def callFuncBody(fstart, fend):
    """ Call function's body triggers """
    fcallend = Forward()

    rt.RawTrigger(
        nextptr=fstart,
        actions=[rt.SetNextPtr(fend, fcallend)]
    )

    fcallend << rt.NextTrigger()


def createIndirectCaller(f, _caller_dict={}):
    """ Create function caller using common argument/return storage """

    # Cache function in _caller_dict. If uncached,
    if f not in _caller_dict:
        rt.PushTriggerScope()
        caller_start = rt.NextTrigger()
        fillArguments(f)
        callFuncBody(f._fstart, f._fend)
        fillReturns(f)
        caller_end = rt.RawTrigger()
        rt.PopTriggerScope()

        _caller_dict[f] = (caller_start, caller_end)

    return _caller_dict[f]


# ---------------------------------


def EUDFuncPtr(argn, retn):
    class PtrDataClass(EUDStruct):
        _fields_ = [
            '_fstart',
            '_fendnext_epd'
        ]

        def __init__(self, f_init=None):
            """ Constructor with function prototype

            :param argn: Number of arguments function can accepy
            :param retn: Number of variables function will return.
            :param f_init: First function
            """

            if f_init:
                if isinstance(f_init, EUDFuncN):
                    self.checkValidFunction(f_init)
                    f_idcstart, f_idcend = createIndirectCaller(f_init)
                    super().__init__([
                        f_idcstart,  # fstart
                        ut.EPD(f_idcend + 4)  # fendnext_epd
                    ])
                else:
                    super().__init__(f_init)

            else:
                super().__init__()

        def checkValidFunction(self, f):
            ut.ep_assert(isinstance(f, EUDFuncN))
            if not f._fstart:
                f._CreateFuncBody()

            f_argn = f._argn
            f_retn = f._retn
            ut.ep_assert(argn == f_argn, "Function with different prototype")
            ut.ep_assert(retn == f_retn, "Function with different prototype")

        def setFunc(self, f):
            """ Set function pointer's target to function

            :param f: Target function
            """
            self.checkValidFunction(f)

            # Build actions
            f_idcstart, f_idcend = createIndirectCaller(f)
            self._fstart = f_idcstart
            self._fendnext_epd = ut.EPD(f_idcend + 4)

        def __lshift__(self, rhs):
            self.setFunc(rhs)

        def __call__(self, *args):
            """ Call target function with given arguments """

            rt.RawTrigger(actions=rt.SetDeaths(2, rt.SetTo, 5, 0))

            if argn:
                argStorage = getArgStorage(argn)
                SetVariables(argStorage, args)

            # Call function
            t, a = Forward(), Forward()
            SetVariables(
                [ut.EPD(t + 4), ut.EPD(a + 16)],
                [self._fstart, self._fendnext_epd]
            )

            fcallend = Forward()
            t << rt.RawTrigger(
                actions=[
                    a << rt.SetNextPtr(0, fcallend),
                    rt.SetDeaths(2, rt.SetTo, 4, 0),
                ]
            )
            fcallend << rt.NextTrigger()

            if retn:
                tmpRets = [EUDVariable() for _ in range(retn)]
                retStorage = getRetStorage(retn)
                SetVariables(tmpRets, retStorage)
                return ut.List2Assignable(tmpRets)

    return PtrDataClass
