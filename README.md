tttt
====

Technology Trends Through Tweets

Configuration
-------------
### Install
    cd ~
    tar zxvf hadoop-2.5.1.tar.gz
    mv hadoop-2.5.1 hadoop

### Quick alias
    vim ~/.bash_aliases

    alias hadoop='~/hadoop/bin/hadoop'
    alias hdfs='~/hadoop/bin/hdfs'

### Environment
    vim ~/hadoop/etc/hadoop/hadoop-env.sh

    # add these environment variables below JAVA_HOME
    export PATH=$JAVA_HOME/bin:$PATH
    # let you could call official java compile function to compile MapReduce file
    HADOOP_CLASSPATH=$JAVA_HOME/lib/tools.jar

### Single hadoop mode
    cd to/WordCount/folder
    cp something input/
    rm -rf output
    make
    hadoop jar wc.jar WordCount input/ output

### Cluster mode
    hdfs dfs -mkdir -p /cs736/input
    hdfs dfs -put YOURINPUTFILE /cs736/input/
    hdfs dfs -ls /cs736/input/
    hadoop jar wc.jar WordCount /cs736/input/ /cs736/output
    hdfs dfs -ls /cs736/output/
