#!/usr/bin/env python
# coding=utf-8
#

#### IMPORT ####################################################################################################################################################
from bottle import route, run, get, post, request, response, template, static_file
import time
import io

#### VARS #####################################################################################################################################################
PORT_NUMBER         = 8000
HOST_NAME 	        = 'localhost'
HOST_IP             = '192.168.11.32'
WWW_DIR 	        = 'www'
WWW_INDEX           = 'www/index.html'
CONF_DIR            = 'conf'
CONF_DEVICES_DIR    = 'conf/devices'

#### FUNCTIONS #################################################################################################################################################
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


#### ACTION ###################################################################################################################################################
if __name__ == "__main__":	
	print time.asctime(), "\nHOST: %s:%s\nIP: %s\nWWW: %s" % (HOST_NAME, PORT_NUMBER, HOST_IP, WWW_DIR)
	try:
		run(host='0.0.0.0', port=8000, debug=True)
	except KeyboardInterrupt:
		pass
		print time.asctime(), "Server Stops - %s:%s" % (HOST_NAME, PORT_NUMBER)
