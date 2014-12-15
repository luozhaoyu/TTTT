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
import csv
import StringIO

import argparse

import numpy
from matplotlib import pyplot


class DstatPlot(object):
    def __init__(self, measure, title="Dstat Statistics"):
        #: valid dstat field
        self.measure = measure
        self.fig = pyplot.figure(figsize=(10, 12))
        self.sp = self.fig.add_subplot(111)
        self.sp.set_title(title)
        self.sp.set_xlabel('Time Elapsed')
        self.sp.set_ylabel('Data %s (B/s)' % measure.capitalize())
        self.linestyles = [
            #'-', '--', '-.', ':',
            '-',
            #'.', ',', 'o', 'v', '^', '<', '>', '1', '2', '3', '4', 's', 'p',
            #'*', 'h', 'H', '+', 'x', 'D', 'd', '|', '_'
            ]
        random.shuffle(self.linestyles)
        dstat_names = ["time","usr","sys","idl","wai","hiq", "siq", "read","writ","recv","send","in","out","int","csw"]
        dstat_type = ["S14"]
        dstat_type.extend([numpy.float] * 14)
        #dstat_type.extend([numpy.int] * 6)
        self.dtype = zip(dstat_names, dstat_type)

    def plot_folder(self, csv_folder="~/dstats/", start_time=None, end_time=None):
        csv_path = os.path.expanduser(csv_folder)
        for i in os.listdir(csv_path):
            self.plot_file(os.path.join(csv_path, i), start_time, end_time)

    def plot_file(self, csv_file="~/dstats/dstat.csv", start_time=None, end_time=None):
        csv_path = os.path.expanduser(csv_file)
        host = os.path.basename(csv_path).split('.')[0]
        with open(csv_path, 'r') as f:
            raw_data = f.read()
        cut = -1
        for i in range(6):
            cut = raw_data.index('\n', cut+1)
        raw_data = raw_data[cut+1:]
        csv_buffer = StringIO.StringIO(raw_data)
        reader = csv.DictReader(csv_buffer, delimiter=',', quotechar='"')
        datas = []
        for r in reader:
            try:
                today_time = r['time'].split(' ')[-1]
                if start_time and (today_time < start_time or today_time > end_time):
                    continue
                else:
                    datas.append(float(r[self.measure]))
            except (TypeError, ValueError) as e:
                print e, csv_file, r
        relative_timestamp = range(len(datas))
        ls = self.linestyles[random.randint(0, len(self.linestyles)-1)]
        self.sp.plot(relative_timestamp, datas, ls=ls, label=host)
        self.sp.set_yscale('log')

    def show(self):
        self.sp.legend()
        return self.fig.show()

    def savefig(self, file_path):
        self.sp.legend()
        return self.fig.savefig(file_path)


def plot_dstat(folder='~/dstats', start_time=None, end_time=None):
    dp = DstatPlot('send', title="Dstat Of Network Sends Traffic During Hadoop")
    dp.plot_folder(folder, start_time=start_time, end_time=end_time)
    dp.savefig('dstat_send.png')
    dp = None
    dp = DstatPlot('recv', title="Dstat Of Network Recvs Traffic During Hadoop")
    dp.plot_folder(folder, start_time=start_time, end_time=end_time)
    dp.savefig('dstat_recv.png')
    return dp


def parse(file_path):
    d = {}
    key = ''
    with open(file_path, 'r') as f:
        for line in f:
            content = line.strip()
            if (line.startswith("\t") or line.startswith(" ")):
                if not (content.startswith('at') or content.startswith('.')):
                    if "=" in content:
                        name, value = content.split('=')
                        d[key][name] = int(value)
                    else:
                        key = content
                        d[key] = {}
            elif line.startswith("14"): # this is a hack, I do not want to write regular expression
                ts = time.mktime(datetime.datetime.strptime(content.split(' ')[1], "%H:%M:%S").timetuple())
                d['end_time'] = ts
                if not 'start_time' in d:
                    d['start_time'] = ts
    return d


def parse_folder(folder_path):
    folder_path = os.path.expanduser(folder_path)
    d = {}
    for i in os.listdir(folder_path):
        match = re.search(r'\d+', i)
        if match:
            nodes = int(match.group())
            p = parse(os.path.join(folder_path, i))
            if len(p) > 2: # more than 2 keys: start & end time
                d[nodes] = p
    return d


def plot_variance(folder_path):
    d = parse_folder(folder_path)
    x = d.keys()
    x.sort()
    ys = []
    titles = ['MapDuration', 'ReduceCount', 'ReduceDuration', 'MapCount']
    for t in titles:
        ys.append([numpy.std(d[n][t].values()) for n in x])
    fig = pyplot.figure(figsize=(16, 12))
    for i in range(len(titles)):
        y = ys[i]
        title = titles[i]
        sp = fig.add_subplot(2, 2, i)
        sp.set_title(title)
        sp.set_xlabel('Number of Nodes')
        sp.set_ylabel('Standard Deviation')
        sp.bar(numpy.arange(len(x)), y)
        sp.set_xticks(numpy.arange(len(x)))
        sp.set_xticklabels(x)
        sp.ticklabel_format(style='plain', axis='y')
    fig.savefig('variance.png')
    return fig


