#!/usr/bin/python
# WRITE DEVICE DATA TO DEVICE_XX.JSON
# USAGE: writeDeviceToJSON.py deviceID deviceTitle deviceUsbId deviceDesc deviceIcon
#
print('Content-type: application/python\n')

#### IMPORT ###############################################################################################
import sys


#### VARS ################################################################################################
deviceID 	= sys.argv[1]
deviceTitle	= sys.argv[2]
deviceUsbID	= sys.argv[3]
deviceDesc	= sys.argv[4]
deviceIcon	= sys.argv[5]
filePath = "../../../conf/devices/device_" + deviceID + ".json"
#print filePath

print 'Number of arguments:', len(sys.argv), 'arguments.'
print 'Argument List:', str(sys.argv)


#### ACTION ##############################################################################################
f = open(filePath, "w")
f.write('{ "title": "' + deviceTitle + '", "deviceID": ' + deviceID + ', "usbID": "' + deviceUsbID + '", "desc": "' + deviceDesc + '", "icon": "' + deviceIcon + '" }')
f.close()
