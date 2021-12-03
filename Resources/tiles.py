import shutil
import os
import subprocess
import re
import time
import execThreads

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



avoidClean=[]


def extractTiles():

    tarFiles=[x for x in os.listdir(pathLVA) if os.path.splitext(x)[1] in ('.tar')]

    
    c=0
    while c< len(tarFiles):
        a=open(TempPath+'extractTile'+str(c)+'.bat','w')
        a.write('CD '+pathLVA+'\n')
        a.write('python -m tarfile -v -e "'+tarFiles[c]+'" '+pathLVA)
        a.close()
        subprocess.call([TempPath+'extractTile'+str(c)+'.bat'],shell=True)

        c+=1

