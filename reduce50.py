import maya.cmds as cmds
import re
import pprint

orderedEdges = cmds.ls(orderedSelection=True, flatten=True)
def correctNameFace(facesList):
        """ removed range from bracket [x:y] and inserts value in range into new list"""
        temp_faceList = []
        for face in facesList:
                objName = face.split('.f')[0]
                if ":" in face:  
                    nPCompile = re.compile(r'(\d+)') 
                    numbers = nPCompile.findall(face)
                    x = len(numbers)
                    for i in range(int(numbers[x-2]), int(numbers[x-1])+1):
                        temp_faceList.append(objName + ".f[" +str(i) + ']') 
                        i += 1
                else:
                    temp_faceList.append(face)
        return temp_faceList    

def correctEdgeFace(facesList):
        """ removed range from bracket [x:y] and inserts value in range into new list"""
        temp_faceList = []
        for face in facesList:
                objName = face.split('.e')[0]
                if ":" in face:  
                    numbers = []
                    nPCompile = re.compile(r'(\d+)') 
                    numbers = nPCompile.findall(face)
                    x = len(numbers)
                    for i in range(int(numbers[x-2]), int(numbers[x-1])+1):
                        temp_faceList.append(objName + ".e[" +str(i) + ']') 
                        i += 1
                else:
                    temp_faceList.append(face)
        return temp_faceList         

def correctNameVertex(vertexList):
        """ removed range from bracket [x:y] and inserts value in range into new list"""
        temp_vertexList = []
        for vertex in vertexList:
                objName = vertex.split('.vtx')[0]
                # correct naming convention
                if ":" in vertex:  
                    nPCompile = re.compile(r'(\d+)') 
                    numbers = nPCompile.findall(vertex)
                    x = len(numbers)
                    for i in range(int(numbers[x-2]), int(numbers[x-1])+1):
                        temp_vertexList.append(objName + ".vtx[" +str(i) + ']') 
                        i += 1
                else:
                    temp_vertexList.append(vertex)
        return temp_vertexList        

def getNumber(item, type):
    """ args:   poly asset
                string of type of asset
        return: number inside brackets of object """
    
    match type:
        case "edge":
            type = '.e'
        case "face":
            type = '.f'
    
    bracket = item.split(type)[1]
    nPattern = re.compile(r'(\d+)') 
    number = nPattern.findall(bracket)[0]
    return int(number)
def removeBrackets(set, type):
    type = getType(type)
    correctedNames = []
    for item in set:
        objName, bracket = item.split(type)
        if ":" in bracket:
            nPattern = re.compile(r'(\d+)') 
            numbers = nPattern.findall(bracket)
            for i in range(int(numbers[0]), int(numbers[1])+1):
                correctedNames.append(objName + type + "[" + str(i) + "]")
                i += 1
        else:
            correctedNames.append(item)

    return correctedNames

def getType(n):
    match n:
        case "edge":
            type = '.e'
        case "face":
            type = '.f'
        case "vertex":
            type = '.vtx'
    return type
#testEdge = orderedEdges[0]


def test(index, bo):
    bo = correctEdgeFace(bo)
    orderedEdges = cmds.polySelect( 'polySurface21', edgeRing= index, en = 2 , add = 1)
    originalSpan = len(orderedEdges)
    length = 0
    corners = []
    edgeDict = []
    good = []
    bad = []
    badEL = []
    askewE = []
    for each in orderedEdges:
        #edgeLoop = [each]
        if each not in borders:
            
            secondEdge =  cmds.polySelect( 'polySurface21', el= each, ass = 1, q = 1)
            
            g = 0
            gb = 0 
            secondEdge = correctEdgeFace(secondEdge)
            for edge in secondEdge:
                if edge in bo:
                    g += 1
                if edge in borders:
                    gb += 1
            if g == 2:
                good.extend(secondEdge)
                edgeDict.append(secondEdge)
                badEL.append([])
                length += 1
            else:
                if len(secondEdge) != 1:
                    if gb != 2:
                        bad.append(length)
                        badEL.append(secondEdge)
                        edgeDict.append([])
                        length += 1
                    else:
                        askewE.append(secondEdge)
    
    newGood = []
    allEdges = []
    
    for i in range(len(edgeDict)):
        if i not in bad:
            allEdges.extend(edgeDict[i])
    for edges in badEL:
        allEdges.extend(edges)

    for j in range(0, len(edgeDict), 1):
        if edgeDict[j] != []:
            firstDict = edgeDict[j]
            for k in range(len(edgeDict)-1, 0, -1):
                if len(edgeDict[k]) > 0:
                    secDict = edgeDict[k]
                    break
 
            # cmds.select(firstDict, secDict)
            if len(firstDict) > len(secDict):
                startDict = firstDict
                end = secDict
            else:
                startDict = secDict
                end = firstDict
            for i in range((len(startDict))):
                start = getNumber(startDict[i], "edge")
                newEdges = getEdges(start,end, originalSpan, bo)
                try:
                    newAddOns = list(set(newEdges) - set(allEdges))
                    if newAddOns != []:
                        newGood.extend(newAddOns)
                        allEdges.extend(newAddOns)
                        #cmds.select(newAddOns)
                        # print("newAddons ")

                except:
                    pass
        
    
    cmds.select(newGood)
    good.extend(newGood)
    # cmds.select(good, tgl = True)
    selected = cmds.ls(sl=True,long=True)
    return good, allEdges, askewE

