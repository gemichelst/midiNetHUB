#!/usr/bin/env python
# coding=utf-8

import SimpleHTTPServer
import CGIHTTPServer
import BaseHTTPServer
import SocketServer
import urlparse
import urllib
import urlparse
import httplib
import time
import io

PORT_NUMBER = 8000
HOST_NAME = '192.168.11.32'
# IP = "0.0.0.0"

# class MyHttpRequestHandler(SimpleHTTPServer.SimpleHTTPRequestHandler):
# 	def do_GET(self):

# 		# PARSE URL PARAMS

# 		# REDIRECT TO PATH
# 		print self.path
# 		if self.path == 'www/index.html#refresh' or self.path == '/www/index.html#refresh' or self.path == '#refresh':
# 			print "reloading site..."
# 			self.path = 'www/index.html'
# 		elif self.path == '/':
# 			self.path = 'www/index.html'

# 		return SimpleHTTPServer.SimpleHTTPRequestHandler.do_GET(self)

# # Create an object of the above class
# handler_object = MyHttpRequestHandler
# my_server = SocketServer.TCPServer(("", PORT), handler_object)

# # Star the server
# print "midiDisplay WWW-SERVER started"
# print "serving at port", PORT
# print "CTRL + C to close"
# my_server.serve_forever()

class MyHttpRequestHandler(CGIHTTPServer.CGIHTTPRequestHandler):

	def do_POST(self):
		print('POST ACCESS TO writeDeviceToJSON.py')
		content_length = int(self.headers['Content-Length'])
		body = self.rfile.read(content_length)
		self.send_response(200)
		self.end_headers()
		response = io.BytesIO()
		response.write(b'This is POST request. ')
		response.write(b'Received: ')
		response.write(body)
		self.wfile.write(response.getvalue())
		print response.getvalue()
	# def do_POST(self):

	# 	# PARSE URL PARAMS

	# 	# REDIRECT TO PATH
	# 	print self.path
	# 	if self.path == '/cgi-bin/writeDeviceToJSON.py':
	# 		self.path = '/cgi-bin/writeDeviceToJSON.py'
	# 		print('POST ACCESS TO writeDeviceToJSON.py')
	# 		print self.path
	# 	elif self.path == '/':
	# 		self.path = 'www/index.html'

	# 	return CGIHTTPServer.CGIHTTPRequestHandler.do_POST(self)

	def do_GET(self):

		# PARSE URL PARAMS

		# REDIRECT TO PATH
		print self.path
		if self.path == '/cgi-bin/writeDeviceToJSON.py':
			self.path = '/cgi-bin/writeDeviceToJSON.py'
			print('GET ACCESS TO writeDeviceToJSON.py')
			print self.path
		elif self.path == '/':
			self.path = 'www/index.html'

		return CGIHTTPServer.CGIHTTPRequestHandler.do_GET(self)


if __name__ == "__main__":
	server = BaseHTTPServer.HTTPServer
	#handler = CGIHTTPServer.CGIHTTPRequestHandler
	handler = MyHttpRequestHandler
	server_address = ("", 8000)
	handler.cgi_directories = ["/cgi-bin"]
	httpd = server(server_address, handler)
	print time.asctime(), "Server Starts - %s:%s" % (HOST_NAME, PORT_NUMBER)
	try:
		httpd.serve_forever()
	except KeyboardInterrupt:
		pass
		httpd.server_close()
		print time.asctime(), "Server Stops - %s:%s" % (HOST_NAME, PORT_NUMBER)
