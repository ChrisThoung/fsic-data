# -*- coding: utf-8 -*-


import os

import numpy as np
from pandas import DataFrame
from pandas.util.testing import assert_frame_equal
import pandas as pd

from nose.tools import with_setup, raises

from FSICData.ons import csv as reader


def setup():
    global test_input_data
    test_input_data = '''\
,ABCD,EFGH,IJKL,MNOP,QRST,UVWX
"2000",0,,,,10,0
"2001",1,,,,20,-11
"2002",2,,,,30,-23
"2003",3,,,,,-35
"2004",4,,,,50,-47
"2005",5,,,,,-59
"2006",6,,,,60,-71
"2007",7,,,,70,-83
"2008",8,,,,80,-95
"2009",9,,,,90,-107
"2010",10,,,,100,-119
"2000 Q1",,0,,,,9
"2000 Q2",,0.25,,,,6
"2000 Q3",,0.5,,,,3
"2000 Q4",,0.75,,,,0
"2001 Q1",,1,,,,-2
"2001 Q2",,1.25,,,,-5
"2001 Q3",,1.5,,,,-8
"2001 Q4",,1.75,,,,-11
"2002 Q1",,2,,,,-14
"2002 Q2",,2.25,,,,-17
"2002 Q3",,2.5,,,,-20
"2002 Q4",,2.75,,,,-23
"2003 Q1",,3,,,,-26
"2003 Q2",,3.25,,,,-29
"2003 Q3",,3.5,,,,-32
"2003 Q4",,3.75,,,,-35
"2004 Q1",,4,,,,-38
"2004 Q2",,4.25,,,,-41
"2004 Q3",,4.5,,,,-44
"2004 Q4",,4.75,,,,-47
"2005 Q1",,5,,,,-50
"2005 Q2",,5.25,,,,-53
"2005 Q3",,5.5,,,,-56
"2005 Q4",,5.75,,,,-59
"2000 JAN",,,0,,,0
"2000 FEB",,,1,,,-1
"2000 MAR",,,2,,,-2
"2000 APR",,,3,,,-3
"2000 MAY",,,4,,,-4
"2000 JUN",,,5,,,-5
"2000 JUL",,,6,,,-6
"2000 AUG",,,7,,,-7
"2000 SEP",,,8,,,-8
"2000 OCT",,,9,,,-9
"2000 NOV",,,10,,,-10
"2000 DEC",,,11,,,-11
"2001 JAN",,,12,,,-12
"2001 FEB",,,13,,,-13
"2001 MAR",,,14,,,-14
"2001 APR",,,15,,,-15
"2001 MAY",,,16,,,-16
"2001 JUN",,,17,,,-17
"2001 JUL",,,18,,,-18
"2001 AUG",,,19,,,-19
"2001 SEP",,,20,,,-20
"2001 OCT",,,21,,,-21
"2001 NOV",,,22,,,-22
"2001 DEC",,,23,,,-23
"2002 JAN",,,24,,,-24
"2002 FEB",,,25,,,-25
"2002 MAR",,,26,,,-26
"2002 APR",,,27,,,-27
"2002 MAY",,,28,,,-28
"2002 JUN",,,29,,,-29
"2002 JUL",,,30,,,-30
"2002 AUG",,,31,,,-31
"2002 SEP",,,32,,,-32
"2002 OCT",,,33,,,-33
"2002 NOV",,,34,,,-34
"2002 DEC",,,35,,,-35

© Crown Copyright

ABCD,"First test series"
,seasonal_adjustment='SA'
,base_period='2000'
,price='CONS'
,index_period='-'
EFGH,"Second test series"
,seasonal_adjustment='NSA'
,base_period='-'
,price='CURR'
,index_period='-'
IJKL,"Third test series"
,seasonal_adjustment='NSA'
,base_period='-'
,price='CURR'
,index_period='2000'
MNOP,"Fourth test series"
,seasonal_adjustment='NSA'
,base_period='-'
,price='CURR'
,index_period='2000Jan'
QRST,"Fifth test series"
,seasonal_adjustment='SA'
,base_period='2000'
,price='CONS'
,index_period='2000'
UVWX,"Sixth test series"
,seasonal_adjustment='SA'
,base_period='2000'
,price='DEFL'
,index_period='2000'
'''


if __name__ == '__main__':
    import nose
    nose.runmodule()
