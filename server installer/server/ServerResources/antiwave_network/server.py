import socket              
import codecs 
import os
import subprocess
import shutil


homeDrive=os.environ["HOMEDRIVE"]
localAppData=os.environ["LOCALAPPDATA"]+"\\"
pathAntiwave=homeDrive+"\\ANTIWAVE1.0\\"
pathResources=pathAntiwave+"Resources\\"
pathLVA = pathAntiwave+"LVA\\"
TempPath = pathResources+"Temp\\"                                       
NetworkPath = pathResources+"antiwave_network\\"                        

##server path structure
serverLVAPath = pathAntiwave + "server installer\\server\\LVA\\"
serverTempPath = serverLVAPath + "Temp\\"
serverNetworkPath = pathAntiwave + "server installer\\server\\ServerResources\\antiwave_network\\"
serverConfigNetworkPath=serverNetworkPath+'config\\'



import sys
sys.path.insert(1,serverConfigNetworkPath)
import serverNetworkSetup


s = socket.socket()         
host = socket.gethostname() 
port = 12345                
ip=socket.gethostbyname(host) 
s.bind((ip, port))           
print (host+ip)
s.listen(10)                 
while True:
   c, addr = s.accept()     
   print ('Got connection from ', addr)
   c.send(b'Thank you for connecting')

   b=c.recv(512)
   c.send(b'1')
   if b == b'copyrenderproject':                                                       #Before render
      print("copyrenderproject")
      c.send(b'2')
   
      a=open(serverNetworkPath + "sendFileServer.bat",'w')
      a.write('python "' + serverNetworkPath + 'send_file_server.py"')
      a.close()

      subprocess.call([serverNetworkPath+'sendFileServer.bat'],shell=False) 

      
      

      swapSymbol=serverLVAPath
      
      swapSymbol0=[]

      for x in swapSymbol:
         swapSymbol0.append(x)
      
      swapSymbol0.pop()
      swapSymbol1=''
      for x in swapSymbol0:
         swapSymbol1+=x
         

##      print (swapSymbol1)
         
      

      while True:
         if os.path.isfile(serverNetworkPath + "projectFolderCopied.txt") is True:
            a=open(serverNetworkPath + "projectFolderCopied.txt",'r')
            b=a.read()
            a.close()
            if b=="b'Copied File'":

               e=open(serverNetworkPath+"extractProjectFile.bat",'w')


              
               
               e.write('python -m tarfile -v -e "'+serverLVAPath+'projectFolder.tar" "'+ swapSymbol1+'"\necho finish extraction>"'+serverLVAPath+'extraction.txt"')
               e.close()
               subprocess.Popen([serverNetworkPath+"extractProjectFile.bat"],shell=False)            
               
             
               while os.path.isfile(serverLVAPath+"extraction.txt") is False:
                  total_size=0
                  start_path=serverLVAPath
                  for path, dirs, files in os.walk(start_path):
                    for f in files:
                        fp= os.path.join(path,f)
                        total_size+=os.path.getsize(fp)
                  print("Please wait..."+str(total_size))
                  
                  if os.path.isfile(serverLVAPath+"extraction.txt") is True:
                     
                     print ("Done.")
                     break
                  

               break
               
      
      
      
   elif b == b'startrenderframes':
      print("startrenderframes")
      c.send(b'3') 
      
      a=open(serverNetworkPath+'send_bat_server_frames.bat','w')
      a.write('python "'+serverNetworkPath+'send_bat_server_frames.py"')
      a.close()
      subprocess.call([serverNetworkPath+'send_bat_server_frames.bat'],shell=False)


      state=None
      while True:
         if os.path.exists(serverLVAPath+'copiedRenderScript.txt') is True:
            state=True
            break
      
      index=0
      if state is True:
         files= [x for x in os.listdir(serverLVAPath) if os.path.splitext(x)[1] in ('.bat')]
##         print (files)
         for x in files:
            if x.split('renderScript_0') is True:
               break
            elif x.split('renderScript_0') is False:
               index+=1


##         print(files[index-2])
         subprocess.call([serverLVAPath+files[index-2]],shell=False) 
         

         

   elif b == b'aestartrenderframes':
      print('aestartrenderframes')
      c.send(b'3') 
      
      a=open(serverNetworkPath+'send_bat_server_frames.bat','w')
      a.write('python "'+serverNetworkPath+'send_bat_server_frames.py"')
      a.close()
      subprocess.call([serverNetworkPath+'send_bat_server_frames.bat'],shell=False)


      state=None
      state0=True
      while state0 is True:
         if os.path.exists(serverLVAPath+'copiedRenderScript.txt') is True:
            state=True
            state0=False
            break
      
      index=0
      if state is True:
         files= [x for x in os.listdir(serverLVAPath) if os.path.splitext(x)[1] in ('.bat')]
##         print (files)
         d=0
         while d< len(files):

            if files[d].split('renderScript_0') is True:
               d=len(files)
            elif files[d].split('renderScript_0') is False:
               index+=1
            d+=1


