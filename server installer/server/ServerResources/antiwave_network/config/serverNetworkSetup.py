import subprocess
import os
import socket
import re
import pathlib
import codecs
import time
import serverSortWeigth



homeDrive=os.environ["HOMEDRIVE"]
localAppData=os.environ["LOCALAPPDATA"]+"\\"
pathAntiwave=homeDrive+"\\ANTIWAVE1.0\\"
pathResources=pathAntiwave+"Resources\\"
pathLVA = pathAntiwave+"LVA\\"
binPath = pathResources+"bin\\"                                         
TempPath = pathResources+"Temp\\"                                       
InstallPath = pathResources+"antiwave_install\\"                        
NetworkPath = pathResources+"antiwave_network\\"                        
actualPath=str(pathlib.Path(__file__).parent.absolute())+"\\"

ipAddress="192.168.103." 


##server path structure
serverLVAPath = pathAntiwave + "server\\LVA\\"
serverTempPath = serverLVAPath + "Temp\\"
serverNetworkPath = pathAntiwave + "server\\ServerResources\\antiwave_network\\"


  

def oldNetworkConfig():
    
    if os.path.exists(actualPath+'oldNetwork.txt')!=True:
        os.system('netsh dump>"'+actualPath+'oldNetwork.txt"')

#def restoreNetworkConfig:

        
def getOldHostname():
    
    hostname = socket.gethostname()

    file=open(actualPath+"oldHostname.txt","w")
    file.write(hostname)
    file.close()
    return hostname

def setHostname():


    file= open(actualPath+"ipaddress.txt",'r')
    a=file.read()
    b=a.split('.')[3]
    
    file.close()
    
    hostname=getOldHostname()
    file = open(actualPath+"setHostname.bat",'w')
    file.write("WMIC computersystem where caption='" + hostname + "' rename antiwave" + b)
    file.close()

    subprocess.call([actualPath+"setHostname.bat"])

    newHostName = "antiwave" + b
    return newHostName

##def restoreNetworkSettings():
    #netsh run script
    #set old hostname
    
def changeIP():
    file= open(actualPath+"ipaddress.txt",'r')
    a=file.read()
    b=a.split('.')[3]
    c=ipAddress + b
    file.close()    
   
    file=open(actualPath+"IP.bat","w")
    file.write("netsh int ip set address "+'"Ethernet"'+" static "+c+" 255.255.255.0 192.168.103.1")
    file.close()

    subprocess.call([actualPath+"IP.bat"])    
    
    
    file= open(actualPath+"ipaddress.txt",'w')
    b=int(b)+1
    file.write(ipAddress+str(b))
    file.close()
    return c


def getThreadsSupported(cpuOffset=0, RAMoffset=0):
    cpuCores=getWeigth(cpuOffset)
    freeRam=getFreeRAM(RAMoffset)
    RAMthreadsSupported=int(freeRam/cpuCores[0])
    freeRAMcpuWeigth=[RAMthreadsSupported,cpuCores[0],cpuCores[1]]

    return freeRAMcpuWeigth


def getWeigth(cpuOffset):
    file=open(actualPath+"cpu.bat","w")
    file.write('WMIC cpu get CurrentClockSpeed,NumberOfCores>"'+actualPath+'cpu.txt"')
    file.close()
    subprocess.call([actualPath+"cpu.bat"])

    file=open(actualPath+"cpu.txt",'r')
    a=file.read()
    file.close()
    c=re.sub("[^0-9]","",a)

    cpuSpeed=''
    counter=0
    for x in c:        
        if counter == 4:            
            break
        cpuSpeed+=x
        counter+=1


    cpuCoresLength=len(c)-counter 

    cpuCores=int(c[4:cpuCoresLength+4]) - cpuOffset



    padding='0000000'
    zero='0'
    weigth=str(int(cpuSpeed)*int(cpuCores))
    dif=len(padding)-len(weigth)

    weigthInverted=[]
    counter=0
    while counter < dif:
        weigthInverted.append(zero)

        counter+=1
    

    weigthInverted.append(weigth)
    
    convertString=str(weigthInverted)
    totalWeigth=''
 
    for x in convertString:
        if x.isalnum() is True:
            totalWeigth+=x
 
    total=[]
    total.append(cpuCores)
    total.append(totalWeigth)
    return total
  

def getFreeRAM(RAMoffset):
    a=open(actualPath+"ram.bat",'w')
    a.write('wmic OS get FreePhysicalMemory>"'+actualPath+'ram.txt"')
    a.close()
    subprocess.call([actualPath+'ram.bat'])
    a=open(actualPath+"ram.txt",'r')
    b=a.read()
    a.close()
    ramBytes=''
    
    for x in b:
        if x.isdigit() is True:
            ramBytes+=x
    MB=1024
    ramBytes=(int(int(ramBytes)/MB))-RAMoffset

    return ramBytes

def saveData(data):
    file=open(actualPath+"weigthData.txt","a")
    counter=0
    for x in data:
        file.write(str(data[counter])+"*")
        counter+=1
    file.write('\n') 
    file.close()

def compressRenderProjectFolder(projectPath):


    a=open(TempPath+"projectFolder.txt",'w')
    a.write(projectPath+'\\')
    a.close()
    

    total_size=0
    start_path=projectPath
    for path, dirs, files in os.walk(start_path):
        for f in files:
            fp= os.path.join(path,f)
            total_size+=os.path.getsize(fp)



    d=open(pathResources+"Temp\\projectFolderCompress.bat",'w')
    d.write('python -m tarfile -c "'+TempPath+'projectFolder.tar" "' + projectPath + '"')
    d.close()


    p = subprocess.Popen([TempPath+"projectFolderCompress.bat",'ls'],shell=True)

    d=0
    while True:        
        if os.path.isfile(TempPath+"projectFolder.tar") is True:
            e=os.path.getsize(TempPath+"projectFolder.tar")-total_size
            if e < 0:                
                print(e)
            c=os.path.getsize(TempPath+"projectFolder.tar")
            if c >int(total_size):
                
                print("Preparing project folder...")                
                break
    p.terminate()


def getWeigthData():
    a=serverSortWeigth.sortComputers()

    return a


def sendProjectFolder():
    computers=getWeigthData()
    ipAdress=[]
    c=0
    while c<len(computers):
        ipAdress.append(computers[c][3])
        c+=1
    print(ipAdress)


    a=open(TempPath+"clienttoserver1.bat",'w')

    a.write("python "+NetworkPath+"client.py 127.0.0.1 copyrenderproject")
    a.close()
    subprocess.call([TempPath+"clienttoserver1.bat"],shell=False)
    


    a=open(TempPath+"sendProjectToLVAserver.bat",'w')
    a.write("python "+NetworkPath+"send_file_client.py")
    a.close()

    subprocess.call([TempPath+"sendProjectToLVAserver.bat"],shell=False)

