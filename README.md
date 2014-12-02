tttt
====

Technology Trends Through Tweets

Configuration
-------------
### Install
1. install virtual environments

        virtualenv ~/venv
        pip install tweepy fabric matplotlib
        source ~/venv/bin/activate
- install hadoop

        cd ~
        tar zxvf hadoop-2.5.1.tar.gz
        mv hadoop-2.5.1 hadoop
        git clone TTTTREPO
        cp -r TTTTREPO/etc
- install dstat

        cd ~
        wget -c http://dag.wieers.com/home-made/dstat/dstat-0.7.2.tar.bz2
        tar jxvf dstat-0.7.2.tar.bz2
        cp dstat-0.7.2.tar.bz2/dstat ~

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

Check cluster status
* <http://macaroni-05.cs.wisc.edu:50070/>
    * [HDFS files] (http://macaroni-05.cs.wisc.edu:50070/explorer.html#/)
* <http://macaroni-05.cs.wisc.edu:8088/>


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

##### Manually operate dstat
* `fab start_dstat`: start dstat, which would last for 3600 seconds (configurable)
* `fab stop_dstat`

##### Copy new configurations
* `fab copy`

##### Add nodes

Assuming `macaroni-01` is the only slave currently, and we will add *macaroni-02 macaroni-03*.
And `macaroni-05` is the master

1. `fab stop`: stop all nodes.
- modify your `config.py` like:

        MACHINES = {
            #'master': [macaroni-05],
            'master': [],
            'slave': [
                #'macaroni-01',
                'macaroni-02',
                'macaroni-03',
            ]
            }
- `fab init` (Attention, **never reinitialize** your master!)
- uncomment the machines in the `config.py`
- `fab start`
    * then fabric would say something like *No hosts found. Please specify (single) host string for connection:*. Just type in an arbitrary **new slave** hostname, in this case: macaroni-03. (It is a hack)

`hadoop/etc/hadoop/slaves` seems to be **irrelevant** with specifying the slave nodes.
However, you have to modify it if you do not use fabric.

### Known Bugs
* the nodemanager in slave should be started manually
* Off safemode `hadoop dfsadmin -safemode leave`
