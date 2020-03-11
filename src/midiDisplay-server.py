#!/usr/bin/env python
# coding=utf-8

import SimpleHTTPServer
import SocketServer
import urlparse
import urllib

PORT = 8000
IP = "0.0.0.0"

class MyHttpRequestHandler(SimpleHTTPServer.SimpleHTTPRequestHandler):
	def do_GET(self):

		# PARSE URL PARAMS

		# REDIRECT TO PATH
		print self.path
		if self.path == 'www/index.html#refresh' or self.path == '/www/index.html#refresh' or self.path == '#refresh':
			print "reloading site..."
			self.path = 'www/index.html'
		elif self.path == '/':
			self.path = 'www/index.html'

		return SimpleHTTPServer.SimpleHTTPRequestHandler.do_GET(self)

# Create an object of the above class
handler_object = MyHttpRequestHandler
my_server = SocketServer.TCPServer(("", PORT), handler_object)

# Star the server
print "midiDisplay WWW-SERVER started"
print "serving at port", PORT
print "CTRL + C to close"
my_server.serve_forever()