##         print(files[index-2])
         subprocess.call([serverLVAPath+files[index-2]],shell=False)
      
   elif b == b'startrendertiles':         #1
      
      print("startrendertiles")
      c.send(b'3')

      swapSymbol=serverLVAPath
      
      swapSymbol0=[]
      c=0
      for x in swapSymbol:
         swapSymbol0.append(x)
      
      swapSymbol0.pop()
      swapSymbol1=''
      for x in swapSymbol0:
         swapSymbol1+=x
      
      a=open(serverNetworkPath+'send_bat_server_tiles.bat','w')
      a.write('python "'+serverNetworkPath+'send_bat_server_tiles.py"')
      a.close()
      subprocess.call([serverNetworkPath+'send_bat_server_tiles.bat'],shell=False)


 


      if os.path.isfile(serverNetworkPath + "tileScriptsFolderCopied.txt") is True:
         e=open(serverNetworkPath+"tileScriptsFolder.bat",'w')               
         e.write('python -m tarfile -v -e "'+serverLVAPath+'tileScriptsFolder.tar" "'+ swapSymbol1+'"\necho finish extraction>"'+serverLVAPath+'extraction.txt"')
         e.close()
         subprocess.call([serverNetworkPath+"tileScriptsFolder.bat",'ls'],shell=False)            
         

         while os.path.isfile(serverLVAPath+"extraction.txt") is False:
            total_size=0
            start_path=serverLVAPath
            for path, dirs, files in os.walk(start_path):
              for f in files:
                  fp= os.path.join(path,f)
                  total_size+=os.path.getsize(fp)
            print("Please wait..."+str(total_size))
            
            if os.path.isfile(serverLVAPath+"extraction.txt") is True:

               print ("Done.")
               break



      hostname=serverNetworkSetup.getOldHostname()

      files=os.listdir(serverLVAPath+'tileScripts\\'+hostname)
##      print (files)
      
      c=0
      for x in files:
         a=open(serverLVAPath+'tileScripts\\'+hostname+'\\'+str(c)+'.bat','w')
         a.write('"'+serverLVAPath+'tileScripts\\'+hostname+'\\'+x+'"')
         a.close()
         c+=1


      c=0
      for x in files:         
         subprocess.Popen([serverLVAPath+'tileScripts\\'+hostname+'\\'+str(c)+'.bat'],shell=False)
         c+=1


   elif b == b'coordinates2':
      print ("coordinates2")
      c.send(b'6')
      
      a=open(serverNetworkPath+'send_coordinates2_server.bat','w')
      a.write('python "'+serverNetworkPath+'send_coordinates2_server.py"')
      a.close()
      subprocess.call([serverNetworkPath+'send_coordinates2_server.bat'],shell=False)
      


   elif b == b'coordinates1':
      print ("coordinates1")
      c.send(b'6')
      
      a=open(serverNetworkPath+'send_coordinates1_server.bat','w')
      a.write('python "'+serverNetworkPath+'send_coordinates1_server.py"')
      a.close()
      subprocess.call([serverNetworkPath+'send_coordinates1_server.bat'],shell=False)

   elif b == b'coordinates0':
      print ("coordinates0")
      c.send(b'6')
      
      a=open(serverNetworkPath+'send_coordinates0_server.bat','w')
      a.write('python "'+serverNetworkPath+'send_coordinates0_server.py"')
      a.close()
      subprocess.call([serverNetworkPath+'send_coordinates0_server.bat'],shell=False)
      
   elif b == b'startmonitortiles':   #2
      print ("startmonitortiles")
      c.send(b'6')
      
      a=open(serverNetworkPath+'startMonitor.bat','w')
      a.write('python "' + serverNetworkPath+'monitor_quit.py"')
      a.close()
      subprocess.call([serverNetworkPath+'startMonitor.bat'],shell=False)
         
      
      
   elif b==b'startmonitorframes':
      print("startmonitorframes")
      c.send(b'6')


      hostname=serverNetworkSetup.getOldHostname()

      hostnameIndex=''
      for x in hostname:
         if str.isnumeric(x) is True:
            hostnameIndex+=x
      hostnameIndex=str(int(hostnameIndex)-2)

      a=open(serverLVAPath + "renderScript_0.bat",'r')
      b=a.read()
      c0=b.split('-s')[1]
      c0=c0.split('-rt')[0]
      c0=c0.split('-e')
      frames=[]
      frames.append(int(c0[0]))
      frames.append(int(c0[1].split(' -mm')[0]))

      c0=b.split('-rd')[1]
      renderDirectorie=c0.split('-s')[0]
      
      state=True
      while state is True:
         if os.path.exists(serverLVAPath+"renderDone.txt") is True:
  
            a=open(serverLVAPath+"renderFolderFrames.bat",'w')
            swap0 = renderDirectorie.replace("RENDER",'')
