import socket               
import sys
print(sys.argv)




serverIP=sys.argv[1]
print (serverIP)

s = socket.socket()         
host = socket.gethostname() 
port = 12345                
b=socket.gethostbyname(host)                              
print(b)
s.connect((serverIP, port))             
print (s.recv(1024))

b=str(sys.argv[2])
s.send(bytes(b, encoding='utf-8'))
print(s.recv(1024))





s.close()                     

