import shutil
import os
homeDrive=os.environ["HOMEDRIVE"]
pathAntiwave=homeDrive+"\\ANTIWAVE1.0\\"

##server path structure
serverLVAPath = pathAntiwave + "server installer\\server\\LVA\\"
serverTempPath = serverLVAPath + "Temp\\"
serverNetworkPath = pathAntiwave + "server installer\\server\\ServerResources\\antiwave_network\\"
serverConfigNetworkPath=serverNetworkPath+'config\\'


a=open(serverConfigNetworkPath+'ipaddress.txt','w')
a.write('192.168.103.2')
a.close()


os.remove(serverConfigNetworkPath+'weigthData.txt')




#if it returns error means is well configured
#if no error is given means was not configured
