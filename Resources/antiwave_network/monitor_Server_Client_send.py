import socket
import sys
import os

homeDrive=os.environ["HOMEDRIVE"]
pathAntiwave=homeDrive+"\\ANTIWAVE1.0\\"
pathResources=pathAntiwave+"Resources\\"
pathLVA = pathAntiwave+"LVA\\"
binPath = pathResources+"bin\\"                                        
TempPath = pathResources+"Temp\\"                                       
NetworkPath = pathResources+"antiwave_network\\"                        
InstallPath = pathResources+"antiwave_install\\"                        

##server path structure
serverLVAPath = pathAntiwave + "server installer\\server\\LVA\\"
serverTempPath = serverLVAPath + "Temp\\"
serverNetworkPath = pathAntiwave+"server installer\\server\\ServerResources\\antiwave_network\\"

host = socket.gethostname() 
ip=socket.gethostbyname(host) 


s = socket.socket()
s.bind((ip,12346))
s.listen(100) 


while True:

    a=open(NetworkPath+"tileOrder.txt",'r')
    b=a.read()
    a.close()

    limit = 5000
    if int(b) >= limit:
        b='1'

    sc, address = s.accept()

    print (address)

    f = open(pathLVA + "renderToClient"+b+".tar",'wb')

    l = sc.recv(1024)
    while l is not False:
        f.write(l)
        l = sc.recv(1024)
        if not l:

            f.close()
            sc.close()

            a=open(NetworkPath + "tileOrder.txt",'w')
            a.write(str(int(b)+1))
            a.close()
            break
        

    

s.close()




