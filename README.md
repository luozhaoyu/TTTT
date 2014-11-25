tttt
====

Technology Trends Through Tweets

Configuration
-------------
### Install
1. install virtual environments

    virtualenv ~/venv
    pip install tweepy fabric
    source ~/venv/bin/activate

- install hadoop

        cd ~
        tar zxvf hadoop-2.5.1.tar.gz
        mv hadoop-2.5.1 hadoop
        git clone TTTTREPO
        cp -r TTTTREPO/etc

### Quick alias
    vim ~/.bash_aliases

    # change hadoop path to your actual hadoop
    alias hadoop='/tmp/dfs/hadoop/bin/hadoop'
    alias hdfs='/tmp/dfs/hadoop/bin/hdfs'

### Environment
    vim ~/hadoop/etc/hadoop/hadoop-env.sh

    export JAVA_HOME=/usr/lib/jvm/java
    # you could also try
    # export JAVA_HOME=/usr/lib/jvm/java-1.7.0

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
1. modify `hadoop/etc/hadoop/slaves` file, which would look like
        macaroni-01.cs.wisc.edu
        macaroni-02.cs.wisc.edu
        macaroni-03.cs.wisc.edu

- upload file into HDFS

        hdfs dfs -mkdir -p /cs736/input
        hdfs dfs -put YOURINPUTFILE /cs736/input/
        hdfs dfs -ls /cs736/input/
        hadoop jar wc.jar WordCount /cs736/input/ /cs736/output
        hdfs dfs -ls /cs736/output/

#### Using fabric
1. Configure the master and slaves

        cp config.py.sample config.py
        vim config.py
        EDITYOURMASTERSANDSLAVES

- `fab init`
- `fab start`
- `hdfs dfs -ls /`

##### Stop hadoop
* `fab stop`

##### Restart hadoop
* `fab restart`

### Known Bugs
* the nodemanager in slave should be started manually
* Off safemode `hadoop dfsadmin -safemode leave`
