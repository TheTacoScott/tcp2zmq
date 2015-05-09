import select 
import socket 
import sys 
import zmq
import msgpack
import time

host = '' 
port = 50000
backlog = 50 
size =  4096
server = socket.socket(socket.AF_INET, socket.SOCK_STREAM) 
server.bind((host,port)) 
server.listen(backlog) 
insock = [server]
q_lookup = {}

context = zmq.Context()
data_pub_zmq = context.socket(zmq.PUB)
data_pub_zmq.bind("tcp://0.0.0.0:50010")

socket_present_zmq = context.socket(zmq.PUSH)
socket_present_zmq.bind("tcp://0.0.0.0:50001")

cmd_push_zmq = context.socket(zmq.PUSH)
cmd_push_zmq.bind("tcp://0.0.0.0:50002")
cmd_rep_zmq = context.socket(zmq.REP)
cmd_rep_zmq.bind("tcp://0.0.0.0:50004")

#data_pull_zmq = context.socket(zmq.PULL)
#data_pull_zmq.bind("tcp://0.0.0.0:50003")

cmd_rep_zmq = context.socket(zmq.REP)
cmd_rep_zmq.bind("tcp://0.0.0.0:50004")


while 1: 
  inputready,outputready,exceptready = select.select(insock,insock,insock,0.001)
  for s in exceptready:
    if s in insock:  insock.remove(s)

  for s in inputready:
    if s == server:
      client, address = server.accept()
      client_hash = client.__hash__() 
      if client_hash not in q_lookup:
        q_lookup[client_hash] = address
        socket_present_zmq.send(client_hash)
      #print((client,address))
      insock.append(client) 
    else:
      data = s.recv(size)
      if len(data) > 0:
        print(data)
        output_msg = msgpack.packb((s.__hash__(),data))

  for s in outputready:
    pass
server.close()
