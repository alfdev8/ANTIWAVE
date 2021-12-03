import pathlib
import subprocess
import time
import os


actualPath=str(pathlib.Path(__file__).parent.absolute())+"\\"


homeDrive=os.environ["HOMEDRIVE"]
pathAntiwave=homeDrive+"\\ANTIWAVE1.0\\"
pathResources=pathAntiwave+"Resources\\"
pathLVA = pathAntiwave+"LVA\\"



pathLVAserver = pathAntiwave+"server\\LVA\\"                            



binPath = pathResources+"bin\\"                                         
TempPath = pathResources+"Temp\\"                                       
NetworkPath = pathResources+"antiwave_network\\"                         
InstallPath = pathResources+"antiwave_install\\"                        







def sortComputers():
    file=open(actualPath+"weigthData.txt",'r')
    a=file.read().split("\n")
    file.close()
    a.pop()

    b=[]

    for x in a:
        b.append(x.split('*'))
        
    for x in b:
        x.pop()        

    d=[]
    d=sorted(b,key=lambda x: (x[0]))


    return d


def normalizeWeights(weights):    
    
    counter=0
    w=[]
    paddingZeros=[]

    while counter < len(weights):
        w.append(weights[counter][0])
        counter+=1

 
    nw=[]
    counter=0


#1,2
    if int(w[counter+1]) - int(w[counter]) == 2 or int(w[counter+1]) - int(w[counter]) == 1:
        nw.append(1)
        nw.append(nw[0]+1)
    elif int(w[counter+1]) - int(w[counter]) == 3 or int(w[counter+1]) - int(w[counter]) == 4:
        nw.append(1)
        nw.append(nw[0]+2)
    elif int(w[counter+1]) - int(w[counter]) == 5 or int(w[counter+1]) - int(w[counter]) > 5:
        nw.append(1)
        nw.append(nw[0]+nw[0])
    elif int(w[counter+1]) - int(w[counter]) == 0:
        nw.append(1)
        nw.append(nw[0])

#3
    counter=2
    while counter < len(w):
        if int(w[counter]) - int(w[counter-1])==2 or int(w[counter]) - int(w[counter-1])==1:
            nw.append(nw[counter-1]+1)
        elif int(w[counter]) - int(w[counter-1])==3 or int(w[counter]) - int(w[counter-1])==4:
            nw.append(nw[counter-1]+2)
        elif int(w[counter]) - int(w[counter-1])==5 or int(w[counter]) - int(w[counter-1]) > 5:
            nw.append(nw[counter-1] + nw[counter-1])
        elif int(w[counter]) - int(w[counter-1]) == 0:
            nw.append(nw[counter-1])        
        counter+=1
    
    return nw


def distributeRegions(weights,size):
    resolutionX=size[0]
    resolutionY=size[1]    

    w=weights

    wt=''
    wtotal=[]
    

    wt2=0
    for x in w:
        wt2+=x


    counter=0
    while True:
        resolutionX-=wt2
        counter+=1
        if resolutionX < 0:
            break

    wt3=[]
    for x in w:
        wt3.append(x*counter)

   
    wt4=0
    for x in wt3:
        wt4+=x

    resolutionX=size[0]
    dif=wt4-resolutionX


    c=len(wt3)-1
    while dif!=0:
        dif-=1
        wt3[c]-=1
        c+=1 
        if c >= len(wt3):
            c=len(wt3)-1

    return wt3



def getDividerSubregions(data,regionsX):

    cpuCores=[]
    c=0
    while c < len(data):
        cpuCores.append(int(data[c][1]))
        c+=1

    regX=regionsX

    dividers=[]
    divideRounded=[]
    c=0
    while c <len(cpuCores):
        dividers.append(regX[c]/cpuCores[c])
        c+=1
    c=0

    SubRegionSwap=[]
    while c<len(regX):
        SubRegion=[]
        checkDecimal=str(dividers[c]).split('.')
        if checkDecimal[1]!=0 :

            d=0
            while d<cpuCores[c]:
                SubRegion.append(int(checkDecimal[0]))
                d+=1                
        elif checkDecimal[1]==0:

            d=0
            while d<cpuCores[c]:
                SubRegion.append(int(checkDecimal[0]))                
                d+=1                
        SubRegionSwap.append(SubRegion)
        c+=1

    sum1=0
    sum2=[]
    d=0
    while d< len(SubRegionSwap):
        c=0
        sum1=0

        while c <len(SubRegionSwap[d]):
            sum1+=SubRegionSwap[d][c]
            c+=1
        sum2.append(sum1)
        d+=1

    dif1=[]
    c=0
    for x in regionsX:
        dif0=0
        dif0=regionsX[c]-sum2[c]
        dif1.append(dif0)
        c+=1

    d=0
    while d<len(SubRegionSwap):
        c=0
        while c<len(SubRegionSwap[d]):

            if dif1[d]==0:
                break
            SubRegionSwap[d][c]+=1
            dif1[d]-=1
            
            c+=1
        d+=1



        
    return SubRegionSwap   


