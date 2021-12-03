import os
import subprocess

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
serverNetworkPath = pathAntiwave + "server installer\\server\\ServerResources\\antiwave_network\\"
serverConfigNetworkPath=serverNetworkPath+'config\\'

import sys
sys.path.insert(1,InstallPath)
import networkSetup


computers=networkSetup.getWeigthData()



hostnames=[]
ip=[]
cores=[]


renderDirectories=[]
renderDirectoriesSwap=[]
c=0
while c<len(computers):
    hostnames.append(computers[c][4])
    ip.append(computers[c][3])
    cores.append(computers[c][1])
    c+=1





renderDirectories=[]
renderDirectoriesSwap=[]
c=0
while c<len(computers):
    hostnames.append(computers[c][4])
    ip.append(computers[c][3])
    cores.append(computers[c][1])
    c+=1
d=0
while d< len(ip):
    a=open(TempPath+'cancelRender.bat','w')
    a.write('python "'+NetworkPath+'client.py" '+ip[d]+' cancelrender')
    a.close()
    subprocess.call([TempPath+'cancelRender.bat'],shell=True)
    d+=1

    
