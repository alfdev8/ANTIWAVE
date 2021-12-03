import subprocess
import os
import socket
import re
import pathlib
import codecs
import time
import sortWeigth
import re



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
serverLVAPath = pathAntiwave + "server installer\\server\\LVA\\"
serverTempPath = serverLVAPath + "Temp\\"
serverNetworkPath = pathAntiwave + "server installer\\server\\ServerResources\\antiwave_network\\"
serverConfigNetworkPath=serverNetworkPath+'config\\'

def createLVA():
    if os.path.exists(pathLVA)!=True:
        os.mkdir(pathLVA)  

def oldNetworkConfig():
    
    if os.path.exists('"'+pathLVA+'oldNetwork.txt"')!=True:
        os.system('netsh dump>"'+pathLVA+'oldNetwork.txt"')

#def restoreNetworkConfig:

        
def getOldHostname():
    
    hostname = socket.gethostname()



    return hostname


    
def changeIP():
    file= open(actualPath+"ipaddress.txt",'r')
    a=file.read()
    b=a.split('.')[3]
    c=ipAddress + b
    file.close()    
   
    file=open(pathLVA+"IP.bat","w")
    file.write("netsh int ip set address "+'"Ethernet"'+" static "+c+" 255.255.255.0 192.168.103.1")
    file.close()

    subprocess.call([pathLVA+"IP.bat"])    
    

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

    file=open(pathLVA+"cpu.bat","w")
    file.write('WMIC cpu get CurrentClockSpeed,NumberOfCores>"'+pathLVA+'cpu.txt"')
    file.close()




    subprocess.call([pathLVA+"cpu.bat"])


    file=open(pathLVA+"cpu.txt",'r')
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
  

def getFreeRAM(RAMoffset=0):
    a=open(pathLVA+"ram.bat",'w')
    a.write('wmic OS get FreePhysicalMemory>"'+pathLVA+'ram.txt"')
    a.close()
    subprocess.call([pathLVA+'ram.bat'])
    a=open(pathLVA+"ram.txt",'r')
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
    a=sortWeigth.sortComputers()


    return a


def sendProjectFolder():
    computers=getWeigthData()
    
    
    ipAdress=[]
    c=0
    while c<len(computers):
        ipAdress.append(computers[c][3])
        c+=1
    print(ipAdress)

    
    if len(ipAdress) == 1:
        a=open(TempPath+"clienttoserver1.bat",'w')
        a.write("python "+NetworkPath+"client.py "+ipAdress[0]+" copyrenderproject")
        a.close()
        subprocess.call([TempPath+"clienttoserver1.bat"],shell=False)
        

        a=open(TempPath+"sendProjectToLVAserver.bat",'w')        
        a.write("python "+NetworkPath+"send_file_client.py " + ipAdress[0])
        a.close()

        subprocess.call([TempPath+"sendProjectToLVAserver.bat"],shell=False)


    elif len(ipAdress) > 1:

        c=0
        while c < len(ipAdress):
            a=open(TempPath+"clienttoserver"+str(c)+".bat",'w')
            a.write("python "+NetworkPath+"client.py "+ipAdress[c]+" copyrenderproject")
            a.close()
            c+=1

        c=0
        while c < len(ipAdress):
            d=subprocess.Popen([TempPath+"clienttoserver"+str(c)+".bat",'ls'],shell=False)
            time.sleep(1) 

            if os.path.isfile(NetworkPath+"projectFolderCopied.txt") is True:
                os.remove(NetworkPath+"projectFolderCopied.txt")

            c+=1
        
        

        
        c=0
        while c < len(ipAdress):
            a=open(TempPath+"sendProjectToLVAserver"+str(c)+".bat",'w')
            a.write("python "+NetworkPath+"send_file_client.py " + ipAdress[c])
            a.close()
            c+=1
        
        
        c=0
        while c < len(ipAdress):
            subprocess.call([TempPath+"sendProjectToLVAserver"+str(c)+".bat"],shell=False)
            c+=1


    
def extractRenderFramesFolder():
    tarFiles=[x for x in os.listdir(pathLVA) if os.path.splitext(x)[1] in ('.tar')]
    
    c=0
    while c< len(tarFiles):
        a=open(TempPath+'extractFramesFolder.bat','w')
        a.write('CD '+pathLVA+'\n')
        a.write('python -m tarfile -v -e "'+tarFiles[c]+'" '+pathLVA)
        a.close()
        subprocess.call([TempPath+'extractFramesFolder.bat'],shell=True)

        c+=1