def distributeFrames(frames,nw):
    
    sumNW=sum(nw)
    nwSwap=nw
    print (nw)
    print (sumNW)
    print(sum(frames))

    maxValue=nw[int(len(nwSwap)/2)]

    dif=0
    indexes=[]
    values=[]
    nwSwap=nw
    nwSwap2=[]



    if sumNW == len(nw):
        print ("All are equal")

        dividedFrames=int(sum(frames)/len(nw))

        swapNW=nw

        c=0
        while c < len(swapNW):
            swapNW[c]=dividedFrames
            c+=1

        

        dif = sum(frames) - sum(swapNW)


        
        c=0
        while True:
            if c>len(swapNW):
                c=0
            if dif==0:
                break                
            dif-=1
            swapNW[c]+=1
            c+=1
        


        return swapNW    
        
    elif len(nw) == 0  or len(nw) == 2 or len(nw) == 1:
        print ("error")






    
    elif sumNW > sum(frames):                                                


        swapFrames = sum(frames)+sumNW
        dif = swapFrames - sumNW 
        



        distributedDif=int(dif/maxValue)


        c=0
        while c< int(len(nwSwap)/2): 
            if nwSwap[c] <= maxValue: 
                indexes.append(nw.index(nwSwap[c]))
                values.append(nwSwap[c])
            elif nwSwap[c] > maxValue:
                break
            c+=1
        
        c=0
        while c<len(values):
            nwSwap.remove(values[c])
            c+=1

        
        exactDivisor=distributedDif*maxValue
        d=0
        while d<maxValue:
            c=0
            while c<len(nwSwap):

                nwSwap[c]+=1
                c+=1
                break
            d+=1
        
        notExact=sum(nwSwap)+sum(values)

        a=0
        if notExact<swapFrames:
            a=swapFrames-notExact
        elif notExact>swapFrames:
            a=notExact-swapFrames

        if a!=0:

            d=0
            while d!=int(a/len(nwSwap)):
                
                c=0
                while c< len(nwSwap):
                    nwSwap[c]+=1
                    c+=1
                d+=1
        elif a ==0:
            print("Does not exceed")

        amountOfBalance=len(values)
        c=0
        balancing=[]
        while c < len(nwSwap):
            balancing.append(int(nwSwap[c]/amountOfBalance))
            c+=1

        c=0
        while c<len(balancing):
            nwSwap[c]-=balancing[c]
            c+=1

        
        distributeLarger=int(sum(balancing)/amountOfBalance)


        c=0
        while c < len(values):
            values[c]+=distributeLarger
            c+=1   
        for x in values:
            nwSwap2.append(x)
        for x in nwSwap:
            nwSwap2.append(x)


        unbalancedTotal=0
        for x in nwSwap2:
            unbalancedTotal+=x

        if unbalancedTotal != swapFrames:
            dif = swapFrames-unbalancedTotal
            nwSwap2[len(nwSwap2)-1]+=dif

        return nwSwap2





       
    elif sumNW<sum(frames):
 
        dif= sum(frames)-sumNW

        distributedDif=int(dif/maxValue)

        c=0
        while c< int(len(nwSwap)/2):
            if nwSwap[c] <= maxValue: 
                indexes.append(nw.index(nwSwap[c]))
                values.append(nwSwap[c])
            elif nwSwap[c] > maxValue:
                break
            c+=1
        
        c=0
        while c<len(values):
            nwSwap.remove(values[c])
            c+=1

 
        exactDivisor=distributedDif*maxValue

        d=0
        while d<maxValue:
            c=0
            while c<len(nwSwap):

                nwSwap[c]+=1
                c+=1
                break
            d+=1
        
        notExact=sum(nwSwap)+sum(values)

        a=0
        if notExact<sum(frames):
            a=sum(frames)-notExact
        elif notExact>sum(frames):
            a=notExact-sum(frames)

        if a!=0:

            d=0
            while d!=int(a/len(nwSwap)):
                
                c=0
                while c< len(nwSwap):
                    nwSwap[c]+=1
                    c+=1
                d+=1
        elif a ==0:
            print("Doesn't Exceed")
  
        amountOfBalance=len(values)
        c=0
        balancing=[]
        while c < len(nwSwap):
            balancing.append(int(nwSwap[c]/amountOfBalance))
            c+=1

        c=0
        while c<len(balancing):
            nwSwap[c]-=balancing[c]
            c+=1

        
        distributeLarger=int(sum(balancing)/amountOfBalance)


        c=0
        while c < len(values):
            values[c]+=distributeLarger
            c+=1


        
        for x in values:
            nwSwap2.append(x)
        for x in nwSwap:
            nwSwap2.append(x)

        unbalancedTotal=0
        for x in nwSwap2:
            unbalancedTotal+=x
        if unbalancedTotal != sum(frames):
            dif = sum(frames)-unbalancedTotal
            nwSwap2[len(nwSwap2)-1]+=dif

            

        return nwSwap2


