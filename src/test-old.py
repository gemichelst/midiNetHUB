#!/usr/bin/env python
# coding=utf-8
#!/usr/bin/python

import re, os
from subprocess import Popen, PIPE

def os_system(command):
    process = Popen(command, stdout=PIPE, shell=True)
    while True:
        line = process.stdout.readline()
        if not line:
            break
        yield line

for line in os_system("/usr/bin/aconnect -l -o"):
    if not re.search("verbunden*", line) and not re.search("client*", line) and not re.search("Through*", line) and not re.search("VirMIDI*", line):
	os.system("echo " + line)
