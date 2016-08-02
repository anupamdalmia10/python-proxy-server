import socket, sys
from thread import *

buffersize = 8193
max_conn = 5
port = 5140
def startserver():
	try:
		print "\n starting..."
		s = socket.socket()
		s.bind(('',port))
		s.listen(max_conn)
	except Exception, e:
		print "Something went wrong \n"
		print e
		sys.exit(2)

	while 1:
		try:
			client_connecion, client_address = s.accept()
			in_data = client_connecion.recv(buffersize)
			start_new_thread(connection_proxy,(client_connecion,in_data,client_address))
		except KeyboardInterrupt:
			s.close()
			print "\nclosing..."
			sys.exit(1)

	s.close()

def connection_proxy(client_connecion,in_data,client_address):
	try:
		first_line = in_data.split('\n')[0]
		url = first_line.split(' ')[1]
		http_pos = url.find("://")
		if http_pos==-1:
			temp = url
		else:
			temp = url[http_pos+3:]

		port_position = temp.find(':')
		target_server_pos = temp.find(':')
		if target_server_pos==-1:
			target_server_pos=len(temp)

		target_server=""
		port=-1
		if port_position==-1 or target_server_pos<port_position:
			port=80
			target_server = temp[:target_server_pos-1]
		else:
			target_server=temp[:port_position-1]
			port = int(temp[port_position+1:target_server_pos - port_position - 1])
		#client_connecion.send("reply")
		#proxy_connect(target_server,port,client_connecion,client_address,in_data)
		


	except Exception, e:
		pass

	try:
		print target_server
		print port
		#print in_data
		sr = socket.socket()
		try:
			sr.connect((target_server,port))
		except:
			print "kuch gadbad hai"
		sr.send(in_data)
		#client_connecion.send("reply")
		while 1:
			try:
				reply = sr.recv(buffersize)
				print reply
			except:
				print "problem in reply"
			if(len(reply)>0):
				client_connecion.send(reply)
			else:
				break

		sr.close()
		client_connecion.close()

	except Exception, e:
		sr.close()
		client_connecion.close()
		sys.exit(1)

def proxy_connect(target_server,port,client_connecion,client_address,in_data):

	try:
		print target_server+":"
		print port
		print in_data
		sr = socket.socket()
		sr.connect((target_server,port))
		sr.send(in_data)
		client_connecion.send("reply")
		while 1:
			reply = sr.recv(buffersize)
			print reply
			if(len(reply)>0):
				client_connecion.send("reply")
			else:
				break

		sr.close()
		client_connecion.close()

	except Exception, e:
		sr.close()
		client_connecion.close()
		sys.exit(1)



startserver()


