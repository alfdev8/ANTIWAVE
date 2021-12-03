import socket
import sys
import os


#sys.argvs    ip   

homeDrive=os.environ["HOMEDRIVE"]
localAppData=os.environ["LOCALAPPDATA"]+"\\"
pathAntiwave=homeDrive+"\\ANTIWAVE1.0\\"
pathResources=pathAntiwave+"Resources\\"
path = pathAntiwave+"LVA\\"
TempPath = pathResources+"Temp\\"
NetworkPath = pathResources+"antiwave_network\\"                        


##server path structure
serverLVAPath = pathAntiwave + "server installer\\server\\LVA\\"
serverTempPath = serverLVAPath + "Temp\\"
serverNetworkPath = pathAntiwave + "server installer\\server\\ServerResources\\antiwave_network\\"
serverConfigNetworkPath=serverNetworkPath+'config\\'



serverIP = "192.168.103.1"



s = socket.socket()
s.connect((serverIP,12346))
f = open (serverLVAPath+"renderedTiles.tar", "rb")

l = f.read(1024)
while (l):
    s.send(l)
    l = f.read(1024)

s.shutdown(socket.SHUT_WR)
reply =s.recv(1024) 
a=open(serverLVAPath+"tileCopied.txt",'w')
a.write(str(reply))
a.close()
print (reply)




f.close()
s.close()
