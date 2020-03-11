#!/usr/bin/python
#

#### IMPORT ###############################################################################################
from __future__ import absolute_import
from __future__ import division
from __future__ import print_function
from __future__ import unicode_literals
import re, os
from subprocess import Popen, PIPE
from __builtin__ import bytes
from optparse import OptionParser
import codecs
import sys, socket, struct, time, logging, select, fileinput

#### VARS ################################################################################################
COMMAND_NOTE_OFF = 0x80
COMMAND_NOTE_ON = 0x90
COMMAND_AFTERTOUCH = 0xA0
COMMAND_CONTROL_MODE_CHANGE = 0xB0
midiout = []
midiin = []
midicmd = ''
mididumpids_arr = []
mididumpids_str = ''
previd = 0
localport1 = 5004
localport2 = 5005
localport3 = 5006
localport = localport1
i = 0
logger = logging.getLogger('midiDisplay-connect')
os.system("rm /usr/local/etc/midiDisplay/tmp/midiDisplay.packets && touch /usr/local/etc/midiDisplay/tmp/midiDisplay.packets")



#### FUNCTIONS ###########################################################################################
def getMidiDevices(type):
	"""MIDIDEVICE NAME/ID
	get midi devices from
	list file and return them in list
	"""
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
	mididevicesids = {}
	prev_midi_name = []
	prev_midi_id = []
	i = 0

	for midi_name in mididevnames:
			mididevices[midi_name] = ''
			for midi_id in mididevids:
					if midi_name in prev_midi_name or midi_id in prev_midi_id:
							continue
					else:
							mdname = mididevices[midi_name]
							mdid = midi_id
							if mdname == mdid:
									os.system("echo \"[midiDisplay]::WARNING @ getMidiDevices() ==> mdname is mdid\"")
									continue
							elif midi_id in mididevices:
									os.system("echo \"[midiDisplay]::WARNING @ getMidiDevices() ==> midi_id in mididevices\"")
									continue
							else:
									mididevicesids[midi_id] = midi_name
									mididevices[midi_name] = midi_id
									prev_midi_name.append(midi_name)
									prev_midi_id.append(midi_id)
	if type == 1:
		return mididevices
	elif type == 2:
		return mididevicesids
	else:
		os.system("echo \"[midiDisplay]::ERROR @ getMidiDevices() ==> no type given\"")


def getMidi(midiport):
	"""MIDI DETECTOR
	detects midi device input
	and output midi device name if detected.
	if detected and known input redraw display
	to animate activity dots.
	"""
	os.system("echo \"" + midiport + "\" >> /usr/local/etc/midiDisplay/tmp/midiDisplay.packets")
	midiport = str(midiport)
	mididevice = mididevicesids[midiport]
	if mididevice == '':
		os.system("echo \"[midiDisplay]::detected\t ==> unknown midiDeviceID(" + midiport + ":0)\"")
		os.system("echo \"[midiDisplay]::detected\t ==> unknown midiDeviceID(" + midiport + ":0)\" >> /usr/local/etc/midiDisplay/tmp/midiDisplay.log")
	else:
		os.system("echo \"[midiDisplay]::detected\t ==> " + mididevice + " (" + midiport + ":0)\"")
		os.system("echo \"[midiDisplay]::detected\t ==> " + mididevice + " (" + midiport + ":0)\" >> /usr/local/etc/midiDisplay/tmp/midiDisplay.log")

class Handler(object):
	"""MIDI HANDLER
	starts aseqdump and 
	stdout deviceid
	"""
	def on_midi_commands(self, aseqnetOut, command_list):
		pass

def os_system(command):
	"""BASH/SHELL COMMAND AND STDIM
	performs shell commands and
	write it to stdout
	"""
	process = Popen(command, stdout=PIPE, shell=True)
	while True:
		line = process.stdout.readline()
		if not line:
			break
		yield line

def h2b(s):
	"""HEX(Str) TO BYTES
	Converts a hex string 
	to bytes; Python 2/3 compatible.
	"""
	return bytes.fromhex(s)

def b2h(b):
	"""BYTES(Obj) to HEX(Str)
	Converts a `bytes` object 
	to a hex string.
	"""
	if not isinstance(b, bytes):
		raise ValueError('Argument must be a `bytes`')
	result = codecs.getencoder('hex_codec')(b)[0]
	if isinstance(result, bytes):
		result = result.decode('ascii')
	return result

# RECEIVE MIDI CMD AND CHANGE DISPLAY
def midipackets(command):
	"""RECEIVE MIDIPACKETS."""	
	process = Popen(command, stdout=PIPE, shell=True)
	out = process.stdout.readline()
	while True:
		line = process.stdout.readline()
		if not line:
			break
		yield line

class MidiHandler(Handler):
	  """Example handler.
	  This handler doesn't do all that much; we're just using one here to
	  illustrate the handler interface, so you can write a much cooler one.
	  """
	  def __init__(self):
		  self.logger = logging.getLogger('MidiHandler')

	  def on_midi_commands(self, peer, command_list):
		  for command in command_list:
			  if command.command == 'note_on':
				 key = command.params.key
				 velocity = command.params.velocity
				 print('Someone hit the key {} with velocity {}'.format(key, velocity))



#### APP ####################################################################################################