def getEdges(start, end, origSpan,  bo):

    orderedEdges = cmds.polySelect( 'polySurface21', edgeRing= start, en = 2, q = 1)
    allGood = False
    newPath = len(orderedEdges)
    length = 0
    edgeDict = []
    good = []
    bad = []
    
    #origSpan = 27
    for each in orderedEdges:
        #edgeLoop = [each]
        if each not in borders:
            
            secondEdge =  cmds.polySelect( 'polySurface21', el= each, ass = 1, q = 1)
            g = 0
            gb = 0 
            secondEdge = correctEdgeFace(secondEdge)
            for edge in secondEdge:
                if edge in bo:
                    g += 1
                if edge in borders:
                    gb += 1
            if g == 2:
                if allGood or len(secondEdge) < origSpan :
                    good.extend(secondEdge)
                    edgeDict.append(secondEdge)
                    length += 1
            else:
                if len(secondEdge) != 1 and allGood:
                    #
                    
                    if gb != 2:
                        bad.append(length)
                        good.extend(secondEdge)
                        edgeDict.append(secondEdge)
                        length += 1
                    
    
    
    # if newPath < origSpan:
    #     allGood = True

    # if not allGood:
    #     print("denied")
    #     return
    
    #cmds.select(good, add = True)
    
    return good

def getAEdges(start, end,bo):

    orderedEdges = cmds.polySelect( 'polySurface21', edgeRing= start, en = 2, q = 1)
    allGood = False
    newPath = len(orderedEdges)
    length = 0
    edgeDict = []
    good = []
    bad = []
    
    #origSpan = 27
    for each in orderedEdges:
        #edgeLoop = [each]
        if each not in borders:
            
            secondEdge =  cmds.polySelect( 'polySurface21', el= each, ass = 1, q = 1)
            g = 0
            gb = 0 
            secondEdge = correctEdgeFace(secondEdge)
            for edge in secondEdge:
                if edge in bo:
                    g += 1
                if edge in borders:
                    gb += 1
            if g == 2:
                    good.extend(secondEdge)
                    edgeDict.append(secondEdge)
                    length += 1
            else:
                if len(secondEdge) != 1 and allGood:
                    #
                    
                    if gb == 2:
                        bad.append(length)
                        good.extend(secondEdge)
                        edgeDict.append(secondEdge)
                        length += 1

    for edge in end:
        if edge in good:
            allGood = True
            break                
    
    
    # if newPath < origSpan:
    #     allGood = True

    if not allGood:
        print("denied")
        return
    
    #cmds.select(good, add = True)
    
    return good

def checkAskew(correct, wonky):
    newCorrect = []
    
    for each in wonky:
        #cmds.select(each, add = True)
        for edge in each:
            newE = getAEdges(getNumber(edge, "edge"), correct,  borders)
            if newE != []:
                # newCorrect.extend(each)
                newEd = getAEdges(getNumber(edge, "edge"), correct, borders)
                try:
                    newCorrect.extend(newEd)
                except:
                    pass
                break
    

    return newCorrect



