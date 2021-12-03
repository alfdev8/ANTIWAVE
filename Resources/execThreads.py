import shutil
import os
import subprocess
import re


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



def getResolution():
    a=open(TempPath+'dataForCoordinates.txt','r')
    b=a.read()
    a.close()
    c=b.split('*')
    print (c)
    resX=c[1]
    resX=resX.replace('[','')
    resX=resX.replace(']','')
    print (resX)
    resY=c[2]
    resY=resY.replace('[','')
    resY=resY.replace(']','')
    print (resY)
    RAMspace=int(resX)*int(resY)
    print (RAMspace)
    RAMspaceMB=RAMspace/1024
    print  (RAMspaceMB)
    return (RAMspaceMB)


def getThreadsPossible():
    usedRAMperThread=getResolution()
    freeRAM=networkSetup.getFreeRAM()
    threads=freeRAM/usedRAMperThread
    print(threads)
    return threads
