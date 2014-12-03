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
import re

import argparse

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

    def savefig(self, file_path):
        return self.fig.savefig(file_path)


def foo():
    dp = DstatPlot()
    dp.plot_folder()
    return dp


def parse(file_path):
    d = {}
    key = ''
    with open(file_path, 'r') as f:
        for line in f:
            content = line.strip()
            if (line.startswith("\t") or line.startswith(" ")) and\
                not (content.startswith('at') or content.startswith('.')):
                if "=" in content:
                    name, value = content.split('=')
                    d[key][name] = int(value)
                else:
                    key = content
                    d[key] = {}
    return d


def parse_folder(folder_path):
    folder_path = os.path.expanduser(folder_path)
    d = {}
    for i in os.listdir(folder_path):
        nodes = int(re.search(r'\d+', i).group())
        p = parse(os.path.join(folder_path, i))
        if p:
            d[nodes] = p
    return d


def plot_variance(folder_path):
    d = parse_folder(folder_path)
    x = d.keys()
    x.sort()
    ys = []
    titles = ['MapCount', 'ReduceCount', 'MapDuration', 'ReduceDuration']
    for t in titles:
        ys.append([numpy.std(d[n][t].values()) for n in x])
    fig = pyplot.figure()
    for i in range(len(titles)):
        y = ys[i]
        title = titles[i]
        sp = fig.add_subplot(2, 2, i)
        sp.set_title(title)
        sp.set_xlabel('number of nodes')
        sp.set_ylabel('standard deviation')
        sp.bar(numpy.arange(len(x)), y)
        sp.set_xticks(numpy.arange(len(x)))
        sp.set_xticklabels(x)
    fig.savefig('variance.png')
    return fig


def plot_single(folder_path):
    d = parse_folder(folder_path)
    fig = pyplot.figure()
    for i, n in enumerate(d.keys()):
        sp = fig.add_subplot(len(d), 1, 1 + i)
        sp.set_title("%i hosts" % n)
        sp.set_xlabel('hosts names')
        sp.set_ylabel('milliseconds')
        x = [i.split('.')[0] for i in d[n]['MapDuration'].keys()]
        y = d[n]['MapDuration'].values()
        sp.bar(numpy.arange(len(x)), y)
        sp.set_xticks(numpy.arange(len(x)))
        sp.set_xticklabels(x)
    fig.savefig('single.png')
    return fig


def plot_time(folder_path):
    d = parse_folder(folder_path)
    x = d.keys()
    x.sort()
    map_times = []
    reduce_times = []
    total_times = []
    for i in x:
        mt = d[i]['Job Counters']['Total time spent by all map tasks (ms)']
        rt = d[i]['Job Counters']['Total time spent by all reduce tasks (ms)']
        map_times.append(mt)
        reduce_times.append(rt)
        total_times.append(mt+rt)
    fig = pyplot.figure()
    sp = fig.add_subplot(3, 1, 1)
    sp.set_title("Map Time Cost")
    sp.set_xlabel('number of nodes')
    sp.set_ylabel('milliseconds')
    sp.plot(numpy.arange(len(x)), map_times)
    sp.set_xticks(numpy.arange(len(x)))
    sp.set_xticklabels(x)
    sp1 = fig.add_subplot(3, 1, 2)
    sp1.set_title("Reduce Time Cost")
    sp1.set_xlabel('number of nodes')
    sp1.set_ylabel('milliseconds')
    sp1.plot(numpy.arange(len(x)), reduce_times)
    sp1.set_xticks(numpy.arange(len(x)))
    sp1.set_xticklabels(x)
    sp2 = fig.add_subplot(3, 1, 3)
    sp2.set_title("Total Time Cost")
    sp2.set_xlabel('number of nodes')
    sp2.set_ylabel('milliseconds')
    sp2.plot(numpy.arange(len(x)), total_times)
    sp2.set_xticks(numpy.arange(len(x)))
    sp2.set_xticklabels(x)
    fig.savefig('time.png')
    return fig


def main(argv):
    import pprint
    import time
    parser = argparse.ArgumentParser(description="""
        Plots for TTTT""")
    different_actions = parser.add_mutually_exclusive_group()
    different_actions.add_argument('-d', help='draw from dstat')
    different_actions.add_argument('-v', help='plot variance', action='store_true')
    different_actions.add_argument('-t', help='plot time', action='store_true')
    different_actions.add_argument('-s', help='plot each single node time spent', action='store_true')
    different_actions.add_argument('--test', help='', action="store_true")
    parser.add_argument('--file')
    parser.add_argument('--folder', default="./experiments/")
    args = parser.parse_args()
    if args.d:
        dp = DstatPlot()
        dp.plot_folder()
        dp.savefig('dstat.png')
        dp.show()
    elif args.v:
        plot_variance(args.folder).show()
    elif args.t:
        plot_time(args.folder).show()
    elif args.s:
        plot_single(args.folder).show()
    elif args.test:
        if args.file:
            pprint.pprint(parse(args.file))
        else:
            pprint.pprint(plot_variance(args.folder))
    while True:
        time.sleep(1)


if __name__ == '__main__':
    import sys
    main(sys.argv)
