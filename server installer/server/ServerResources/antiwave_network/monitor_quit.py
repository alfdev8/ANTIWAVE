import os
import shutil
import time
import subprocess
##import socket

homeDrive=os.environ["HOMEDRIVE"]
localAppData=os.environ["LOCALAPPDATA"]+"\\"
pathAntiwave=homeDrive+"\\ANTIWAVE1.0\\"
pathResources=pathAntiwave+"Resources\\"
pathLVA = pathAntiwave+"LVA\\"
TempPath = pathResources+"Temp\\"                                       
NetworkPath = pathResources+"antiwave_network\\"                        


##server path structure
serverLVAPath = pathAntiwave + "server installer\\server\\LVA\\"
serverScriptsPath = serverLVAPath + "tileScripts\\"
serverTempPath = serverLVAPath + "Temp\\"
serverNetworkPath = pathAntiwave + "server installer\\server\\ServerResources\\antiwave_network\\"
serverConfigNetworkPath=serverNetworkPath+'config\\'


import sys
sys.path.insert(1,serverConfigNetworkPath)
import serverNetworkSetup



   
def getRenderCoordinatesAE(startFrame,endFrame):
    startFrame+='.0'
    endFrame+='.0'
    swap=['','','',startFrame,endFrame]
    swap0=[]
    swap0.append(swap)
    return swap0
    

def loadCoordinates0():
    a=open(serverLVAPath + "coordinates0.txt",'r')
    b=a.read()
    print (b)
    #C:\Users\alf\Documents\maya\projects\default\scenes\[test][2k][200F].mb version
    formatType=b.split('.')[1]
    filenameSwap=b.split('.')[0]
    swap0=filenameSwap.split('\\')
    index=len(swap0)
    filename=swap0[index-1]
    filenameFormat = []
    filenameFormat.append(filename)
    filenameFormat.append(formatType)
    return filenameFormat

def loadCoordinates1():
    a=open(serverLVAPath + "coordinates1.txt",'r')
    b=a.read()
    c=[]
    a.close()

    for x in b:
        if x == '[' or x == ']':

            continue
        else:
            c.append(x)



    swap=''
    for x in c:
        swap+=x
    
    swap=swap.split('*')


    swap2=[]
    d=0
    while d < len(swap):
        swap2.append(swap[d].replace("u'",''))
        d+=1


    swap=[]
    d=0
    while d< len(swap2):
        swap.append(swap2[d].split(','))
        d+=1

    
    swap2=[]
    d=0
    while d< len(swap[0]):

        swap2.append(swap[0][d].replace("'",''))
        d+=1


    swap[0]=swap2

    swap[len(swap)-1].pop()
    swap.pop()


    InitialCoordinates=[]
    swap2=[]
    f=0
    while f<len(swap[0]):
        d=0
        swap2=[]
        while d< len(swap):              

            swap2.append(swap[d][f])
            d+=1
        InitialCoordinates.append(swap2)
        f+=1



    return InitialCoordinates








def loadCoordinates2():    
    a=open(serverLVAPath+'coordinates2.txt','r')
    b=a.read()
    a.close()
    c=b.split('\n')
    renderMode=c[0]
    renderDirectories=c[1].split('@')

    d=2
    weigthDataFile=[]
    while d < len(c):
        weigthDataFile.append(c[d])
        d+=1
    weigthDataFile.pop()
    a=open(serverConfigNetworkPath+'weigthData.txt','w')
    for x in weigthDataFile:
        a.write(x+'\n')
    a.close()
    
    computers=serverNetworkSetup.getWeigthData()
    coordinates2=[]
    coordinates2.append(computers)
    coordinates2.append(list(renderMode))
    
    del renderDirectories[0]
       
    coordinates2.append(renderDirectories)
    return coordinates2

coordinates0=loadCoordinates0()
coordinates1=loadCoordinates1()
coordinates2=loadCoordinates2()
##print (coordinates0)
##print (coordinates1)
##print (coordinates2)


filename = coordinates0
frames =[]
frames.append(coordinates1[0][3].split('.')[0])
frames.append(coordinates1[0][4].split('.')[0])

renderMode = coordinates2[1]
renderFolders = coordinates2[2]


def inspectLast():
    renderDirectoriesIndex=[]    
    correspondRenderDirectories=[]  
    index=[]
    swap=''
    
    d=0
    
    for x in coordinates2[2]:
##        print (x)
        x=x[1:]
        swap = x
        if os.path.exists(swap) is True:
            print('True')
            index.append(d)
            correspondRenderDirectories.append(swap)

            d+=1
    frameToMatch = filename[0] +'_'+ frames[1] +'.iff'

    foldersToDetect=0
    if len(correspondRenderDirectories)==1:
        foldersToDetect=1        
    elif len(correspondRenderDirectories)>1:
        foldersToDetect=len(correspondRenderDirectories)-1




    a=False
    while a is False:
        states=[]
        d=0
        while d < len(correspondRenderDirectories):
            if os.path.exists(serverLVAPath+'renderDone_'+str(d)+'.txt') is True:
                states.append(True)
                d+=1
        a=all(states)
        
        
            




    

    a=True
    while a is True:
        time.sleep(1)
        files=[]
        for x in correspondRenderDirectories:
            files.append([y for y in os.listdir(x) if os.path.splitext(y)[1] in ('.iff')])


        if len(correspondRenderDirectories) == 1:
            
            for x in files:
                for y in x:                    
                    if y == filename[0] +'_'+ frames[1] +'.iff':
                        print ("Finishing...")

                        a=False
        elif len(correspondRenderDirectories) > 1:            
            counter = 0
            for x in files:
                for y in x:                    
                    if y == filename[0] +'_'+ frames[1] +'.iff':
                        print ("Finishing...")
                        print (foldersToDetect)
                        print (counter)
                        
                        counter += 1
                        if counter == foldersToDetect:
                            a=False
    print ("Rendering Done.")
    if os.path.exists(serverLVAPath+'renderToClient') is False:
        os.mkdir(serverLVAPath+'renderToClient')
    files=[]
    for x in correspondRenderDirectories:
        files.append([y for y in os.listdir(x) if os.path.splitext(y)[1] in ('.iff')])


    newDirectories=[]
    for x in correspondRenderDirectories:
        a=x.split('\\')
        a=a[len(a)-1]
        newDirectories.append(a)
        


    #create folders
    for x in newDirectories:
        os.mkdir(serverLVAPath+'renderToClient\\'+x+'\\')
    

    counter0=0
    for x in files:
        for y in x:
            print("Compressing Files")
            
            shutil.copyfile(correspondRenderDirectories[counter0]+'\\'+y,serverLVAPath+'renderToClient\\'+newDirectories[counter0]+'\\'+y)
        counter0+=1
    
   
    a=open(serverLVAPath+'compressTiles.bat','w')
    a.write('CD "'+serverLVAPath+'"\n')
    a.write('python -m tarfile -c "'+serverLVAPath+'renderedTiles.tar" "'+'renderToClient"')
    
    a.close()
    
    subprocess.call([serverLVAPath+'compressTiles.bat'],shell=False)
    
       
def sendCompressedTiles():
    a=open(serverLVAPath+'sendCompressedTiles.bat','w')
    a.write('python "'+serverNetworkPath+'monitor_Client_Server_send.py"')
    a.close()
    subprocess.call([serverLVAPath+'sendCompressedTiles.bat'],shell=False)
    
   
    

            
inspectLast()
print("Sending...")
time.sleep(1)
sendCompressedTiles()