def convertUnitsToFramesPositives(frameUnits,realFrames):

    framesStartEnd=[]

    framesStartEnd.append(1)                
    framesStartEnd.append(frameUnits[0])
    

    c=1
    while c<len(frameUnits):
        framesStartEnd.append(framesStartEnd[len(framesStartEnd)-1]+1)
        framesStartEnd.append(framesStartEnd[len(framesStartEnd)-1]+frameUnits[c])
        c+=1


##    print("verificar si  se pasa o no se pasa")    
    if framesStartEnd[len(framesStartEnd)-1] < sum(frameUnits):
##        print ("no se pasa le falta")
        dif= sum(frameUnits) + framesStartEnd[len(framesStartEnd)-1]
        framesStartEnd[len(framesStartEnd)-1]+=dif
        
    elif framesStartEnd[len(framesStartEnd)-1] > sum(frameUnits):
##        print ("se pasa hay que quitarle")
        dif= framesStartEnd[len(framesStartEnd)-1]- sum(frameUnits)
        framesStartEnd[len(framesStartEnd)-1]-=dif
        
    elif framesStartEnd[len(framesStartEnd)-1] == sum(frameUnits):
        print ("Is exact")
        



    framesSwap=[]
    frames=[]
    
  
    c=1
    while c < len(framesStartEnd):
        framesSwap.append(framesStartEnd[c-1])
        framesSwap.append(framesStartEnd[c])
        frames.append(framesSwap)
        framesSwap=[]
        c+=2


    validation=[]
    for x in frames:
        validation.append((x[1]-x[0])+1)







    if realFrames[0] == 1 and realFrames[1] > 0:  
        dif = realFrames[1]-realFrames[0]

    
        frames[0][0] = realFrames[1]-dif
        frames[0][1] +=realFrames[1]-dif

        c=1
        while c < len(frames):
            frames[c][0]+=realFrames[0]
            frames[c][1]+=realFrames[0]
            c+=1


        frames[len(frames)-1][1]-=2
        

        return frames

        
    elif realFrames[0] == 0 and realFrames[1] > 0: 
        frames[0][0] = realFrames[0]
        frames[0][1] +=realFrames[0]

        c=1
        while c < len(frames):
            frames[c][0]+=realFrames[0]
            frames[c][1]+=realFrames[0]
            c+=1

        frames[len(frames)-1][1]=realFrames[1]


        return frames
        





