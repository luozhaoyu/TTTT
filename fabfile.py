#!/usr/bin/python
# -*- coding: utf-8 -*-
"""
    fabfile.py
    ~~~~~~~~~~~~~~

    A brief description goes here.
"""
from subprocess import check_call
from fabric.api import run, env, roles, execute
from fabric.api import local, settings


try:
    from config import MACHINES
    from config import COUNT
except ImportError as e:
    print "You should cp config.py.sample config.py, and modify it then"
    raise e

env.roledefs = MACHINES
#env.roledefs = {
#    'master': ['adelie-05'],
#    'slave': [
#        #'macaroni-01',
#        'adelie-02',
#        'adelie-03'
#        #'macaroni-04',
#    ]
#    }

@roles('master')
def init_master():
    run("rm -rf /tmp/dfs")
    run("mkdir -p /tmp/dfs/data")
    run("cp -r ~/hadoop /tmp/dfs/")
    run("/tmp/dfs/hadoop/bin/hdfs namenode -format")


@roles('slave')
def init_slaves():
    run("rm -rf /tmp/dfs")
    run("mkdir -p /tmp/dfs/data")
    run("cp -r ~/hadoop /tmp/dfs/")


def init():
    execute(init_master)
    execute(init_slaves)
    with settings(warn_only=True):
        local("mkdir ~/dstats")


def start():
    execute(start_master)
    execute(start_slaves)
    execute(start_dstat)


def stop():
    execute(stop_dstat)
    execute(stop_slaves)
    execute(stop_master)


def restart():
    execute(stop)
    execute(start)


@roles('master')
def start_master():
    run("/tmp/dfs/hadoop/sbin/hadoop-daemon.sh --config /tmp/dfs/hadoop/etc/hadoop/ start namenode")
    run("/tmp/dfs/hadoop/sbin/yarn-daemon.sh --config /tmp/dfs/hadoop/etc/hadoop/ start resourcemanager")
    run("/tmp/dfs/hadoop/sbin/yarn-daemon.sh --config /tmp/dfs/hadoop/etc/hadoop/ start proxyserver")
    run("/tmp/dfs/hadoop/sbin/mr-jobhistory-daemon.sh --config /tmp/dfs/hadoop/etc/hadoop/ start historyserver")


@roles('master')
def stop_master():
    run("/tmp/dfs/hadoop/sbin/hadoop-daemon.sh --config /tmp/dfs/hadoop/etc/hadoop/ stop namenode")
    run("/tmp/dfs/hadoop/sbin/yarn-daemon.sh --config /tmp/dfs/hadoop/etc/hadoop/ stop resourcemanager")
    run("/tmp/dfs/hadoop/sbin/yarn-daemon.sh --config /tmp/dfs/hadoop/etc/hadoop/ stop proxyserver")
    run("/tmp/dfs/hadoop/sbin/mr-jobhistory-daemon.sh --config /tmp/dfs/hadoop/etc/hadoop/ stop historyserver")


@roles('slave')
def start_slaves():
    run("/tmp/dfs/hadoop/sbin/hadoop-daemon.sh --config /tmp/dfs/hadoop/etc/hadoop/ start datanode")
    run("/tmp/dfs/hadoop/sbin/yarn-daemon.sh --config /tmp/dfs/hadoop/etc/hadoop/ start nodemanager")


@roles('slave')
def stop_slaves():
    run("/tmp/dfs/hadoop/sbin/hadoop-daemon.sh --config /tmp/dfs/hadoop/etc/hadoop/ stop datanode")
    run("/tmp/dfs/hadoop/sbin/yarn-daemon.sh --config /tmp/dfs/hadoop/etc/hadoop/ stop nodemanager")


@roles('slave', 'master')
def start_dstat(count=COUNT):
    check_call("ssh -f %s nohup ~/dstat -ta --output ~/dstats/%s.csv 1 %i >& /dev/null < /dev/null &"
        % (env.host_string, env.host_string, count), shell=True)


@roles('slave', 'master')
def stop_dstat(count=COUNT):
    run("pkill -f dstat", warn_only=True)


def main(argv):
    pass


if __name__ == '__main__':
    import sys
    main(sys.argv)
