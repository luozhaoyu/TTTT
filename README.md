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

### Single hadoop mode
    cd to/WordCount/folder
    cp something input/
    rm -rf output
    make
    hadoop jar wc.jar WordCount input/ output
