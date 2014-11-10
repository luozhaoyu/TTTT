#!/bin/sh
HADOOP_PREFIX=~/hadoop/
HADOOP_YARN_HOME=~/hadoop/
HADOOP_CONF_DIR=~/hadoop/etc/hadoop/
#Start the HDFS with the following command, run on the designated NameNode:

$HADOOP_PREFIX/sbin/hadoop-daemon.sh --config $HADOOP_CONF_DIR --script hdfs start namenode
#Run a script to start DataNodes on all slaves:

$HADOOP_PREFIX/sbin/hadoop-daemons.sh --config $HADOOP_CONF_DIR --script hdfs start datanode
#Start the YARN with the following command, run on the designated ResourceManager:

$HADOOP_YARN_HOME/sbin/yarn-daemon.sh --config $HADOOP_CONF_DIR start resourcemanager
#Run a script to start NodeManagers on all slaves:

$HADOOP_YARN_HOME/sbin/yarn-daemons.sh --config $HADOOP_CONF_DIR start nodemanager
#Start a standalone WebAppProxy server. If multiple servers are used with load balancing it should be run on each of them:

$HADOOP_YARN_HOME/sbin/yarn-daemon.sh start proxyserver --config $HADOOP_CONF_DIR
#Start the MapReduce JobHistory Server with the following command, run on the designated server:

$HADOOP_PREFIX/sbin/mr-jobhistory-daemon.sh start historyserver --config $HADOOP_CONF_DIR

#$HADOOP_PREFIX/sbin/start-dfs.sh --config $HADOOP_CONF_DIR
#$HADOOP_PREFIX/sbin/start-yarn.sh --config $HADOOP_CONF_DIR

#ssh macaroni-01 "$HADOOP_PREFIX/sbin/yarn-daemon.sh --config $HADOOP_CONF_DIR start nodemanager"
#ssh macaroni-02 "$HADOOP_PREFIX/sbin/yarn-daemon.sh --config $HADOOP_CONF_DIR start nodemanager"
