#!/usr/bin/env python
# coding=utf-8
#

#### IMPORT ####################################################################################################################################################
import os, time, io, json, socket
from bottle import route, run, get, post, request, response, template, static_file


#### VARS #####################################################################################################################################################
HOST_PORT           = 8000
HOST_NAME 	        = socket.gethostname()
HOST_IP             = socket.gethostbyname(HOST_NAME)
WWW_DIR 	        = 'www'
WWW_INDEX           = 'www/index.html'
CONF_DIR            = 'conf'
CONF_MIDINETHUB     = 'conf/midiDisplay.conf'
CONF_RAVELOXMIDI    = 'conf/raveloxmidi.conf'
CONF_DEVICES_DIR    = 'conf/devices'


#### FUNCTIONS #################################################################################################################################################
def get_Host_name_IP():
    try:
        HOST_NAME = socket.gethostname()
        HOST_IP = socket.gethostbyname(HOST_NAME)
        print("HOSTNAME :  ",HOST_NAME)
        print("IP : ",HOST_IP)
    except:
        print("Unable to get Hostname and IP")

def os_system(command):
    # BASH/SHELL COMMAND AND STDIM
    process = Popen(command, stdout=PIPE, shell=True)
    while True:
        line = process.stdout.readline()
        if not line:
            break
        yield line

def saveDeviceFile(device_file,device_id,device_title,device_usbid,device_desc,device_icon):
    # SAVE DEVICE CONF
    f = open(device_file, "w")
    f.write('{ "title": "' + device_title + '", "deviceID": ' + device_id + ', "usbID": "' + device_usbid + '", "desc": "' + device_desc + '", "icon": "' + device_icon + '" }')
    f.close()



#### ROUTES ####################################################################################################################################################
@route('/www/<filepath:path>')
# WWW FILES
def server_static(filepath):
    return static_file(filepath, root=WWW_DIR)

@route('/conf/devices/<filepath:path>')
# DEVICES CONF
def server_static(filepath):
    return static_file(filepath, root=CONF_DEVICES_DIR)

#@route('/www/<filename>')
#def server_static(filename):
#    return static_file(filename, root=WWW_DIR)

@route('/saveDevice', method='GET')
# SAVE DEVICES
def saveDevice():
    device_id       = request.query.get('id')
    device_title    = request.query.get('devicename')
    device_usbid    = request.query.get('usbid')
    device_desc     = request.query.get('desc')
    device_icon     = request.query.get('icon')
    device_file     = CONF_DEVICES_DIR + '/device_' + device_id + '.json'
    saveDeviceFile(device_file,device_id,device_title,device_usbid,device_desc,device_icon)
    return template("device_id: {{device_id}}\ndevice_title: {{device_title}}\ndevice_usbid: {{device_usbid}}\ndevice_desc: {{device_desc}}\ndevice_icon: {{device_icon}}\n device_file: {{device_file}}", device_id=device_id, device_title=device_title, device_usbid=device_usbid, device_desc=device_desc, device_icon=device_icon, device_file=device_file)

@route('/listIcons', method='GET')
# LIST MIDI DEVICE ICONS FOR THE ICON PICKER
def listIcons():
    midiicons_folder    = 'www/assets/images/icons/midi/'
    dir = 'www/assets/images/icons/midi/'
    icons = [os.path.join(os.path.dirname(os.path.abspath(__file__)),dir,i) for i in os.listdir(dir)]
    icon_list = []
    headers = {}
    for icon in icons:
        icon_list.append(icon)

    # RESPONSE AS JSON
    json_encoded = json.dumps(icon_list, indent=4, sort_keys=True)
    json_decoded = json.loads(json_encoded)
    return { 'icons': json_decoded, }


#### ACTION ###################################################################################################################################################
if __name__ == "__main__":	
	print time.asctime(), "\nHOST: %s:%s\nIP: %s\nWWW: %s" % (HOST_NAME, HOST_PORT,     HOST_IP, WWW_DIR)
	try:
		run(host=HOST_IP, port=HOST_PORT, debug=True)
	except KeyboardInterrupt:
		pass
		print time.asctime(), "Server Stops - %s:%s" % (HOST_NAME, HOST_PORT) 
