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

def test(index, borderEdges):
    everyOther = cmds.polySelect(objName, er = index, en = 2, q = True)
    usableEdges = []
    unusableEdges = []
    possibleEdges = []
    for edge in everyOther:
        edgeLoop = removeBrackets(cmds.polySelect(objName, el = edge, q = True, ass = 1), "edge")
        bordersFound = 0
        allBorderFound = 0
        for loop in edgeLoop:
            if loop in borderEdges:
                bordersFound += 1
            if loop in borders:
                allBorderFound += 1
        if 'polySurface21.e[453]' in edgeLoop:
            print("found : ", bordersFound)
        if bordersFound == 2:
            usableEdges.append(edgeLoop)
        else:
            if allBorderFound == 2:
                if len(edgeLoop) != 1:
                    possibleEdges.append(edgeLoop)
            else:
                unusableEdges.append(edgeLoop)    
    # cmds.select(usableEdges)
    usable = testUnusable(usableEdges, unusableEdges, borderEdges)
    return usableEdges, possibleEdges, usable

def testPossible(usable, possible, borderEdges, alternativebo):
    usableEd = []
    unusable = []
    # pprint.pp(possible)
    for loop in possible:
        for edge in loop:
            use = 0
            everyOther = cmds.polySelect(objName, er =  getNumber(edge, "edge"), en = 2, q = True)
            for each in usable:
                for ed in each:
                    if getNumber(ed, "edge") in everyOther:
                        use += 1
            if use > 1:
                if type(loop) is list:
                    usableEd.extend(loop)
                    # pprint.pp(loop)
                    for e in everyOther:
                        edgeLoop = removeBrackets(cmds.polySelect(objName, el = e, q = True, ass = 1), "edge")
                        bordersFound = 0
                        allBorderFound = 0
                        
                        bordersFound = 0
                        allBorderFound = 0
                        for loop in edgeLoop:
                            if loop in borderEdges:
                                bordersFound += 1
                            if loop in borders:
                                allBorderFound += 1
                        if 'polySurface21.e[453]' in edgeLoop:
                            print("found poss : ", bordersFound)
                        if bordersFound == 2 :
                                usableEd.extend(edgeLoop)
                        if bordersFound == 1 and allBorderFound != 2:
                            #change if don't want unfished borders
                            unusable.extend(edgeLoop)
                        else:
                            if use >= len(edgeLoop) - len(usable):
                                for loop in edgeLoop:
                                    if loop in alternativebo:
                                        bordersFound += 1
                                    if loop in borders:
                                        allBorderFound += 1
                                    if 'polySurface21.e[453]' in edgeLoop:
                                        print("found poss : ", bordersFound)
                                    if bordersFound == 2:
                                        usableEd.extend(edgeLoop)
                                    else:
                                        unusable.extend(edgeLoop)


    # pprint.pp(usableEd)
    return usableEd

def testUnusable(usable, unusable, borderEdges):
    longestEdge = []
    span = 0
    for loop in usable:
        tempSpan = len(loop)
        if tempSpan > span:
            longestEdge = loop
            span = tempSpan
    cmds.select(clear = 1)
    cmds.select(longestEdge)
    usableEdges = []
    unusableEdges = []
    
    for index in longestEdge:
        use = 0
        everyOther = cmds.polySelect(objName, er =  getNumber(index, "edge"), en = 2, q = True)
        for each in usable:
            for ed in each:
                if getNumber(ed, "edge") in everyOther:
                  use += 1
        # print(use, " : ", len(usable), " : ", len(everyOther))
        if use >= len(usable):

            for edge in everyOther:
                edgeLoop = removeBrackets(cmds.polySelect(objName, el = edge, q = True, ass = 1), "edge")
                bordersFound = 0
                allBorderFound = 0
                for loop in edgeLoop:
                    if loop in borderEdges:
                        bordersFound += 1
                    if loop in borders:
                        allBorderFound += 1
                if bordersFound == 2:
                    usableEdges.extend(edgeLoop)
                    # cmds.select(usableEdges, add = 1)
                if 'polySurface21.e[448]' in edgeLoop:
                    print("found un: ", bordersFound)
                else:
                    if bordersFound == 1 and allBorderFound != 2:
                        unusableEdges.extend(edgeLoop)
                    if allBorderFound == 2:
                        unusableEdges.extend(edgeLoop)
                    else:
                        #change if you want unfinished edges
                        unusableEdges.extend(edgeLoop)

    for each in usable:
        usableEdges.extend(each)
    # cmds.select(usableEdges)
    # print (span)
    return usableEdges


