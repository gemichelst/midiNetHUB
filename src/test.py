#!/usr/bin/python
import re, os
from subprocess import Popen, PIPE
import sys, socket, struct, time, fileinput
#def myFunction():
#	print "Blapups3000"
#myFunction()

def os_system(command):
    process = Popen(command, stdout=PIPE, shell=True)
    while True:
        line = process.stdout.readline()
        if not line:
            break
        yield line

def getMidiDevices():
	mididevnames = []
	mididevids = []

	for line in fileinput.input('/usr/local/etc/midiDisplay/tmp/midiDisplay.list'):
		mididevname=re.search("(\w*)\:", line)
		if mididevname:
			mididevnames.append(mididevname.group(1))

	for line in fileinput.input('/usr/local/etc/midiDisplay/tmp/midiDisplay.list'):
        	mididevid=re.search("\:(\d*)", line)
        	if mididevid:
                	mididevids.append(mididevid.group(1))

	mididevices = {}
	prev_midi_name = []
	prev_midi_id = []
	i = 0
	for midi_name in mididevnames:
		mididevices[midi_name] = ''
		for midi_id in mididevids:
			if midi_name in prev_midi_name or midi_id in prev_midi_id:
				continue
#				for midiID in prev_midi_id:
#			if midi_name not in prev_midi_name and midi_id not in prev_midi_id:
#				if midi_name:
			else:
				mdname = mididevices[midi_name]
				mdid = midi_id
				if mdname == mdid:
					os.system("echo \"mdname is mdid\"")
					continue
#				elif mdname.isdigit() or mdname is prev_midi_id:
#					os.system("echo \"mdname is digit\"")
#					continue
				elif midi_id in mididevices:
					os.system("echo \"midi_id in mididevices\"")
					continue
				else:
					os.system("echo \"" + midi_name + " = " + midi_id + "\"")
					mididevices[midi_name] = midi_id
					prev_midi_name.append(midi_name)
					prev_midi_id.append(midi_id)
					#os.system("echo \"" + midi_name + " = " + midi_id + "\"")
					#mididevices[midi_name] = midi_id

	print(mididevices)


getMidiDevices()

#print(mididevnames)
#print(mididevids)
