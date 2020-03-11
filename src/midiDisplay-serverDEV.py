#!/usr/bin/env python
# coding=utf-8

import SimpleHTTPServer
import SocketServer
import urlparse
import urllib

PORT = 8000
IP = '0.0.0.0'

class MyHttpRequestHandler(SimpleHTTPServer.SimpleHTTPRequestHandler):
	def do_GET(self):

		# PARSE URL PARAMS
		#query_components = parse_qs(urlparse(self.path).query)
		#if 'site' in query_components:
		#	site = query_components["site"][0]
		#	print site

		# REDIRECT TO PATH
		print self.path
		if self.path == '/index.html#refresh':
			self.path = 'index.html'
		else if self.path == '/':
			self.path = 'index.html'

		return SimpleHTTPServer.SimpleHTTPRequestHandler.do_GET(self)

# Create an object of the above class
handler_object = MyHttpRequestHandler
my_server = SocketServer.TCPServer(("", PORT), handler_object)

# Star the server
print "serving at port", PORT
my_server.serve_forever()
