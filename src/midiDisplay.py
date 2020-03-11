#!/usr/bin/env python
# coding=utf-8

# IMPORT PYTHON LIBS
from lib_oled96 import ssd1306
from smbus import SMBus
from time import sleep
from PIL import ImageFont, ImageDraw, Image
import re, os
from subprocess import Popen, PIPE
import sys, socket, struct, time

# DEFINE FUNCTION
def os_system(command):
    process = Popen(command, stdout=PIPE, shell=True)
    while True:
        line = process.stdout.readline()
        if not line:
            break
        yield line

font = ImageFont.load_default()

# DISPLAY HW VARS
i2cbus = SMBus(1)            # 0 = Raspberry Pi 1, 1 = Raspberry Pi > 1
oled = ssd1306(i2cbus)

# SHORTENER: oled.canvas => draw
draw = oled.canvas

# RESET DISPLAY AT START
oled.cls()
oled.display()

# LOAD IMAGE AND RESET AFTER 3SEC
#logo = Image.open('/usr/local/etc/midiDisplay/assets/images/midiDisplay_logo_inverted.png')
logo = Image.open('/usr/local/etc/midiDisplay/assets/images/midiDisplay_logo.png')
draw.bitmap((32, 0), logo, fill=1)
oled.display()
sleep(2)

# BORDER AROUND THE SCREEN
draw.rectangle((0, 0, oled.width-1, oled.height-1), outline=1, fill=0)

# draw.text((x, y), "TEXT", fill=1)
# ROW1: 0,0 | ROW2: 0,16 | ROW3: 0,32 | ROW4: 0,48
#draw.text((0, 0), "row1", font=font,fill=1)
#draw.text((0, 16), "row2", font=font,fill=1)
#draw.text((0, 32), "row3", font=font,fill=1)
#draw.text((0, 48), "row4", font=font,fill=1)
#oled.display()


# DEFINE FONT, VARS AND ARRAYS
count = 0
mididevices = []
midideviceids = []

# CLEAR LOGS
os.system("rm /usr/local/etc/midiDisplay/tmp/midiDisplay.log && touch /usr/local/etc/midiDisplay/tmp/midiDisplay.log")
os.system("rm /usr/local/etc/midiDisplay/tmp/midiDisplay.list && touch /usr/local/etc/midiDisplay/tmp/midiDisplay.list")

# GET DEVICES (names + ids)
os.system("echo \"[midiDisplay]::devices\t  ==> reading ...\"")
for line in os_system("/usr/bin/aconnect -l -i"):
	client=re.sub("\s*", "", line)
	client=re.search("\:\'(.*)\'", client)
	if client and not re.search("Through", line) and not re.search("System*", line) and not re.search("Timer*", line) and not re.search("Announce*", line) and not re.search("Connect*", line) and not re.search("VirMIDI*", line) and not re.search("Virtual Raw MIDI*", line) and not re.search("/usr/local/bin/multimidicast*", line) and not re.search("225.0.0.*", line) and not re.search("aseqdump*", line):
		mididevices.append(client.group(1))

for line in os_system("/usr/bin/aconnect -l -i"):
	deviceids=re.search("client (\d*)\:", line)
	if deviceids and not re.search("Through", line) and not re.search("System*", line) and not re.search("Timer*", line) and not re.search("Announce*", line) and not re.search("Connect*", line) and not re.search("VirMIDI*", line) and not re.search("Virtual Raw MIDI*", line) and not re.search("/usr/local/bin/multimidicast*", line) and not re.search("225.0.0.*", line) and not re.search("aseqdump*", line):
		midideviceids.append(deviceids.group(1))

## DEVICE-ID
midiDevices = {}
for mididevice in mididevices:
	midiDevices[mididevice] = midideviceids[count] + ':0'
	os.system("echo \"[midiDisplay]::devices\t  ==> " + mididevice + " (" + midideviceids[count] + ":0)\"")
	os.system("echo \"" + mididevice + ":" + midideviceids[count] + "\" >> /usr/local/etc/midiDisplay/tmp/midiDisplay.list")
	count += 1

# DEBUG
#print(midiDevices)


# CREATE DISPLAY-DATA
os.system("echo \"[midiDisplay]::display\t  ==> draw.display()\"")

# DISPLAY VARS
fontSize = 10
font = ImageFont.truetype('/usr/local/etc/midiDisplay/assets/fonts/FreeSans.ttf', fontSize)
linebreak_val = 10
linebreak_run = 0
linebreak = 0
padding = 2
shapeWidth = 10 + padding
shapeHeight = 10 + padding
top = padding
x = padding
bottom = oled.height - padding - 1
counterr = 1

# DRAW DISPLAY-DATA
for mididevice in mididevices:
	draw.ellipse((3, linebreak + padding + 2, shapeWidth, shapeHeight * counterr - padding), outline=1, fill=0)
	draw.text((x + shapeWidth + 1, shapeHeight * counterr - 10), mididevice + " (" + midiDevices[mididevice] + ")", font=font,fill=1)
#	draw.line((x, linebreak + padding + 1, oled.width, shapeHeight * counterr - padding), fill=1)
#	draw.line((x + shapeWidth - 1, 0, 1, oled.height + padding + shapeWidth), fill=1)
	draw.line((x, shapeHeight * counterr - padding + 3, oled.width, shapeHeight * counterr - padding + 3), fill=1)
	linebreak += fontSize + padding
	top += padding
	counterr += 1
	os.system("echo \"" + mididevice + " (" + midiDevices[mididevice] + ")\" >> /usr/local/etc/midiDisplay/tmp/midiDisplay.log")

# WRITE DISPLAY-DATA
oled.display();

# EXIT
os.system("echo \"[midiDisplay]::done\t  ==> exit\"")
