#!/bin/sh
HADOOP_PREFIX=~/hadoop/
rm -rf ~/hadoop/logs/*

ssh macaroni-05 "rm -rf /tmp/dfs/; mkdir -p /tmp/dfs/data"
ssh macaroni-01 "rm -rf /tmp/dfs/; mkdir -p /tmp/dfs/data"
ssh macaroni-02 "rm -rf /tmp/dfs/; mkdir -p /tmp/dfs/data"
ssh macaroni-03 "rm -rf /tmp/dfs/; mkdir -p /tmp/dfs/data"
ssh macaroni-04 "rm -rf /tmp/dfs/; mkdir -p /tmp/dfs/data"

$HADOOP_PREFIX/bin/hdfs namenode -format