##            print (swap0)
##            print (swap0[2:index-2]+'renderedFrames.tar')
            a.write("cd "+swap0+'\n')
            a.write('python -m tarfile -c renderedFrames.tar RENDER')
            a.close()
            
            index=len(swap0)
            
##            print(swap0)
            subprocess.call([serverLVAPath+"renderFolderFrames.bat"],shell=False)  
            shutil.copyfile(swap0[2:index-2]+'renderedFrames.tar',serverLVAPath+"renderedFrames_"+hostnameIndex+'.tar')   #error maybe
   
            state=False

            a=open(serverLVAPath+'serverFrames.bat','w')
            a.write('python "'+serverNetworkPath+'send_frames_client.py"')
            a.close()
            subprocess.call([serverLVAPath+'serverFrames.bat'],shell=False)  
            
            
      
      
   elif b==b'aestartmonitorframes':
      print("aestartmonitorframes")
      c.send(b'6')
   
      hostname=serverNetworkSetup.getOldHostname()

      hostnameIndex=''
      for x in hostname:
         if str.isnumeric(x) is True:
            hostnameIndex+=x
      hostnameIndex=str(int(hostnameIndex)-2)

      a=open(serverLVAPath + "renderScript_0.bat",'r')
      b=a.read()
      c0=b.split(' -s ')[1]
      c0=c0.split(' -mem_usage ')[0]
      c0=c0.split(' -e ')
      frames=[]
      frames.append(int(c0[0]))
      frames.append(int(c0[1]))

      c0=b.split(' -output ')[1]
      renderDirectorie=c0.split('render[######].png" ')[0]
      
      state=True
      while state is True:
         if os.path.exists(serverLVAPath+"renderDone.txt") is True:
            
            
            
            a=open(serverLVAPath+"renderFolderFrames.bat",'w')
            swap0 = renderDirectorie.replace("RENDER",'')
##            print (swap0)
##            print (swap0[2:index-2]+'renderedFrames.tar')
            a.write("cd "+swap0+'\n')
            a.write('python -m tarfile -c renderedFrames.tar RENDER')
            a.close()
            
            index=len(swap0)
            
##            print(swap0)
            subprocess.call([serverLVAPath+"renderFolderFrames.bat"],shell=False)  
            shutil.copyfile(swap0[1:index-1]+'renderedFrames.tar',serverLVAPath+"renderedFrames_"+hostnameIndex+'.tar')
  
            

            a=open(serverLVAPath+'serverFrames.bat','w')
            a.write('python "'+serverNetworkPath+'send_frames_client.py"')
            a.close()
            subprocess.call([serverLVAPath+'serverFrames.bat'],shell=False)  
            
            state=False





            
      
   elif b == b'deleteproject':
      print ("deleteproject")
      c.send(b'6')

      shutil.rmtree(serverLVAPath)
      os.mkdir(serverLVAPath)


   elif b == b'cleanworkspace':
      print ("cleanworkspace")
      c.send(b'6')

      swapPath = serverLVAPath.split('\\')
      swapPath0 = ''
      d=0
      while d<len(swapPath)-2:
         swapPath0+=swapPath[d]+'\\'
         d+=1
##      print (swapPath0)
      if os.path.exists(serverLVAPath+"projectFolder.tar") is True:
         shutil.copyfile(serverLVAPath+"projectFolder.tar",swapPath0+"projectFolder.tar")

     
      
         shutil.rmtree(serverLVAPath)
       
         os.mkdir(serverLVAPath)
         
         index=len(serverLVAPath)
         a=open(serverLVAPath+'projectFolder.bat','w')
         a.write('python -m tarfile -v -e "'+swapPath0+'projectFolder.tar" "'+ serverLVAPath[:index-1]+'"')
         a.close()
         subprocess.call([serverLVAPath+"projectFolder.bat"],shell=False)
         shutil.copyfile(swapPath0+"projectFolder.tar",serverLVAPath+"projectFolder.tar")
         os.remove(swapPath0+"projectFolder.tar")



   elif b == b'restart':
      print ("restart")
      c.send(b'7')
      a=open(serverLVAPath+"restartServers.bat",'w')
      a.write("shutdown /r /t 00 /f")
      a.close()
      subprocess.call([serverLVAPath+"restartServers.bat"],shell=False)
      break

      
      


      
   elif b == b'shutdown':
      print ("shutdown")
      c.send(b'7')
      a=open(serverLVAPath+"shutdownServers.bat",'w')
      a.write("shutdown /s /t 00 /f")
      a.close()
      subprocess.call([serverLVAPath+"shutdownServers.bat"],shell=False)
      break


   
   elif b == b'resetconnection':
      print ("resetconnection")
      c.send(b'8')     
               
      a=open(serverLVAPath+'resetconection.bat','w')
      a.write('python "'+serverNetworkPath+'server.py"')
      a.close()
      subprocess.Popen([serverLVAPath+'resetconection.bat'],shell=False)
      exit()
      break
        

c.close()               