def compressRenderTileScriptsFolder(projectPath):

    
    a=open(TempPath+"tileScriptFolder.txt",'w')
    a.write(projectPath+'\\')
    a.close()
    

    total_size=0
    start_path=projectPath
    for path, dirs, files in os.walk(start_path):
        for f in files:
            fp= os.path.join(path,f)
            total_size+=os.path.getsize(fp)
    


    print (actualPath)
    d=open(TempPath+"tileScriptsFolder.bat",'w')
    d.write('cd '+TempPath)
    d.write('\npython -m tarfile -c "'+TempPath+'tileScriptsFolder.tar" "' + 'tileScripts' + '"')
    d.close()

    
    p = subprocess.Popen([TempPath+"tileScriptsFolder.bat",'ls'],shell=True)

    d=0
    while True:        
        if os.path.isfile(TempPath+"tileScriptsFolder.tar") is True:
            e=os.path.getsize(TempPath+"tileScriptsFolder.tar")-total_size
            if e < 0:                
                print(e)
            c=os.path.getsize(TempPath+"tileScriptsFolder.tar")
            if c >int(total_size):
                
                print("Preparing project folder...")                
                break
    p.terminate()


def sendScripts(renderMode,tiles=0):
    computers=getWeigthData()
    
    
    hostnames=[]
    ip=[]
    cores=[]
    c=0
    while c<len(computers):
        hostnames.append(computers[c][4])
        ip.append(computers[c][3])
        cores.append(computers[c][1])
        c+=1



    if renderMode == 2:
        
        c=0
        while c < len(ip):
            a=open(TempPath+"startScriptServer"+'_'+str(c)+".bat",'w')
            a.write("python "+NetworkPath+"client.py "+ip[c]+" startrenderframes")
            a.close()
            c+=1
            
        c=0
        while c < len(ip):
            subprocess.call([TempPath+"startScriptServer"+'_'+str(c)+".bat"],shell=False)
            c+=1



            
        c=0
        while c< len(hostnames):
            a=open(TempPath+'send_'+hostnames[c]+'.bat','w')
            a.write('python '+NetworkPath+'send_bat_client_frames.py '+ip[c]+' '+hostnames[c])
            a.close()
            c+=1

        c=0
        while c< len (hostnames):
##            time.sleep(1)
            subprocess.call([TempPath+'send_'+hostnames[c]+'.bat'],shell=False)
            c+=1






            
    elif renderMode == 1:


        
        d=0
        for x in cores:            
            a=open(TempPath+"startScriptServer.bat",'a')
            a.write("python "+NetworkPath+"client.py "+ip[d]+" startrendertiles\n")
            a.close()            
            d+=1
        
        subprocess.call([TempPath+"startScriptServer.bat"],shell=False)
        


        compressRenderTileScriptsFolder(TempPath+'tileScripts')


        
        d=0
        for x in cores:        
            a=open(TempPath+'send_'+hostnames[d]+'.bat','w')
            a.write('python '+NetworkPath+'send_bat_client_tiles.py '+ip[d])
            a.close()
            
            d+=1
            
        
        d=0
        for x in cores:                               
##                time.sleep(1)
                subprocess.call([TempPath+'send_'+hostnames[d]+'.bat'],shell=False)                
                d+=1
        

def startMonitorFrames():
    
    

    
    computers=getWeigthData()

    hostnames=[]
    ip=[]
    cores=[]
    c=0
    while c<len(computers):
        hostnames.append(computers[c][4])
        ip.append(computers[c][3])
        cores.append(computers[c][1])
        c+=1



    rate=1000000
    
    c=0
    while c < len(ip):
        
        
        a=open(TempPath+"startmonitorframes"+'_'+str(c)+".bat",'w')
        a.write("python "+NetworkPath+"client.py "+ip[c]+" startmonitorframes")
        a.close()

        d=0
        while d < rate: 
            d+=1
            
        subprocess.Popen([TempPath+"startmonitorframes"+'_'+str(c)+".bat"],shell=False)
        c+=1


    
    a=open(pathLVA+'clientFrames.bat','w')

    a.write('python "'+NetworkPath+'send_frames_server.py"')
    a.close()
    subprocess.call([pathLVA+'clientFrames.bat','ls'],shell=False) 



def sendCoordinates0():

    computers=getWeigthData()

    hostnames=[]
    ip=[]
    cores=[]
    c=0
    while c<len(computers):
        hostnames.append(computers[c][4])
        ip.append(computers[c][3])
        cores.append(computers[c][1])
        c+=1
    


    totalCores=0
    for x in cores:
        totalCores+=int(x)
        
    d=0
    for x in cores:            
        a=open(TempPath+"startCoords0Server.bat",'a')
        a.write("python "+NetworkPath+"client.py "+ip[d]+" coordinates0\n")
        a.close()            
        d+=1
    
    subprocess.call([TempPath+"startCoords0Server.bat"],shell=False)


    d=0
    for x in cores:            
        a=open(TempPath+"send_coordinates0_client.bat",'a')
        a.write("python "+NetworkPath+'send_coordinates0_client.py '+ip[d]+"\n")
        a.close()            
        d+=1

    
    subprocess.call([TempPath+'send_coordinates0_client.bat'],shell=False)


        
