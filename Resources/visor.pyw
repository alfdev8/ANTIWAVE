import tkinter as tk
import subprocess
import time
import os
import re
import shutil
import getEnviromentVariable
import tiles



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
import sortWeigth




def getFolderBrowserNetwork():    
    subprocess.call([pathResources+"Render Project Folder.exe"]) 
    b=''
    while True: 
        if os.path.isfile(TempPath+"projectFolder.txt") is True:
            a=open(TempPath+"projectFolder.txt",'r')
            b=a.read()
            a.close()
            break
    uploadProject(b) 

def getFolderBrowserUSB():
    subprocess.call([pathResources+"Render Project Folder.exe"])


def getFileBrowser():
    if os.path.exists(TempPath+'LoadFile.txt') is True:
        os.remove(TempPath+'LoadFile.txt')
    subprocess.call([pathResources+"Load File.exe"]) 
    b=''
    while True:  
        if os.path.isfile(TempPath+"LoadFile.txt") is True:
            a=open(TempPath+"LoadFile.txt",'r')
            b=a.read()
            a.close()
            break

    c = b.split('.')
    c=c[len(c)-1]

    d=getRenderTypes(c)

    if d == '1':
        #maya        
        e=getEnviromentVariable.getMayaPath()
        a=open(TempPath+"mayaGetFileInfo.bat",'w')
        a.write('"'+e +'mayapy.exe" "'+ pathResources+ 'mayaGetFileInfo.py" "' + b+'"')
        a.close()    
        subprocess.Popen([TempPath+"mayaGetFileInfo.bat"],shell=False)
        
        #after effects
    elif d=='2':
        print ("After Effects")

   
def uploadProject(projectPath):   
    networkSetup.compressRenderProjectFolder(projectPath)   
    networkSetup.sendProjectFolder()   


def getRenderTypes(renderType):

    renderProgram = ''
    if renderType == 'mb' or renderType == 'ma':
        #maya
        #rendermode = 1 tile mode and frame mode        
        renderModesTile.select()
        renderProgram = '1'
    elif renderType == 'aep':
        #ae
        #rendermode = 2 frame mode
        renderModesFrame.select()
        renderProgram = '2'
    return renderProgram

    
def startRender(syntaxType='maya', syntaxVersion='10'):    
    

    j=sortWeigth.getRenderCoordinates()
    frames=''
    tiles=''
    syntaxType=''
    syntaxVersion=''
    k=''
    l=''
    if renderType.get() == 1 and renderModes.get()==1 :
        k=sortWeigth.setRenderCoordinates(renderModes.get(),j,renderType.get())
        l=sortWeigth.setRenderCoordinates(2,j,renderType.get())
        syntaxType="maya"
        syntaxVersion='10'
        print("mentalray Tile mode enabled" )
##        print (k)
##        print (l)

        
        
    elif renderType.get() == 2 and renderModes.get()==1 :
        k=sortWeigth.setRenderCoordinates(renderModes.get(),j,renderType.get())
        l=sortWeigth.setRenderCoordinates(2,j,renderType.get())
        syntaxType='maya'
        syntaxVersion='10'
        print("Maya Software Tile mode enabled")
##        print (k)
##        print (l)

        
    elif renderType.get() == 1 and renderModes.get() ==2 :
        l=sortWeigth.setRenderCoordinates(renderModes.get(),j,renderType.get())
        syntaxType='maya'  
        syntaxVersion='10'
        print("mentalray Frames mode enabled")
##        print (k)


    
    elif renderType.get() == 2 and renderModes.get()==2 :
        l=sortWeigth.setRenderCoordinates(renderModes.get(),j,renderType.get())
        syntaxType='maya'
        syntaxVersion='10'
        print("Maya Software Frames mode enabled")
##        print (k)
        



    d=sortWeigth.loadSyntax(syntaxType,syntaxVersion,renderModes.get(),renderType.get(),l,k)

