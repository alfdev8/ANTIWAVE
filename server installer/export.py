import shutil
import pathlib
import os


homeDrive=os.environ["HOMEDRIVE"]
pathAntiwave=homeDrive+"\\ANTIWAVE1.0\\"
pathAntiwaveInstall=pathAntiwave+"Resources\\antiwave_install\\"


actualPath=str(pathlib.Path(__file__).parent.absolute())

shutil.copyfile(actualPath+"\\server\\ServerResources\\antiwave_network\\config\\weigthData.txt",pathAntiwaveInstall+"weigthData.txt")

#cp "C:\ANTIWAVE1.0\server installer\server weigthData" Resources\antiwave_install