def convertUnitsToFramesNegStartPosEnd(frameUnits,realFrames):



    framesStartEnd=[]

 
    framesStartEnd.append(1)                
    framesStartEnd.append(frameUnits[0])
    

    c=1
    while c<len(frameUnits):
        framesStartEnd.append(framesStartEnd[len(framesStartEnd)-1]+1)
        framesStartEnd.append(framesStartEnd[len(framesStartEnd)-1]+frameUnits[c])
        c+=1


 
    if framesStartEnd[len(framesStartEnd)-1] < sum(frameUnits):

        dif= sum(frameUnits) + framesStartEnd[len(framesStartEnd)-1]
        framesStartEnd[len(framesStartEnd)-1]+=dif
        
    elif framesStartEnd[len(framesStartEnd)-1] > sum(frameUnits):

        dif= framesStartEnd[len(framesStartEnd)-1]- sum(frameUnits)
        framesStartEnd[len(framesStartEnd)-1]-=dif
        
    elif framesStartEnd[len(framesStartEnd)-1] == sum(frameUnits):
        print ("Is exact")
 

    framesSwap=[]
    frames=[]
    

    c=1
    while c < len(framesStartEnd):
        framesSwap.append(framesStartEnd[c-1])
        framesSwap.append(framesStartEnd[c])
        frames.append(framesSwap)
        framesSwap=[]
        c+=2


    validation=[]
    for x in frames:
        validation.append((x[1]-x[0])+1)






    
    negativeValue = - (realFrames[0]+1)
    negativeValue2 = - (realFrames[1]+1)


    
    if negativeValue < 0 and realFrames[1] >0 : 

        frames[0][0] = -(realFrames[0]-1)

        frames[0][1] -= (realFrames[0]+1)


        c=1
        while c < len(frames):
            frames[c][0]+=negativeValue+1
            
            frames[c][1]-= realFrames[0]
            c+=1

        return frames
        




def convertUnitsToFramesNegStartNegEnd(frameUnits,realFrames):

    frames=[]
    
    totalFrames = realFrames[1] - realFrames[0]

    divided = int(totalFrames/len(frameUnits))

    
    swap=[]
    c=1
    swap.append(0)
    swap.append(divided)
    frames.append(swap)
    swap=[]
    while c<(len(frameUnits)*2)-2:
        swap.append(divided*c+1)
        swap.append(0)
        frames.append(swap)
        swap=[]
        if len(frames)-1>=len(frameUnits)-1:
            break
        c+=1


    c=1
    while c< len(frames):
       frames[c][1] =  frames[c][0] + divided
       c+=1


    c=0
    while c< len(frames):
       frames[c][0] += realFrames[0] +1 
       frames[c][1] += realFrames[0]
       c+=1


    frames[len(frames)-1][1] = realFrames[1]
    frames[0][0]=realFrames[0]
    frames[0][1] += 1


    c=0
    while c< len(frames):
        frames[c][0] = -frames[c][0]
        frames[c][1] = -frames[c][1]
        c+=1


    return frames
 

def convertUnitsToPixels(SubRegionX,renderer):    
    pixelMinPosition=0 
    pixelMinSize=0 
    offsetPixelBorder=0
    if renderer == 1:
##        print ("mentalray")
        pixelMinSize=1
        pixelMinPosition=0
        offsetPixelBorder=0
    elif renderer == 2:
##        print ("maya software")
        pixelMinSize=4
        pixelMinPosition=0
        offsetPixelBorder=0

    unifyGroups=[]
    for x in SubRegionX:
        for y in x:
            unifyGroups.append(y)

    duplicatedGroupsIndex=[]
    for x in SubRegionX:
        duplicatedGroupsIndex.append(len(x)*2)

    for x in unifyGroups:
        if x == pixelMinSize:
            
            print ("The render engine does not support this pixel meassure, reduce the # of cores of processing to adjust "+str(pixelMinSize)+"pixels")
            break
            

    pixelsStartEnd=[]

    pixelsStartEnd.append(pixelMinPosition)
    pixelsStartEnd.append(unifyGroups[0])


    
    c=1
    while c < len(unifyGroups):
        pixelsStartEnd.append(pixelsStartEnd[len(pixelsStartEnd)-1]+offsetPixelBorder)
        pixelsStartEnd.append(pixelsStartEnd[len(pixelsStartEnd)-1]+unifyGroups[c])        
        c+=1





    pixelsStartEnd[0]=pixelMinPosition


    
    if pixelsStartEnd[len(pixelsStartEnd)-1] < sum(unifyGroups):

        dif= sum(unifyGroups) + pixelsStartEnd[len(pixelsStartEnd)-1]
        pixelsStartEnd[len(pixelsStartEnd)-1]+=dif

        
    elif pixelsStartEnd[len(pixelsStartEnd)-1] > sum(unifyGroups):

        dif= pixelsStartEnd[len(pixelsStartEnd)-1]- sum(unifyGroups)
        pixelsStartEnd[len(pixelsStartEnd)-1]-=dif

        
    elif pixelsStartEnd[len(pixelsStartEnd)-1] == sum(unifyGroups):
        print ("Is exact")



    
    pixelRegions=[]



    
    maxIndexPosition=sum(duplicatedGroupsIndex)
    c=maxIndexPosition
    d=0
    while c > 0:
        pixelRegions.append(pixelsStartEnd[c-duplicatedGroupsIndex[len(duplicatedGroupsIndex)-(d+1)]:c])
        d+=1
        c-=duplicatedGroupsIndex[len(duplicatedGroupsIndex)-d]

    
    pixelRegionsOrganized=[]
    c=0
    while c < len(pixelRegions):
        pixelRegionsOrganized.append(pixelRegions[len(pixelRegions)-(c+1)])
        c+=1
        
    
    

    
            
   
    a=open(TempPath+"dataForCoordinates.txt",'r')
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

    coordinateY = []
    swap=[]
    c=0
    while c< len(pixelRegionsOrganized):
        d=0
        swap=[]
        while d < len(pixelRegionsOrganized[c])/2:
            
            swap.append(0)
            swap.append(InitialCoordinates[0][2])
            d+=1
        coordinateY.append(swap)
        c+=1


    coordinateXY=[]
    swap=[]
    c=0
    while c< len(pixelRegionsOrganized):
        d=0
        f=2
        swap=[]
        while d < len(pixelRegionsOrganized[c])/2:
            a=pixelRegionsOrganized[c][f-2:f]
            b=coordinateY[c][f-2:f]
            swap.append(a+b) 
            f+=2 
            d+=1
        coordinateXY.append(swap)              
        c+=1




    return coordinateXY


