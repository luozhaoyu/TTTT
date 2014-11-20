#!/usr/bin/python
# -*- coding: utf-8 -*-
"""
    fabfile.py
    ~~~~~~~~~~~~~~

    A brief description goes here.
"""
from fabric.api import run, env, roles, execute

env.roledefs = {
    'master': ['macaroni-05'],
    'slave': [
        #'macaroni-01',
        #'macaroni-02',
        'macaroni-03',
        #'macaroni-04',
    ]
    }

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


def start():
    execute(start_master)
    execute(start_slaves)


def stop():
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


def main(argv):
    pass


if __name__ == '__main__':
    import sys
    main(sys.argv)
