#!/usr/bin/python
# -*- coding: utf-8 -*-
"""
    plot.py
    ~~~~~~~~~~~~~~

    A brief description goes here.
"""
import os
import datetime
import random
import time

import numpy
from matplotlib import pyplot


class DstatPlot(object):
    def __init__(self):
        self.fig = pyplot.figure()
        self.sp = self.fig.add_subplot(111)
        self.sp.set_title('Bandwidth')
        self.sp.set_xlabel('time elapsed')
        self.sp.set_ylabel('bytes/s')
        self.linestyles = ['-', '--', '-.', ':',
            '.', ',', 'o', 'v', '^', '<', '>', '1', '2', '3', '4', 's', 'p',
            '*', 'h', 'H', '+', 'x', 'D', 'd', '|', '_']
        random.shuffle(self.linestyles)
        dstat_names = ["time","usr","sys","idl","wai","stl","read","writ","recv","send","in","out","int","csw"]
        dstat_type = ["S14"]
        dstat_type.extend([numpy.float] * 7)
        dstat_type.extend([numpy.int] * 6)
        self.dtype = zip(dstat_names, dstat_type)

    def plot_folder(self, csv_folder="~/dstats/"):
        csv_path = os.path.expanduser(csv_folder)
        for i in os.listdir(csv_path):
            self.plot_file(os.path.join(csv_path, i))

    def plot_file(self, csv_file="~/dstats/dstat.csv"):
        csv_path = os.path.expanduser(csv_file)
        host = os.path.basename(csv_path).split('.')[0]
        data = numpy.genfromtxt(csv_path, self.dtype, delimiter=",", skip_header=6)
        start = time.mktime(datetime.datetime.strptime(data['time'][0], "%d-%m %H:%M:%S").replace(year=2014).timetuple())
        relative_timestamp = [time.mktime(datetime.datetime.strptime(x, "%d-%m %H:%M:%S").replace(year=2014).timetuple()) - start for x in data['time']]
        ls = self.linestyles.pop()
        self.sp.plot(relative_timestamp, data['send'], ls=ls, label="%s:send" % host)
        self.sp.plot(relative_timestamp, data['recv'], ls=ls, label="%s:recv" % host)

    def show(self):
        self.sp.legend()
        return self.fig.show()


def foo():
    dp = DstatPlot()
    dp.plot_folder()
    return dp


def main(argv):
    import time
    d = foo()
    d.show()
    while True:
        time.sleep(1)


if __name__ == '__main__':
    import sys
    main(sys.argv)
