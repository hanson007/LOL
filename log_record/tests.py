# -*- coding: UTF-8 -*-
from django.test import TestCase

# Create your tests here.
import datetime,time

d1 = datetime.datetime.now()
# time.sleep(1)
d2 = datetime.datetime.now()
t1 = (d2 - d1).total_seconds()
print d2
print d1
print t1,round(t1, 3)
# print round((d3 - d1).total_seconds(), 3)
# print (d2 - d1).microseconds
# print (d2 - d1).microseconds*0.000001
