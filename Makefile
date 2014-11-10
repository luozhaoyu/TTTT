JFLAGS = -g
JC = javac
HADOOP = ~/hadoop/bin/hadoop

.SUFFIXES: .java .class
.java.class:
	$(HADOOP) com.sun.tools.javac.Main $*.java
	jar cf wc.jar WordCount*.class

CLASSES = $(wildcard *.java)

default: clean classes

classes: $(CLASSES:.java=.class)

clean:
	rm -f *.class
	rm -f wc.jar
	rm -rf output
