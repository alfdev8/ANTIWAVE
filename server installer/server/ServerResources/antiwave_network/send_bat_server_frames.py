import socket
import sys
import os
import time

homeDrive=os.environ["HOMEDRIVE"]
localAppData=os.environ["LOCALAPPDATA"]+"\\"
pathAntiwave=homeDrive+"\\ANTIWAVE1.0\\"
pathResources=pathAntiwave+"Resources\\"
pathLVA = pathAntiwave+"LVA\\"


##server path structure
serverLVAPath = pathAntiwave + "server installer\\server\\LVA\\"
serverTempPath = serverLVAPath + "Temp\\"
serverNetworkPath = pathAntiwave+"server installer\\server\\ServerResources\\antiwave_network\\"

host = socket.gethostname() 
ip=socket.gethostbyname(host) 



s = socket.socket()
s.bind((ip,12347))



s.listen(100) 




counter=0


if os.path.exists(serverLVAPath+"scriptsCounter.txt") is True:
    a=open(serverLVAPath+"scriptsCounter.txt",'r')
    
    counter=int(a.read())
    a.close()
    a=open(serverLVAPath+"scriptsCounter.txt",'w')
    counter+=1
    a.write(str(counter))
    
else:
    a=open(serverLVAPath+"scriptsCounter.txt",'w')
    a.write("0")
    a.close()
    counter=0

        

while True:
    sc, address = s.accept()

    print (address)

    f = open(serverLVAPath + "renderScript_"+str(counter)+".bat",'wb') 


    l = sc.recv(1024)
    while l is not False:
        f.write(l)
        l = sc.recv(1024)
        if not l:

            f.close()
            sc.send(b'Copied File')
            a=open(serverLVAPath + "copiedRenderScript.txt",'w')
            a.write("b'Copied File'")
            a.close()
            break            
    sys.exit()
    sc.close()
    address.close()

s.close()