##    print (d)



    
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
    
    
 
    if renderModes.get() == 1: 


        c=0
        for x in hostnames:
            if os.path.exists(TempPath+'tileScripts\\'):
                a=open(TempPath+"removeDirs.bat",'w')
                a.write("RMDIR /S /Q "+TempPath+x)
                a.close()
                subprocess.call([TempPath+"removeDirs.bat"],shell=False)
                os.mkdir(TempPath+'tileScripts\\'+x)
            else:
                os.mkdir(TempPath+'tileScripts\\')
                os.mkdir(TempPath+'tileScripts\\'+x)
            c+=1



        c=0
        for x in d:
            part0=x.split('-rd')[0]
            part1=x.split('-rd')[1]
            swap0 = '-rd'+part1.split(' ')[0]             
            
            swap0 += part1.replace("renderToClient\\","$VARIABLETOCHANGE$")
            d[c]=part0 + swap0
            c+=1


            
        


        print (k[0])

        f=0
        c=0
        for x in cores:
            
            e=0
            
            while e<int(x):

                tiles=str(k[f][e])
                tiles=tiles.replace('[','')
                tiles=tiles.replace(']','')
                tiles=tiles.replace(' ','_')
                tiles=tiles.replace(',','')
                tiles=tiles.replace("'",'')

                swap0=os.path.normpath(d[c].replace("$VARIABLETOCHANGE$",tiles+'_'+hostnames[f]))
                d[c]=swap0
                e+=1
                c+=1
            f+=1


        print (d)

        
        c=0
        for x in d:
            d[c]=x.replace('\\"','"')
            c+=1

        
        c=0
        for x in d:
            part0=x.split('-rd')
            swap0='-rd'+part0[1].split('-s')[0]
            
            indexSwap0=len(swap0)
            swap0=swap0[:indexSwap0-2]
            
            
            renderDirectories.append(swap0)

            c+=1

        print (renderDirectories)            

        
        indexRD=len(renderDirectories)
        f=0
        e=0
        for x in cores:            
            c=0
            while c<int(x):
                a=open(TempPath+"tileScripts\\"+hostnames[f]+'\\'+hostnames[f]+'_'+str(c)+'.bat','a')
                a.write('MD "'+renderDirectories[e][5:]+'"'+'\n')
                renderDirectoriesSwap.append(renderDirectories[e][4:])
                a.close()                
                c+=1
                e+=1
            f+=1


        f=0
        e=0
        for x in cores:            
            c=0
            
            while c<int(x):
                a=open(TempPath+"tileScripts\\"+hostnames[f]+'\\'+hostnames[f]+'_'+str(c)+'.bat','a')
                b=str(d[e]).replace('[','')
                b=b.replace(']','')
                b=b.replace("'",'')
                a.write(b+'\n')
                a.close()                
                c+=1
                e+=1
            f+=1
        f=0
        e=0
        for x in cores:            
            c=0
            
            while c<int(x):
                a=open(TempPath+"tileScripts\\"+hostnames[f]+'\\'+hostnames[f]+'_'+str(c)+'.bat','a') #'a' attribute not need to repeat
                
                a.write('echo renderTilesDone>"'+serverLVAPath+'renderDone_'+str(c)+'.txt"')
                a.close()                
                c+=1
                e+=1
            f+=1



        

        networkSetup.sendScripts(renderModes.get(),k)

        a=open(TempPath+'coordinates2.txt','w')
        a.write(str(renderModes.get())+'\n')

        for x in renderDirectories:
            a.write('@'+x[4:])

        a.write('\n')
        
        b=open(InstallPath+'weigthData.txt','r')
        c=b.read()
        b.close()

        a.write(c)
        a.close()


    
    if os.path.isfile(TempPath+'coordinates2.txt'):
        networkSetup.sendCoordinates0()
        networkSetup.sendCoordinates1()
        networkSetup.sendCoordinates2()
        networkSetup.startMonitor() #error 
        
    #start monitor

    
    #client Side
       