def getRenderCoordinates():
    a=open(TempPath+"dataForCoordinates.txt",'r')
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
    


def setRenderCoordinates(rendermode,coordinates,renderType):
    
    a=sortComputers()
    
    b=normalizeWeights(a)

    frameAB=[int(coordinates[0][3].split('.')[0]),int(coordinates[0][4].split('.')[0])]
    
    resolution = [int(coordinates[0][1]),int(coordinates[0][2])]



    
    if rendermode == 1:
        print ("Tile Mode")
        c=distributeRegions(b,resolution)
        d=getDividerSubregions(a,c)
        e=convertUnitsToPixels(d,renderType)  
##        print (e)
        return e

        
    elif rendermode == 2:
        print ("Frames Mode")        

        if frameAB[0] < 0 and frameAB[1] > 0:
            frameAB[0] = abs(frameAB[0])+1

            e=distributeFrames(frameAB,b)

            f=convertUnitsToFramesNegStartPosEnd(e,frameAB)

            return f
        elif frameAB[0] < 0 and frameAB[1] < 0:

            frameAB[0] = abs(frameAB[0])
            frameAB[1] = abs(frameAB[1])
            
            e=distributeFrames(frameAB,b)
            
            f=convertUnitsToFramesNegStartNegEnd(e,frameAB)
            return f

        elif frameAB[0] == 0 or frameAB[0] == 1 and frameAB[1] > 0:

             e=distributeFrames(frameAB,b)
             f=convertUnitsToFramesPositives(e,frameAB)
             return f
        
    elif rendermode == 3:
        print ("Dynamic Tiled Frames Mode") #versions



def loadSyntax(syntaxType,syntaxVersion,renderMode,renderType,frames,tiles=0):

        
    if syntaxType == "maya" and syntaxVersion =='10' and renderType==1 and renderMode == 1:

        a=open(pathResources + "maya10Syntax.txt",'r')
        b=a.read().split("***MayaSoftware")[0]

        a.close()
        b=b.split('\n')

        b.pop(-1)
        b.pop(0)

        c=getEnviromentVariable.getMayaPath()  

        b[0]='"'+c
        


        a=open(TempPath+"LoadFile.txt",'r')
        
        c=a.read()
        

        
        fileNameIndex = b.index("[file]")

        a.close()        

        


        
        b[1]=b[1].replace(' ','" ')
        b[0]+= b[1]+'"' 
        b.pop(1)

        
        LVApath = b.index("[LVA]")
        a=open(TempPath+"projectFolder.txt",'r')
        fileName=c
        c=a.read()
        
        

        
        d=c.split(':\\')[1] 
        

        a.close()
        stringSwap="-proj "
        b[LVApath] ='"'+pathLVAserver+d+'"' 




        d2=d.split("\\")
        

        fileNameSwap = fileName.split(d2[len(d2)-2])[1]
        
        swap = fileNameSwap.split('\\')
        swap.pop(0)


        

        c=0
        while c< len(swap)-1:
            swap[c]+='\\'
            c+=1

        swap0=''
        for x in swap:
            swap0+=x
            
            
        b[fileNameIndex]='"'+pathLVAserver+d+swap0+'" '+stringSwap 
        b.remove("[file]")