# GET MIDI DEVICE IDS
for line in os_system("/usr/bin/aconnect -l -i"):
	client=re.search("client (\d*)", line)
	if client and not re.search("Through", line) and not re.search("Virtual Raw MIDI", line) and not re.search("multimidicast*", line) and not re.search("aseqdump*", line):
		if client.group(1) != '0':
				midiout.append(client.group(1))

# ACONNECT MIDI DEVICE IDS TO MULTIMIDICAST 128:0 (multimidicast) AND 16:0 (virtualRawMIDI)
os.system("rm /usr/local/etc/midiDisplay/tmp/midiDisplay.portids && touch /usr/local/etc/midiDisplay/tmp/midiDisplay.portids")
for midi_o in midiout:
	os.system("/usr/bin/aconnect " + midi_o + ":0 128:0")
	os.system("/usr/bin/aconnect " + midi_o + ":0 16:0")
	if previd != midi_o:
		mididumpids_str = midi_o + ":0"
		mididumpids_arr.append(mididumpids_str)
		os.system("echo \"" + midi_o + ":0\" >> /usr/local/etc/midiDisplay/tmp/midiDisplay.portids")
	previd = midi_o

# CLEAR DUMP AND DEFINE DUMP COMMAND
aseqnet_dump = "aseqnet -p 5006 -s 16:0 -v -i" 															# >> Channel 0: Control event: 127 ==> aseqnet -p 5006 -s 16:0 -v -i
amidi_dump = "amidi --port=hw:0,0 --receive=/usr/local/etc/midiDisplay/tmp/midiDisplay.packets --dump"	# >> B0 61 7F ==> amidi --port=hw:0,0 --receive=/usr/local/etc/midiDisplay/tmp/midiDisplay.packets --dump
aseq_dump = "aseqdump"																					# >> 32:0 Control change 0, controller 70, value 127 ==> aseqdump --port=32:0,28:0,24:0
aseq_ports = ''

# STOP PREVIOUS ASEQDUMP
os.system("killall -r aseqdump -s SIGTERM")

# LOOP STDIN AND READ MIDI IN COMMANDS
for mididumpid in mididumpids_arr:
	aseq_ports += " --port=" + mididumpid

# GET MIDI DEVICE ID
MDLOGFILE = file('/usr/local/etc/midiDisplay/tmp/midiDisplay.log', 'a')
os.system("echo \"[midiDisplay]::midiDeviceIDs ==> loading listfiles\"")
mididevices = getMidiDevices(1)
if mididevices:
	os.system("echo \"[midiDisplay]::listfile(mididevices) ==> OK\"")
	os.system("echo \"[midiDisplay]::listfile(mididevices) ==> OK\" >> /usr/local/etc/midiDisplay/tmp/midiDisplay.log")
	#print(mididevices) >> MDLOGFILE
	mididevicesStr = str(mididevices)
	print > MDLOGFILE, mididevicesStr
	#MDLOGFILE.write(mididevicesStr)
else:
	os.system("echo \"[midiDisplay]::listfile(mididevices) ==> FAILED\"")
	os.system("echo \"[midiDisplay]::listfile(mididevices) ==> FAILED\" >> /usr/local/etc/midiDisplay/tmp/midiDisplay.log")

mididevicesids = getMidiDevices(2)
if mididevicesids:
	os.system("echo \"[midiDisplay]::listfile(mididevicesids) ==> OK\"")
	os.system("echo \"[midiDisplay]::listfile(mididevicesids) ==> OK\" >> /usr/local/etc/midiDisplay/tmp/midiDisplay.log")
	#print(mididevicesids) >> MDLOGFILE
	mididevicesidsStr = str(mididevicesids)
	print > MDLOGFILE, mididevicesidsStr
	#MDLOGFILE.write(mididevicesidsStr)
else:
	os.system("echo \"[midiDisplay]::listfile(mididevicesids) ==> FAILED\"")
	os.system("echo \"[midiDisplay]::listfile(mididevicesids) ==> FAILED\" >> /usr/local/etc/midiDisplay/tmp/midiDisplay.log")

# MIDI LIVE DUMP AND ACTION IF MIDI DEVICE IS KNOWN
for line in midipackets("aseqdump" + aseq_ports):
	midicmd=True
	if midicmd and not re.search("Waiting*", line) and not re.search("Source*", line):
		if midicmd != '':
			midiport=re.sub("\s*", "", line)
			#midiport=re.sub("0,*", "", midiport)
			midiport=re.sub("0*", "", midiport)
			midiport=re.sub(",*", "", midiport)
			midiport=re.sub("controller", "", midiport)
			midiport=re.sub("value", "", midiport)
			midiport=re.sub("Controlchange", "", midiport)
			midiport=re.sub("Noteon\d*", "", midiport)
			midiport=re.sub("Noteoff\d*", "", midiport)
			midiport=re.sub("note\d*", "", midiport)
			midiport=re.sub("velocity\d*", "", midiport)
			midiport=re.sub(":\d*", "", midiport)
			midiportFull=midiport + ":0"

			out = getMidi(midiport)
			
			# REDRAW DISPLAY

			# IF $_THIS PORT IS DETECTED SHOW ACTIVITY ON LCD SCREEN
			# reDraw.lcd(midiport)
			# draw.circle with fill
