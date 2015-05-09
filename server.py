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
push_zmq = context.socket(zmq.PUSH)
push_zmq.bind("tcp://0.0.0.0:50001")

rep_zmq = context.socket(zmq.REP)
rep_zmq.bind("tcp://0.0.0.0:50002")


while 1: 
  time.sleep(0.5)
  inputready,outputready,exceptready = select.select(insock,insock,insock)
  print(exceptready)
  for s in exceptready:
    if s in insock:  insock.remove(s)

  for s in inputready:
    if s == server:
      client, address = server.accept() 
      q_lookup[client.__hash__()] = address
      #print((client,address))
      insock.append(client) 
    else:
      data = s.recv(size)
      if len(data) > 0:
        print(data)

  for s in outputready:
    pass
server.close()
