import os
import pathlib
import subprocess
import shutil

homeDrive=os.environ["HOMEDRIVE"]
startUp=os.environ["ProgramData"] + "\\Microsoft\\Windows\\Start Menu\\Programs\\Startup\\"
pathAntiwave=homeDrive+"\\ANTIWAVE1.0\\"

##server path structure
serverLVAPath = pathAntiwave + "server\\LVA\\"
#serverTempPath = serverLVAPath + "Temp\\"
serverNetworkConfigPath = pathAntiwave + "server installer\\server\\ServerResources\\antiwave_network\\config\\"
serverNetworkPath = pathAntiwave + "server installer\\server\\ServerResources\\antiwave_network\\"

actualPath=str(pathlib.Path(__file__).parent.absolute())

print (serverNetworkPath)
import sys
sys.path.insert(1,actualPath+"\\server\\ServerResources\\antiwave_network\\config\\")
import serverNetworkSetup

def copyFiles():
    print(actualPath)
    if os.path.exists("c:\\ANTIWAVE1.0") is True:
        os.system("RMDIR /S /Q c:\\ANTIWAVE1.0")
        os.mkdir("c:\\ANTIWAVE1.0") #get if folder was already created
    elif os.path.exists("c:\\ANTIWAVE1.0") is False:
        os.mkdir("c:\\ANTIWAVE1.0")
    #('python -m tarfile -c "'+TempPath+'projectFolder.tar" "' + projectPath + '"')
    file = open(actualPath+"InstallWindows.bat",'w')
    file.write('python -m tarfile -c "C:\\install.tar" "' + actualPath + '"')
    file.close()
    subprocess.call([actualPath+"InstallWindows.bat"],shell=False)

##    file = open(actualPath+"InstallWindows.bat",'w')
##    file.write('python -m tarfile -c "C:\\install.tar" "' + actualPath + '"')
##    file.close()


    file = open(actualPath+"InstallWindows.bat",'w')
    file.write('python -m tarfile -v -e "C:\\install.tar" "C:\\ANTIWAVE1.0"\necho finish extraction>C:\\extraction.txt')
    file.close()
    subprocess.call([actualPath+"InstallWindows.bat"],shell=False)


    os.remove("C:\\install.tar")
    
def network():
    serverNetworkSetup.oldNetworkConfig()    
    b=serverNetworkSetup.setHostname()              #must be in this order
    a=serverNetworkSetup.changeIP()
    c=serverNetworkSetup.getThreadsSupported(0,0)
    array=[c[2],c[1],c[0],a,b]
    serverNetworkSetup.saveData(array)

def startup():
    a=open(serverNetworkPath+'server.bat','w')
    a.write('python "'+serverNetworkPath+'server.py"')
    a.close()
    shutil.copyfile(serverNetworkPath+"server.bat",startUp+"server.bat")
    
#def restart():#version 1 manually



input("Thank you for install ANTIWAVE 1.0 Distributed Network Rendering, please hit Enter key to continue.")
copyFiles()
network()
startup()
input("successfull installation, please restart this computer, hit Enter key to close this window")
exit()