##        c=0
##        while True:
##            tarFiles=[f for f in os.listdir(pathLVA) if os.path.isfile(os.path.join(pathLVA,f))]
##            tarFiles.sort(key=lambda f: int(re.sub('\D','',f)))
##            print (tarFiles)
##            print (str(len(tarFiles)) + str(len(hostnames)))
##            if len(tarFiles) == len(hostnames):
##                
##                print ("Closing Window")
##                
##                b=open(TempPath+'getwindowpid.bat','w')
##                b.write('tasklist /v /fo csv | findstr /i "TilesAW1">'+TempPath+'\\getwindowpid.txt')
##                b.close()
##                subprocess.call([TempPath+'getwindowpid.bat'],shell=False)
##
##                b=open(TempPath+'\\getwindowpid.txt','r')
##                c=b.read()
##                b.close()
##                c=c.split(',')
##                c=c[1]
##                c.replace('"','')
##
##                
##                a=open(TempPath+'closeWindow.bat','w')
##                a.write('taskkill /pid '+c)                
##                a.close()
##                subprocess.call([TempPath+'closeWindow.bat'],shell=False)
##                break
##            else:
##                continue
##            
##            
##            c+=1
                 



    elif renderModes.get() == 2:
##        print (d)
        c=0
        for x in d:
            a=open(TempPath+hostnames[c]+'.bat','w')
            b=str(x).replace('[','')
            b=b.replace(']','')
            b=b.replace("'",'')
            d=b.split("-rd ")[1]
            path=d.split(" -s")[0]
            
            a.write("MD "+os.path.normpath(path)+"\n")
            a.write(b+"\n")
            a.write('echo renderFramesDone>"'+serverLVAPath+'renderDone.txt"')
            a.close()
            
            c+=1



        networkSetup.sendScripts(renderModes.get())
        
        networkSetup.startMonitorFrames()

        #networkSetup.extractRenderFramesFolder()           
        #extract with winrar, buy WINRAR



def shutdownServers(state):
    
    if state==0:
        print (state)

        shutdownWarning.set(1)
        buttonShutdownVar.set("Are you sure to shutdown all servers?")
        buttonShutdownMsg.pack()
        
    elif state==1:
        print('Powering off servers')
        networkSetup.shutdownServers()



def restartServers(state):
    
    if state==0:
        print (state)

        restartWarning.set(1)
        buttonRestartVar.set("Are you sure to restart all servers?")
        buttonRestartMsg.pack()
        
    elif state==1:
        print('Restarting servers')
        networkSetup.restartServers()

    

def reestConnection(): 
    print ("Checking connection")
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

    d=0
    while d < len(ip):        
        a=open(TempPath+'reestablishconnection.bat','w')
        a.write('python  ' +'"'+NetworkPath +'client.py" '+ip[d]+' resetconnection ')
        a.close()
        subprocess.call([TempPath+'reestablishconnection.bat'],shell=True)
        d+=1
    


def cleanServer():
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
    d=0
    while d< len(ip):
        a=open(TempPath+"cleanServer_"+str(d)+".bat",'w')
        a.write('python ' +NetworkPath +'client.py '+ip[d]+' deleteproject')
        a.close()
        subprocess.call([TempPath+"cleanServer_"+str(d)],shell=True)
        d+=1
    


def changeRenderEngine(state):
    if state == False:
        a=open(TempPath+"visor.bat",'w')
        a.write("python "+pathResources+"visor.pyw")
        a.close()
        subprocess.Popen([TempPath+'visor.bat'],shell=False)
        exit()
        
    elif state == True:
        a=open(TempPath+"visormr.bat",'w')
        a.write("python "+pathResources+"visormr.pyw")
        a.close()
        subprocess.Popen([TempPath+'visormr.bat'],shell=False)
        exit()
    elif state == None:
        a=open(TempPath+"ae.bat",'w')
        a.write("python "+pathResources+"visorAE.pyw")
        a.close()
        subprocess.Popen([TempPath+'ae.bat'],shell=False)
        exit()
        