def plot_single(folder_path):
    d = parse_folder(folder_path)
    for n in d.keys():
        if not n in [2, 4, 8, 12, 15]:
            del d[n]

    for k in ['MapCount', 'ReduceCount']:
        fig = pyplot.figure(figsize=(20, 16))
        for i, n in enumerate(d.keys()):
            sp = fig.add_subplot(len(d), 1, 1+i)
            sp.set_title("Number of %s Calls Per Node in a %i Node Configuration" % (k.replace('Count', ''), n))
            sp.set_xlabel('Hosts')
            sp.set_ylabel('Number of %s Calls' % k.replace('Count', ''))
            x = [i.split('.')[0].replace('galapagos', 'g').replace('macaroni', 'm',).replace('adelie', 'a') for i in d[n][k].keys()]
            y = d[n][k].values()
            sp.bar(numpy.arange(len(x)), y)
            sp.set_xticks(numpy.arange(len(x)))
            sp.set_xticklabels(x)
            sp.ticklabel_format(style='plain', axis='y')
        fig.subplots_adjust(hspace=0.4)
        fig.savefig('%s_by_nodes.png' % k)


def plot_time(folder_path):
    d = parse_folder(folder_path)
    x = d.keys()
    x.sort()
    map_times = []
    reduce_times = []
    total_times = []
    for i in x:
        mt = d[i]['Job Counters']['Total time spent by all map tasks (ms)'] / 1000
        rt = d[i]['Job Counters']['Total time spent by all reduce tasks (ms)'] / 1000
        map_times.append(mt)
        reduce_times.append(rt)
        total_times.append(mt+rt)
    fig = pyplot.figure()
    sp = fig.add_subplot(2, 1, 1)
    sp.set_title("Map Time Cost")
    sp.set_xlabel('Number of Nodes')
    sp.set_ylabel('Hadoop Execution Time (Seconds)')
    sp.plot(numpy.arange(len(x)), map_times)
    sp.set_xticks(numpy.arange(len(x)))
    sp.set_xticklabels(x)
    sp1 = fig.add_subplot(2, 1, 2)
    sp1.set_title("Reduce Time Cost")
    sp1.set_xlabel('Number of Nodes')
    sp1.set_ylabel('Hadoop Exectuion Time (Seconds)')
    sp1.plot(numpy.arange(len(x)), reduce_times)
    sp1.set_xticks(numpy.arange(len(x)))
    sp1.set_xticklabels(x)
    fig.subplots_adjust(hspace=0.7)
    fig.savefig('MapReduce_time.png')

    lasts = [d[n]['end_time'] - d[n]['start_time'] for n in x]
    fig1 = pyplot.figure()
    sp2 = fig1.add_subplot(1, 1, 1)
    sp2.set_title("Hadoop Execution Time Relative to Node Count")
    sp2.set_xlabel('Number of Nodes')
    sp2.set_ylabel('Hadoop Execution Time (Seconds)')
    sp2.plot(numpy.arange(len(x)), lasts)
    sp2.set_xticks(numpy.arange(len(x)))
    sp2.set_xticklabels(x)
    fig1.savefig('total_time.png')
    return fig1


def main(argv):
    import pprint
    import time
    parser = argparse.ArgumentParser(description="""
        Plots for TTTT""")
    different_actions = parser.add_mutually_exclusive_group()
    different_actions.add_argument('-a', help='draw all', action='store_true')
    different_actions.add_argument('-d', help='draw from dstat', action='store_true')
    different_actions.add_argument('-v', help='plot variance', action='store_true')
    different_actions.add_argument('-t', help='plot time', action='store_true')
    different_actions.add_argument('-s', help='plot each single node time spent', action='store_true')
    different_actions.add_argument('--test', help='', action="store_true")
    parser.add_argument('--file')
    parser.add_argument('--folder', default="./experiments/")
    parser.add_argument('-st', help='start_time: 21:02:17', default=None)
    parser.add_argument('-et', help='end_time: 21:04:27', default=None)
    args = parser.parse_args()
    fig = None
    if args.a:
        plot_dstat(start_time=args.st, end_time=args.et)
        plot_variance(args.folder)
        plot_time(args.folder)
        plot_single(args.folder)
    elif args.d:
        fig = plot_dstat(args.folder, args.st, args.et).fig
    elif args.v:
        fig = plot_variance(args.folder)
    elif args.t:
        fig = plot_time(args.folder)
    elif args.s:
        fig = plot_single(args.folder)
    elif args.test:
        if args.file:
            pprint.pprint(parse(args.file))
        else:
            pprint.pprint(plot_variance(args.folder))
    if fig:
        fig.show()
        while True:
            time.sleep(1)


if __name__ == '__main__':
    import sys
    main(sys.argv)