##        print(b)
        
        renderFolderLVApath = b.index("[LVA/rendertoclient]")
         
        b[renderFolderLVApath]='"'+pathLVAserver+'renderToClient\\'+'"'
        
        a=sortComputers()

        startFrame = b.index("[start]")
        b[startFrame] = str(frames[0][0])


        cores=[]
        for x in a:
            cores.append(int(x[1]))


        RAM=[]
        for x in a:
            RAM.append(int(x[2]))
            
        endFrame = b.index("[end]")
        b[endFrame] = str(frames[len(frames)-1][1])

        renderThreads = b.index("[cores]")
        RAMindex = b.index("[free ram]")


        swap=''
        swap0=b
        swap1=[]

        d=0
        while d < len(a):  
            swap0[renderThreads]=1
            swap0[RAMindex] = int(int(RAM[d]) / int(cores[d]))
            swap+=str(swap0)+'*'

            
            d+=1

        swap=swap.split('*')

        
        for x in swap:
            swap1.append(x.split(','))

        swap1.pop()
        
        d=0
        while d< len(swap1):
            c=0
            while c< len(swap1[d]):
                swap1[d][c]=swap1[d][c].replace('\\\\','\\')
                swap1[d][c]=swap1[d][c].replace(" '",'')
                swap1[d][c]=swap1[d][c].replace("'",'')

                c+=1            
            d+=1



        c=0
        while c < len (swap1):
            swap1[c].pop()
            c+=1



        swap=[]
        c=0
        while c < len(swap1):
            d=0
            while d< cores[c]:
                swap.append(str(swap1[c]))
                d+=1
            c+=1
            
        
        swap2=[]
        c=0
        while c < len(tiles):
            d=0
            while d< len(tiles[c]):
                swap2.append(str(tiles[c][d]))
                d+=1
            c+=1


        c=0
        while c < sum(cores):                
            swap[c]+= ' '+str(swap2[c])
            c+=1
        
        swap3=''
        swap4=[]
        for x in swap:
            swap3=''
            for y in x:
                if y == '[':
                    continue
                elif y == ']':
                    continue
                elif y == "'":
                    continue
                elif y == ",":
                    continue                    
                else:
                    swap3+=y
            swap4.append(swap3)


        for x in swap4:
            print (x)


##            
    elif syntaxType == "maya" and syntaxVersion =='10' and renderType == 1 and renderMode == 2:
        print ("mentalray frame mode ")
             
        a=open(pathResources + "maya10Syntax.txt",'r')
        b=a.read().split("***MayaSoftware")[0]

        a.close()
        b=b.split('\n')

        b.pop(-1)
        b.pop(0)

        c=getEnviromentVariable.getMayaPath()  

        b[0]='"'+c
        

        a=open(TempPath+"LoadFile.txt",'r')
        fileName = b.index("[file]")

        b[fileName]='"'+pathLVAserver+a.read().split(":\\")[1]+'"' 
        a.close()        

        
        b[1]=b[1].replace(' ','" ')
        b[0]+= b[1]+'"' 
        b.pop(1)


        LVApath = b.index("[LVA]")
        a=open(TempPath+"projectFolder.txt",'r')
        c=a.read()

        d=c.split(':\\')[1] 
        

        a.close()
        b[LVApath] ='"'+pathLVAserver + d +'"' 






        


        


        renderFolderLVApath = b.index("[LVA/rendertoclient]")
                 
        b[renderFolderLVApath]='"'+pathLVAserver+'renderToClient\\"' 

        
        
        a=sortComputers()






        cores=[]
        for x in a:
