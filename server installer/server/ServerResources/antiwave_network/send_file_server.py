import socket
import sys
import os

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
s.bind((ip,12346))
s.listen(100)

while True:
    sc, address = s.accept()

    print (address)

    f = open(serverLVAPath + "projectFolder.tar",'wb')              
    
    l = sc.recv(1024)
    while l is not False:
        f.write(l)
        l = sc.recv(1024)
        if not l:
            f.close()
            sc.send(b'Copied File')
            a=open(serverNetworkPath + "projectFolderCopied.txt",'w')
            a.write("b'Copied File'")
            a.close()
            break            

    sys.exit()
    sc.close()
    address.close()

s.close()