def resetWorkspace():    
    shutil.rmtree(TempPath)
    time.sleep(1)
    os.mkdir(TempPath)        
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

    
    d=0
    while d< len(ip):
        a=open(TempPath+"cleanWorkspace_"+str(d)+".bat",'w')
        a.write('python ' +NetworkPath +'client.py '+ip[d]+' cleanworkspace')
        a.close()
        subprocess.call([TempPath+"cleanWorkspace_"+str(d)+'.bat'],shell=False)
        d+=1
    

def aboutBox():
    a=open(TempPath+"aboutBox.bat",'w')
    a.write('python "' +pathResources +'aboutBox.py"')
    a.close()
    subprocess.call([TempPath+"aboutBox.bat"],shell=True)
    



window = tk.Tk()
window.title("ANTIWAVE 1.0")


frame_buttons = tk.Frame(window, relief=tk.FLAT, bd=120 ,bg="black")


fileMenu = tk.Menu(tearoff=0)
fileMenu.add_command(label='About', command=aboutBox)


a = tk.Menu(window)
a.add_cascade(label="About", menu=fileMenu) 
window.config(menu=a)



buttonReset = tk.Button(frame_buttons,text="Reset", command=resetWorkspace)     

buttonLoadFile = tk.Button(frame_buttons,text="Load File", command=getFileBrowser)   









buttonUploadProject = tk.Button(frame_buttons,text="Upload project folder", command=getFolderBrowserNetwork)     

buttonUploadProjectUSB = tk.Button(frame_buttons,text="Use last project folder", command=getFolderBrowserUSB)

renderType= tk.IntVar()

renderModes=tk.IntVar()





    
    

renderModesFrame=tk.Radiobutton(frame_buttons,text="Frames",variable=renderModes,value=2)
renderModesTile=tk.Radiobutton(frame_buttons,text="Tile",variable=renderModes,value=1)








checkRenderTypemr=tk.Checkbutton(frame_buttons,text="mentalray",variable=renderType,onvalue=1,offvalue=1,command=lambda:changeRenderEngine(True))
checkRenderTypeSw=tk.Checkbutton(frame_buttons,text="Maya Software",variable=renderType,onvalue=2, offvalue=2,command=lambda:changeRenderEngine(False))

checkRenderTypeAE=tk.Checkbutton(frame_buttons,text="After Effects",variable=renderType,onvalue=3, offvalue=3,command=lambda:changeRenderEngine(None))
checkRenderTypeSw.select()




buttonStartRender=tk.Button(frame_buttons,text="Render", command=lambda: startRender())                                                                    

buttonCleanServer=tk.Button(frame_buttons,text="Clean Server", command=lambda:cleanServer() )
reestConnectionToServer=tk.Button(frame_buttons,text="Check server connection", command=lambda:reestConnection() )


buttonCancel = tk.Button(frame_buttons,text="Restart servers",command=lambda: restartServers(restartWarning.get()))#taskkill
buttonRestartVar=tk.StringVar()
buttonRestartMsg= tk.Message(frame_buttons,textvariable=buttonRestartVar,bg='orange',fg='black')



buttonShutdownVar=tk.StringVar()
buttonShutdownMsg= tk.Message(frame_buttons,textvariable=buttonShutdownVar,bg='orange',fg='black')


buttonShutdown = tk.Button(frame_buttons,text="Shutdown servers",command=lambda: shutdownServers(shutdownWarning.get()))




frame_buttons.pack()


buttonReset.pack()
buttonLoadFile.pack()



renderModesFrame.pack()
renderModesTile.pack()


checkRenderTypeSw.pack()
checkRenderTypemr.pack()
checkRenderTypeAE.pack()
buttonStartRender.pack()
buttonCleanServer.pack()
reestConnectionToServer.pack()
buttonUploadProjectUSB.pack()
buttonUploadProject.pack()





buttonCancel.pack()


shutdownWarning=tk.IntVar()
restartWarning=tk.IntVar()
buttonShutdown.pack()




window.mainloop()
