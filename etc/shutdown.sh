#!/bin/sh
HADOOP_PREFIX=~/hadoop/
HADOOP_YARN_HOME=~/hadoop/
HADOOP_CONF_DIR=~/hadoop/etc/hadoop/

#Stop the NameNode with the following command, run on the designated NameNode:

$HADOOP_PREFIX/sbin/hadoop-daemon.sh --config $HADOOP_CONF_DIR --script hdfs stop namenode
#Run a script to stop DataNodes on all slaves:

$HADOOP_PREFIX/sbin/hadoop-daemon.sh --config $HADOOP_CONF_DIR --script hdfs stop datanode
#Stop the ResourceManager with the following command, run on the designated ResourceManager:

$HADOOP_YARN_HOME/sbin/yarn-daemon.sh --config $HADOOP_CONF_DIR stop resourcemanager
#Run a script to stop NodeManagers on all slaves:

$HADOOP_YARN_HOME/sbin/yarn-daemon.sh --config $HADOOP_CONF_DIR stop nodemanager
#Stop the WebAppProxy server. If multiple servers are used with load balancing it should be run on each of them:

$HADOOP_YARN_HOME/sbin/yarn-daemon.sh stop proxyserver --config $HADOOP_CONF_DIR
#Stop the MapReduce JobHistory Server with the following command, run on the designated server:

$HADOOP_PREFIX/sbin/mr-jobhistory-daemon.sh stop historyserver --config $HADOOP_CONF_DIR

$HADOOP_PREFIX/sbin/stop-dfs.sh --config $HADOOP_CONF_DIR
$HADOOP_PREFIX/sbin/stop-yarn.sh --config $HADOOP_CONF_DIR
