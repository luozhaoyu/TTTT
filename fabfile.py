#!/usr/bin/python
# -*- coding: utf-8 -*-
"""
    fabfile.py
    ~~~~~~~~~~~~~~

    A brief description goes here.
"""
import os
import hashlib
from subprocess import check_call
from fabric.api import run, env, roles, execute
from fabric.api import local, settings, parallel


try:
    from config import MACHINES
    from config import COUNT
    from config import UPLOAD_FOLDER
    from password import PASSWORD
except ImportError as e:
    print "You should cp config.py.sample config.py, and modify it then"
    raise e

env.password = PASSWORD
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


@roles('slave','master')
@parallel
def copy():
    run("cp -f ~/hadoop/etc/hadoop/* /tmp/dfs/hadoop/etc/hadoop/")


@parallel
def init():
    execute(init_master)
    execute(init_slaves)
    with settings(warn_only=True):
        local("mkdir ~/dstats")


@parallel
def start():
    execute(start_master)
    execute(start_slaves)
    execute(start_dstat)


@parallel
def stop():
    execute(stop_dstat)
    execute(stop_slaves)
    execute(stop_master)


@parallel
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
@parallel
def start_slaves():
    run("/tmp/dfs/hadoop/sbin/hadoop-daemon.sh --config /tmp/dfs/hadoop/etc/hadoop/ start datanode")
    run("/tmp/dfs/hadoop/sbin/yarn-daemon.sh --config /tmp/dfs/hadoop/etc/hadoop/ start nodemanager")


@roles('slave')
@parallel
def stop_slaves():
    run("/tmp/dfs/hadoop/sbin/hadoop-daemon.sh --config /tmp/dfs/hadoop/etc/hadoop/ stop datanode")
    run("/tmp/dfs/hadoop/sbin/yarn-daemon.sh --config /tmp/dfs/hadoop/etc/hadoop/ stop nodemanager")


@roles('slave', 'master')
@parallel
def start_dstat(count=COUNT):
    check_call("ssh -f %s nohup ~/dstat -ta --noheaders --noupdate --output ~/dstats/%s.csv 1 %i >& /dev/null < /dev/null &"
        % (env.host_string, env.host_string, count), shell=True)


@roles('slave', 'master')
@parallel
def stop_dstat(count=COUNT):
    run("pkill -f dstat", warn_only=True)


@roles('slave')
@parallel
def upload(upload_folder=UPLOAD_FOLDER):
    total_servers = len(env.roledefs['slave'])
    pit = env.roledefs['slave'].index(env.host_string)
    folder_path = os.path.expanduser(upload_folder)
    for i in os.listdir(folder_path):
        if int(hashlib.sha224(i).hexdigest(), 16) % total_servers == pit:
            file_path = os.path.join(folder_path, i)
            run("/tmp/dfs/hadoop/bin/hdfs dfs -put %s /cs736/input/" % file_path, warn_only=True)


def main(argv):
    pass


if __name__ == '__main__':
    import sys
    main(sys.argv)