def fifty():
    firstEdges = ['polySurface21.e[1]', 'polySurface21.e[3]', 'polySurface21.e[6]', 'polySurface21.e[9]', 'polySurface21.e[12]', 'polySurface21.e[14]', 'polySurface21.e[17]', 'polySurface21.e[19:22]', 'polySurface21.e[25]', 'polySurface21.e[28]', 'polySurface21.e[31]', 'polySurface21.e[34]', 'polySurface21.e[37]', 'polySurface21.e[40]', 'polySurface21.e[43]', 'polySurface21.e[46]', 'polySurface21.e[50]', 'polySurface21.e[53]', 'polySurface21.e[56]', 'polySurface21.e[58]', 'polySurface21.e[62]', 'polySurface21.e[65]', 'polySurface21.e[68]', 'polySurface21.e[71]', 'polySurface21.e[74]', 'polySurface21.e[76:79]', 'polySurface21.e[82]', 'polySurface21.e[85]', 'polySurface21.e[88]', 'polySurface21.e[91]', 'polySurface21.e[94]', 'polySurface21.e[124]', 'polySurface21.e[127:128]', 'polySurface21.e[216:217]', 'polySurface21.e[220:221]', 'polySurface21.e[224]', 'polySurface21.e[227]', 'polySurface21.e[230]', 'polySurface21.e[233]', 'polySurface21.e[236]', 'polySurface21.e[239]', 'polySurface21.e[242]', 'polySurface21.e[245]', 'polySurface21.e[248]', 'polySurface21.e[251]', 'polySurface21.e[254]', 'polySurface21.e[257]', 'polySurface21.e[260]', 'polySurface21.e[263]', 'polySurface21.e[268]', 'polySurface21.e[270]', 'polySurface21.e[273]', 'polySurface21.e[276]', 'polySurface21.e[279]', 'polySurface21.e[282]', 'polySurface21.e[285]', 'polySurface21.e[288]', 'polySurface21.e[291]', 'polySurface21.e[294]', 'polySurface21.e[297]', 'polySurface21.e[300]', 'polySurface21.e[303]', 'polySurface21.e[305]', 'polySurface21.e[308]']

    secondEdges = ['polySurface21.e[0]', 'polySurface21.e[2]', 'polySurface21.e[19]', 'polySurface21.e[21:22]', 'polySurface21.e[25]', 'polySurface21.e[28]', 'polySurface21.e[31]', 'polySurface21.e[34]', 'polySurface21.e[37]', 'polySurface21.e[40]', 'polySurface21.e[43]', 'polySurface21.e[46]', 'polySurface21.e[50]', 'polySurface21.e[53]', 'polySurface21.e[56]', 'polySurface21.e[58]', 'polySurface21.e[62]', 'polySurface21.e[65]', 'polySurface21.e[68]', 'polySurface21.e[71]', 'polySurface21.e[74]', 'polySurface21.e[77]', 'polySurface21.e[95:96]', 'polySurface21.e[98]', 'polySurface21.e[101]', 'polySurface21.e[103]', 'polySurface21.e[106]', 'polySurface21.e[109]', 'polySurface21.e[112]', 'polySurface21.e[116]', 'polySurface21.e[119]', 'polySurface21.e[122]', 'polySurface21.e[124]', 'polySurface21.e[127:130]', 'polySurface21.e[132]', 'polySurface21.e[135]', 'polySurface21.e[138]', 'polySurface21.e[141]', 'polySurface21.e[144]', 'polySurface21.e[147]', 'polySurface21.e[150]', 'polySurface21.e[153]', 'polySurface21.e[156]', 'polySurface21.e[159]', 'polySurface21.e[162]', 'polySurface21.e[165]', 'polySurface21.e[168]', 'polySurface21.e[171]', 'polySurface21.e[174]', 'polySurface21.e[177]', 'polySurface21.e[180]', 'polySurface21.e[183]', 'polySurface21.e[186]', 'polySurface21.e[189]', 'polySurface21.e[192]', 'polySurface21.e[195]', 'polySurface21.e[198]', 'polySurface21.e[201]', 'polySurface21.e[204]', 'polySurface21.e[207]', 'polySurface21.e[210]', 'polySurface21.e[213]', 'polySurface21.e[215]', 'polySurface21.e[309:311]', 'polySurface21.e[314]', 'polySurface21.e[317]', 'polySurface21.e[320]', 'polySurface21.e[323]', 'polySurface21.e[326]', 'polySurface21.e[329]', 'polySurface21.e[332]', 'polySurface21.e[335]', 'polySurface21.e[338]', 'polySurface21.e[341]', 'polySurface21.e[344]', 'polySurface21.e[347]', 'polySurface21.e[350]', 'polySurface21.e[353]', 'polySurface21.e[356]', 'polySurface21.e[359]', 'polySurface21.e[362]', 'polySurface21.e[365]', 'polySurface21.e[368]', 'polySurface21.e[371]', 'polySurface21.e[375]', 'polySurface21.e[378]', 'polySurface21.e[381]', 'polySurface21.e[384]', 'polySurface21.e[387]', 'polySurface21.e[390]', 'polySurface21.e[393]', 'polySurface21.e[395]', 'polySurface21.e[397]', 'polySurface21.e[399]', 'polySurface21.e[402]', 'polySurface21.e[405]', 'polySurface21.e[408]', 'polySurface21.e[411]', 'polySurface21.e[416]', 'polySurface21.e[419]', 'polySurface21.e[421]', 'polySurface21.e[424]', 'polySurface21.e[427]', 'polySurface21.e[1844]', 'polySurface21.e[1905]']

    
    global borders,  objName
    objName = 'polySurface21'
    borders = []
    borders.extend(correctEdgeFace(firstEdges))
    borders.extend(correctEdgeFace(secondEdges))
    first, firstPoss, useFirst= test(1617, correctEdgeFace(firstEdges))
    second, secondPoss, useSecond = test(1502, correctEdgeFace(secondEdges))

    addFirst = testPossible(second, firstPoss, correctEdgeFace(firstEdges), correctEdgeFace(firstEdges))
    addSecond = testPossible(first, secondPoss, correctEdgeFace(secondEdges), correctEdgeFace(secondEdges))
    cmds.select(useFirst)
    cmds.select(useSecond, add = True)
    cmds.select(addFirst, add = 1)
    cmds.select(useSecond, add = 1)

    edges = (cmds.ls(sl = 1))
    corners = [['polySurface21.e[59]',
  'polySurface21.e[2248]',
  'polySurface21.e[1985]',
  'polySurface21.e[2090]',
  'polySurface21.e[2148]',
  'polySurface21.e[63]',
  'polySurface21.e[2247]',
  'polySurface21.e[2352]',
  'polySurface21.e[58]',
  'polySurface21.e[2150]',
  'polySurface21.e[2149]',
  'polySurface21.e[2353]',
  'polySurface21.e[2354]'],
 ['polySurface21.e[1975]',
  'polySurface21.e[2070]',
  'polySurface21.e[1790]',
  'polySurface21.e[2069]',
  'polySurface21.e[1793]',
  'polySurface21.e[1974]',
  'polySurface21.e[2071]',
  'polySurface21.e[1791]'],
 ['polySurface21.e[1809]',
  'polySurface21.e[463]',
  'polySurface21.e[464]',
  'polySurface21.e[462]',
  'polySurface21.e[2352]',
  'polySurface21.e[2353]',
  'polySurface21.e[2315]',
  'polySurface21.e[2354]']]

    # allCorners = []
    # for each in corners:
    #     for e in each:
    #         if e in edges:
    #             for ed in each:
    #                 allCorners.extend(cmds.polySelect('polySurface21', el = getNumber(ed, "edge"), ass = 1, q = 1))
                
    # cmds.select(allCorners, add = True)
fifty()