def sendCoordinates1():

    computers=getWeigthData()

    hostnames=[]
    ip=[]
    cores=[]
    c=0
    while c<len(computers):
        hostnames.append(computers[c][4])
        ip.append(computers[c][3])
        cores.append(computers[c][1])
        c+=1
    


    totalCores=0
    for x in cores:
        totalCores+=int(x)
        
    d=0
    for x in cores:            
        a=open(TempPath+"startCoords1Server.bat",'a')
        a.write("python "+NetworkPath+"client.py "+ip[d]+" coordinates1\n")
        a.close()            
        d+=1
    
    subprocess.call([TempPath+"startCoords1Server.bat"],shell=False)


    d=0
    for x in cores:            
        a=open(TempPath+"send_coordinates1_client.bat",'a')
        a.write("python "+NetworkPath+'send_coordinates1_client.py '+ip[d]+"\n")
        a.close()            
        d+=1

    
    subprocess.call([TempPath+'send_coordinates1_client.bat'],shell=False)               

def sendCoordinates2():

    computers=getWeigthData()

    hostnames=[]
    ip=[]
    cores=[]
    c=0
    while c<len(computers):
        hostnames.append(computers[c][4])
        ip.append(computers[c][3])
        cores.append(computers[c][1])
        c+=1
    


    totalCores=0
    for x in cores:
        totalCores+=int(x)
        
    d=0
    for x in cores:            
        a=open(TempPath+"startCoords2Server.bat",'a')
        a.write("python "+NetworkPath+"client.py "+ip[d]+" coordinates2\n")
        a.close()            
        d+=1
    
    subprocess.call([TempPath+"startCoords2Server.bat"],shell=False)


    d=0
    for x in cores:            
        a=open(TempPath+"send_coordinates2_client.bat",'a')
        a.write("python "+NetworkPath+'send_coordinates2_client.py '+ip[d]+"\n")
        a.close()            
        d+=1

    
    subprocess.call([TempPath+'send_coordinates2_client.bat'],shell=False)


    
def startMonitor():
    computers=getWeigthData()
    
    
    hostnames=[]
    ip=[]
    cores=[]
    c=0
    while c<len(computers):
        hostnames.append(computers[c][4])
        ip.append(computers[c][3])
        cores.append(computers[c][1])
        c+=1
    
    
    
    

    totalCores=0
    for x in cores:
        totalCores+=int(x)


    a=open(TempPath+"startMonitorServerToClient.bat",'w')
    d=0
    for x in cores:                    
        a.write("python "+NetworkPath+"client.py "+ip[d]+" startmonitortiles\n")        
        d+=1
    a.close()
    


    subprocess.call([TempPath+"startMonitorServerToClient.bat"],shell=False)


    

    #start server to Client  => client to Server
    a=open(TempPath+'monitor_Server_Client_send.bat','w')

    a.write('title TilesAW1\n')        
    a.write('python '+NetworkPath+'monitor_Server_Client_send.py')        

    a.close()
        


    subprocess.Popen([TempPath+'monitor_Server_Client_send.bat'],shell=False)

    






def shutdownServers():

    computers=getWeigthData()

    ipAdress=[]
    c=0
    while c<len(computers):
        ipAdress.append(computers[c][3])
        c+=1
    print(ipAdress)

    
    if len(ipAdress) == 1:
        a=open(TempPath+"shutdownservers.bat",'w')
        a.write("python "+NetworkPath+"client.py "+ipAdress[0]+" shutdown")
        a.close()
        subprocess.call([TempPath+"shutdownservers.bat"],shell=False)
        



    elif len(ipAdress) > 1:

        c=0
        while c < len(ipAdress):
            a=open(TempPath+"shutdownservers"+str(c)+".bat",'w')
            a.write("python "+NetworkPath+"client.py "+ipAdress[c]+" shutdown")
            a.close()
            c+=1

        c=0
        while c < len(ipAdress):
            d=subprocess.Popen([TempPath+"shutdownservers"+str(c)+".bat",'ls'],shell=False)
##            time.sleep(1) 
            c+=1
        



def restartServers():
    computers=getWeigthData()

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
    d=0
    while d< len(ip):
        a=open(TempPath+'restartRender.bat','w')
        a.write('python "'+NetworkPath+'client.py" '+ip[d]+' restart')
        a.close()
        subprocess.call([TempPath+'restartRender.bat'],shell=True)
        d+=1

