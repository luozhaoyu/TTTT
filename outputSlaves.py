
#!/usr/bin/python
# -*- coding: utf-8 -*-
"""
    fabfile.py
    ~~~~~~~~~~~~~~

    A brief description goes here.
"""
try:
    from config import MACHINES
except ImportError as e:
    print "You should cp config.py.sample config.py, and modify it then"
    raise e
for node in MACHINES['slave']:
   print node