def fifty():
    # firstEdges = ['polySurface21.e[1]', 'polySurface21.e[3]', 'polySurface21.e[6]', 'polySurface21.e[9]', 'polySurface21.e[12]', 'polySurface21.e[14]', 'polySurface21.e[17]', 'polySurface21.e[19:22]', 'polySurface21.e[25]', 'polySurface21.e[28]', 'polySurface21.e[31]', 'polySurface21.e[34]', 'polySurface21.e[37]', 'polySurface21.e[40]', 'polySurface21.e[43]', 'polySurface21.e[46]', 'polySurface21.e[50]', 'polySurface21.e[53]', 'polySurface21.e[56]', 'polySurface21.e[58]', 'polySurface21.e[62]', 'polySurface21.e[65]', 'polySurface21.e[68]', 'polySurface21.e[71]', 'polySurface21.e[74]', 'polySurface21.e[76:79]', 'polySurface21.e[82]', 'polySurface21.e[85]', 'polySurface21.e[88]', 'polySurface21.e[91]', 'polySurface21.e[94]', 'polySurface21.e[124]', 'polySurface21.e[127:128]', 'polySurface21.e[216:217]', 'polySurface21.e[220:221]', 'polySurface21.e[224]', 'polySurface21.e[227]', 'polySurface21.e[230]', 'polySurface21.e[233]', 'polySurface21.e[236]', 'polySurface21.e[239]', 'polySurface21.e[242]', 'polySurface21.e[245]', 'polySurface21.e[248]', 'polySurface21.e[251]', 'polySurface21.e[254]', 'polySurface21.e[257]', 'polySurface21.e[260]', 'polySurface21.e[263]', 'polySurface21.e[268]', 'polySurface21.e[270]', 'polySurface21.e[273]', 'polySurface21.e[276]', 'polySurface21.e[279]', 'polySurface21.e[282]', 'polySurface21.e[285]', 'polySurface21.e[288]', 'polySurface21.e[291]', 'polySurface21.e[294]', 'polySurface21.e[297]', 'polySurface21.e[300]', 'polySurface21.e[303]', 'polySurface21.e[305]', 'polySurface21.e[308]']


    

    # secondEdges = ['polySurface21.e[0]', 'polySurface21.e[2]', 'polySurface21.e[19]', 'polySurface21.e[21:22]', 'polySurface21.e[25]', 'polySurface21.e[28]', 'polySurface21.e[31]', 'polySurface21.e[34]', 'polySurface21.e[37]', 'polySurface21.e[40]', 'polySurface21.e[43]', 'polySurface21.e[46]', 'polySurface21.e[50]', 'polySurface21.e[53]', 'polySurface21.e[56]', 'polySurface21.e[58]', 'polySurface21.e[62]', 'polySurface21.e[65]', 'polySurface21.e[68]', 'polySurface21.e[71]', 'polySurface21.e[74]', 'polySurface21.e[77]', 'polySurface21.e[95:96]', 'polySurface21.e[98]', 'polySurface21.e[101]', 'polySurface21.e[103]', 'polySurface21.e[106]', 'polySurface21.e[109]', 'polySurface21.e[112]', 'polySurface21.e[116]', 'polySurface21.e[119]', 'polySurface21.e[122]', 'polySurface21.e[124]', 'polySurface21.e[127:130]', 'polySurface21.e[132]', 'polySurface21.e[135]', 'polySurface21.e[138]', 'polySurface21.e[141]', 'polySurface21.e[144]', 'polySurface21.e[147]', 'polySurface21.e[150]', 'polySurface21.e[153]', 'polySurface21.e[156]', 'polySurface21.e[159]', 'polySurface21.e[162]', 'polySurface21.e[165]', 'polySurface21.e[168]', 'polySurface21.e[171]', 'polySurface21.e[174]', 'polySurface21.e[177]', 'polySurface21.e[180]', 'polySurface21.e[183]', 'polySurface21.e[186]', 'polySurface21.e[189]', 'polySurface21.e[192]', 'polySurface21.e[195]', 'polySurface21.e[198]', 'polySurface21.e[201]', 'polySurface21.e[204]', 'polySurface21.e[207]', 'polySurface21.e[210]', 'polySurface21.e[213]', 'polySurface21.e[215]', 'polySurface21.e[309:311]', 'polySurface21.e[314]', 'polySurface21.e[317]', 'polySurface21.e[320]', 'polySurface21.e[323]', 'polySurface21.e[326]', 'polySurface21.e[329]', 'polySurface21.e[332]', 'polySurface21.e[335]', 'polySurface21.e[338]', 'polySurface21.e[341]', 'polySurface21.e[344]', 'polySurface21.e[347]', 'polySurface21.e[350]', 'polySurface21.e[353]', 'polySurface21.e[356]', 'polySurface21.e[359]', 'polySurface21.e[362]', 'polySurface21.e[365]', 'polySurface21.e[368]', 'polySurface21.e[371]', 'polySurface21.e[375]', 'polySurface21.e[378]', 'polySurface21.e[381]', 'polySurface21.e[384]', 'polySurface21.e[387]', 'polySurface21.e[390]', 'polySurface21.e[393]', 'polySurface21.e[395]', 'polySurface21.e[397]', 'polySurface21.e[399]', 'polySurface21.e[402]', 'polySurface21.e[405]', 'polySurface21.e[408]', 'polySurface21.e[411]', 'polySurface21.e[416]', 'polySurface21.e[419]', 'polySurface21.e[421]', 'polySurface21.e[424]', 'polySurface21.e[427]', 'polySurface21.e[1844]', 'polySurface21.e[1905]']

    firstEdges = ['polySurface21.e[1]', 'polySurface21.e[3]', 'polySurface21.e[6]', 'polySurface21.e[9]', 'polySurface21.e[12:15]', 'polySurface21.e[30:34]', 'polySurface21.e[37]', 'polySurface21.e[40]', 'polySurface21.e[43]', 'polySurface21.e[46]', 'polySurface21.e[153:154]', 'polySurface21.e[157:158]', 'polySurface21.e[161]', 'polySurface21.e[164]', 'polySurface21.e[167]', 'polySurface21.e[170]', 'polySurface21.e[173]', 'polySurface21.e[176]', 'polySurface21.e[179]', 'polySurface21.e[182]', 'polySurface21.e[185]', 'polySurface21.e[188]', 'polySurface21.e[191]', 'polySurface21.e[195]', 'polySurface21.e[198]', 'polySurface21.e[201]', 'polySurface21.e[204]', 'polySurface21.e[207]', 'polySurface21.e[210]', 'polySurface21.e[213]', 'polySurface21.e[216]', 'polySurface21.e[219]', 'polySurface21.e[222]', 'polySurface21.e[224]', 'polySurface21.e[227]', 'polySurface21.e[354:355]', 'polySurface21.e[357:358]', 'polySurface21.e[360]', 'polySurface21.e[525]', 'polySurface21.e[1483:1484]', 'polySurface21.e[1619:1621]', 'polySurface21.e[1685:1686]']

    secondEdges = ['polySurface21.e[0]', 'polySurface21.e[2]', 'polySurface21.e[13]', 'polySurface21.e[15]', 'polySurface21.e[32:33]', 'polySurface21.e[47:48]', 'polySurface21.e[50]', 'polySurface21.e[53]', 'polySurface21.e[55]', 'polySurface21.e[58]', 'polySurface21.e[62]', 'polySurface21.e[65]', 'polySurface21.e[67]', 'polySurface21.e[70:73]', 'polySurface21.e[75]', 'polySurface21.e[78]', 'polySurface21.e[81]', 'polySurface21.e[84]', 'polySurface21.e[87]', 'polySurface21.e[90]', 'polySurface21.e[93]', 'polySurface21.e[96]', 'polySurface21.e[99]', 'polySurface21.e[102]', 'polySurface21.e[105]', 'polySurface21.e[108]', 'polySurface21.e[111]', 'polySurface21.e[114]', 'polySurface21.e[117]', 'polySurface21.e[120]', 'polySurface21.e[123]', 'polySurface21.e[126]', 'polySurface21.e[129]', 'polySurface21.e[132]', 'polySurface21.e[135]', 'polySurface21.e[138]', 'polySurface21.e[141]', 'polySurface21.e[144]', 'polySurface21.e[147]', 'polySurface21.e[150]', 'polySurface21.e[152]', 'polySurface21.e[228:230]', 'polySurface21.e[233]', 'polySurface21.e[236]', 'polySurface21.e[239]', 'polySurface21.e[242]', 'polySurface21.e[245]', 'polySurface21.e[248]', 'polySurface21.e[251]', 'polySurface21.e[254]', 'polySurface21.e[257]', 'polySurface21.e[260]', 'polySurface21.e[263]', 'polySurface21.e[266]', 'polySurface21.e[269]', 'polySurface21.e[272]', 'polySurface21.e[275]', 'polySurface21.e[278]', 'polySurface21.e[281]', 'polySurface21.e[284]', 'polySurface21.e[288]', 'polySurface21.e[291]', 'polySurface21.e[294]', 'polySurface21.e[297]', 'polySurface21.e[300]', 'polySurface21.e[303]', 'polySurface21.e[306]', 'polySurface21.e[308]', 'polySurface21.e[311]', 'polySurface21.e[314]', 'polySurface21.e[317]', 'polySurface21.e[320]', 'polySurface21.e[325]', 'polySurface21.e[327]', 'polySurface21.e[330]', 'polySurface21.e[354:355]', 'polySurface21.e[357:358]', 'polySurface21.e[360]', 'polySurface21.e[525]', 'polySurface21.e[1391]', 'polySurface21.e[1438]', 'polySurface21.e[1483:1484]', 'polySurface21.e[1619:1621]', 'polySurface21.e[1685:1686]']


    global borders 
    borders = []
    borders.extend(correctEdgeFace(firstEdges))
    borders.extend(correctEdgeFace(secondEdges))
    first = test(1519, firstEdges)
    second = test(1521, secondEdges)
    # second = getCornerEdges('polySurface21',1799)
    # third = getCornerEdges('polySurface21',1762)
    askewF = checkAskew(first[1], second[2])
    askewS = checkAskew(second[1], first[2])
    cmds.select(first[0])
    cmds.select(second[0], add = True)
    # cmds.select(askewF, add = True)
    # cmds.select(askewS, add = True)
    #cmds.polyDelEdge( cv = True, ch = 1)

fifty()