##            print (x[1]) 
            cores.append(x[1])   


        RAM=[]
        for x in a:

            RAM.append(x[2])       

        startFrame = b.index("[start]")
        endFrame = b.index("[end]")
        verboseMode = b.index("[5  0]")
        b[verboseMode] = "0 " 
        

        regIndex = b.index("-reg")
        b[regIndex]=''
        tilesIndex =  b.index("[tiles]")
        b[tilesIndex]=''


        swap=''
        swap0=b
        swap1=[]










        d=0
        while d < len(a):
            
            swap1.append(swap0[0:8])

    

            
            d+=1



        startEndFrame=[]
        swap2=[]
        c=0
        while c< len (a):
            swap+= " -s " + str(frames[c][0])+" -e "+str(frames[c][1]) + " -v " + swap0[verboseMode] 
            swap2.append(swap)
            swap=''
            c+=1

        swap6=[]
        c=0
        while c< len(swap2):
            swap6.append("-rt "+str(cores[c]) + " -mem "+str(RAM[c]))
            
            c+=1
        
        


        swap3=[]
        c=0
        while c< len(a):
            swap3.append(str(swap1[c])+swap2[c])
            
            c+=1



        swap7=[]
        c=0
        while c < len(swap3):
            swap7.append(swap3[c]+swap6[c])
            c+=1



        swap5=''
        swap4=[]
        for x in swap7:
            swap5=''
            for y in x:
                if y == '[':
                    continue
                elif y == ']':
                    continue
                elif y == "'":
                    continue
                elif y == ",":
                    continue                    
                else:
                    swap5+=y
            swap4.append(swap5)



##        for x in swap4:
##           print (x)
        





           
    elif syntaxType == "maya" and syntaxVersion =='10' and renderType == 2 and renderMode == 1:
        print ("Maya Software tile mode ")
        a=open(pathResources + "maya10Syntax.txt",'r')
        b=a.read().split("***MayaSoftware")[1]
        a.close()
        b=b.split('\n')
        c=getEnviromentVariable.getMayaPath()  
        b[0]='"'+c

        a=open(TempPath+"LoadFile.txt",'r')
        c=a.read()

        
        
        fileNameIndex = b.index("[file]")

        a.close()        

        b[1]=b[1].replace(' ','" ')
        b[0]+= b[1]+'"'
        b.pop(1)





        LVApath = b.index("[LVA]")
        a=open(TempPath+"projectFolder.txt",'r')
        fileName=c
        c=a.read()
        d=c.split(':\\')[1] 
        a.close()
        stringSwap="-proj"
        b[LVApath] ='"'+pathLVAserver+d+'"' 


        d2=d.split("\\")
        
        fileNameSwap = fileName.split(d2[len(d2)-2])[1]

        swap = fileNameSwap.split('\\')
        swap.pop(0)

        c=0
        while c< len(swap)-1:
            swap[c]+='\\'
            c+=1

        swap0=''
        for x in swap:
            swap0+=x
            



        b[fileNameIndex]='"'+pathLVAserver+d+swap0+'" '+stringSwap 
        b.remove("[file]")




        renderFolderLVApath = b.index("[LVA/rendertoclient]")

         
        b[renderFolderLVApath]='"'+pathLVAserver+'renderToClient\\"'
        
        a=sortComputers()

        startFrame = b.index("[start]")
        b[startFrame] = str(frames[0][0])

        



        cores=[]
        for x in a:

            cores.append(int(x[1]))


        RAM=[]
        for x in a:
            RAM.append(int(x[2]))
            
        endFrame = b.index("[end]")
        b[endFrame] = str(frames[len(frames)-1][1])



        renderThreads = b.index("[cores]")
        RAMindex = b.index("[free ram]")


        swap=''
        swap0=b
        swap1=[]

        d=0
        

        while d < len(a):
            c=0
            while c< cores[d]:
                swap0[renderThreads]=1  
                swap0[RAMindex] = int(int(RAM[d]) / int(cores[d]))
                swap+=str(swap0)+'*'

                c+=1
          
            
            d+=1


        swap=swap.split('*')



        
        
        for x in swap:
            swap1.append(x.split(','))

        swap1.pop()




        
        d=0
        while d< len(swap1):
            c=0
            while c< len(swap1[d]):

                swap1[d][c]=swap1[d][c].replace('\\\\','\\')

                swap1[d][c]=swap1[d][c].replace("'",'')

                c+=1            
            d+=1











        tilesSwap=[]

        c=0
        while c< len(tiles):
            d=0
            while d< len(tiles[c]):
                tilesSwap.append(tiles[c][d])
                d+=1
            c+=1





        

        c=0
        while c < len(swap1):
            index=swap1[c].index(" [tiles]")
            swap1[c][index] = str(tilesSwap[c]).replace('[','')
            swap1[c][index] = swap1[c][index].replace(']','')
            swap1[c][index] = swap1[c][index].replace("'",'')

            swap1[c][index] = swap1[c][index].replace(",",'')
            c+=1




        swap2=[]
        c=0
        while c <  len(swap1):
            swap2.append(str(swap1[c]).replace('[',''))
            swap2[len(swap2)-1][c].replace(']','')
            swap2[len(swap2)-1][c].replace("',",'')
            swap2[len(swap2)-1][c].replace("'",'')
        
            
            c+=1



        swap4=[]
        swap3=''
        for x in swap2:
            swap3=''
            for y in x:
                if y == ']':
                    continue
                if y == '[':
                    continue
                if y == ',':
                    continue
                if y == "'":
                    continue

                    continue
                else:
                    swap3+=y
            swap4.append(swap3)


        swap5=[]
        c=0
        
        while c<len(swap4):
            swap5.append(str(swap4[c].replace(']','')))
            swap5[len(swap5)-1].replace('[','')
            swap5[len(swap5)-1].replace(',','')

            c+=1
            

        swap6=[]
        for x in swap5:
        
            swap6.append(x.split("  "))


        c=0
        while c < len(swap6):
            d=0
            while d < len(swap6[c]):
                swap6[c][d]+=' '
                d+=1
            c+=1


        

        swap7=[]
