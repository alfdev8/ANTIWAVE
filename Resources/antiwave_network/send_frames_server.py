import socket
import sys

import os

homeDrive=os.environ["HOMEDRIVE"]
localAppData=os.environ["LOCALAPPDATA"]+"\\"
pathAntiwave=homeDrive+"\\ANTIWAVE1.0\\"
pathResources=pathAntiwave+"Resources\\"
pathLVA = pathAntiwave+"LVA\\"
NetworkPath = pathResources+"antiwave_network\\" 


serverLVAPath = pathAntiwave + "server installer\\server\\LVA\\"
serverTempPath = serverLVAPath + "Temp\\"
serverNetworkPath = pathAntiwave+"server installer\\server\\ServerResources\\antiwave_network\\"
InstallPath = pathResources+"antiwave_install\\"



sys.path.insert(1,InstallPath)
import sortWeigth


host = socket.gethostname() 
ip=socket.gethostbyname(host) 


s = socket.socket()
s.bind((ip,12346))
s.listen(100) 



computers=sortWeigth.sortComputers()

hostnames=[]
ip=[]
cores=[]
c=0
while c<len(computers):
    hostnames.append(computers[c][4])
    ip.append(computers[c][3])
    cores.append(computers[c][1])
    c+=1

##print (hostnames)
    
while True:
    tarFiles=[x for x in os.listdir(pathLVA) if os.path.splitext(x)[1] in ('.tar')]
  
##    print (tarFiles)
    if len(tarFiles) == len(hostnames):
        sys.exit()



    
    sc, address = s.accept()
    a=open(NetworkPath+'frameOrder.txt','r')
    index=a.read()
    a.close()

    limit = 5000
    if int(index) >= limit:
        index='1'
    
    

##    print (address)

    f = open(pathLVA + "renderedFrames_"+index+".tar",'wb') 
 
              

    l = sc.recv(1024)
    while l is not False:
        f.write(l)
        l = sc.recv(1024)
        if not l:            
            f.close()
            a=open(NetworkPath+'frameOrder.txt','w')
            a.write(str(int(index)+1))
            a.close()
            sc.send(b'Copied File')
            a=open(pathLVA + "framesReady.txt",'w')
            a.write("b'Copied Frames'")
            a.close()
            break            
    
##    sc.close()         #error?       
##    address.close()

s.close()