##        c=0
##        while c < len(swap6):
##            print (swap6[c])
##            c+=1

        c=0
        while c < len(swap6):
            swap7.append(str(swap6[c]).replace(',',''))
            swap7[len(swap7)-1]=swap7[len(swap7)-1].replace('\\\\','\\')
            swap7[len(swap7)-1]=swap7[len(swap7)-1].replace("' '",'')
            
            c+=1

##        for x in swap7:
##            print (x)




        
    elif syntaxType == "maya" and syntaxVersion =='10' and renderType == 2 and renderMode == 2:
        print("Loading")
        print ("Maya Software frame mode ")
        a=open(pathResources + "maya10Syntax.txt",'r')
        b=a.read().split("***MayaSoftware")[1]

        a.close()
        b=b.split('\n')

        c=getEnviromentVariable.getMayaPath()  

        b[0]='"'+c
        

        
        a=open(TempPath+"LoadFile.txt",'r')
        fileName = b.index("[file]")

        b[fileName]='"'+pathLVAserver+a.read().split(":\\")[1]+'"' 
        a.close()        


        b[1]=b[1].replace(' ','" ')
        b[0]+= b[1] + '"'
        b.pop(1)


        



        renderFolderLVApath = b.index("[LVA/rendertoclient]")
          
        b[renderFolderLVApath]='"'+pathLVAserver+'renderToClient\\"'  


        LVApath = b.index("[LVA]")        

        a=open(TempPath+"projectFolder.txt",'r')
        c=a.read()

        d=c.split(':\\')[1] 
        
##        print (c)
        a.close()
        b[LVApath] ='"'+pathLVAserver + d +'"' 
       
        a=sortComputers()

        cores=[]
        for x in a:
##            print (x[1]) 
            cores.append(x[1])   


        RAM=[]
        for x in a:

            RAM.append(x[2])
      
        

        b.remove("-reg")
        b.remove("[tiles]")
        
        renderThreads = b.index("[cores]")
        RAMindex = b.index("[free ram]")

        swap=''
        swap0=b
        swap1=[]


        d=0
        while d < len(a):
            
            swap1.append(swap0[0:9])

        

            
            d+=1

        startEndFrame=[]
        swap2=[]
        c=0
        while c< len (a):
            swap+= " -s " + str(frames[c][0])+" -e "+str(frames[c][1]) +" -mm "+RAM[c] + " -n "+str(cores[c]) 
            swap2.append(swap)
            swap=''
            c+=1

        swap3=[]
        c=0
        while c< len(a):
            swap3.append(str(swap1[c])+swap2[c])
            
            c+=1

        swap5=''
        swap4=[]
        for x in swap3:
            swap5=''
            for y in x:
                if y == '[':
                    continue
                elif y == ']':
                    continue
                elif y == "'":
                    continue
                elif y == ",":
                    continue
                elif y == "' ":
                    continue    
                else:
                    swap5+=y
            swap4.append(swap5)



##        for x in swap4:
##            print (x)


        
    elif syntaxType == "ae" and syntaxVersion == 'cs6' and rendermode==2 :
        print("")
