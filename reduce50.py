# STYLE ***************************************************************************
# content = evenly reduce polymesh by 50 %
#           selects everyother edge loop
#           requires selection of one vertical and one horizontal line
# date    = 2025-09-12
#
# author  = Reid Bryan (reidwarhola@gmail.com)
# **********************************************************************************
import maya.cmds as cmds
import maya.mel as mel
import re
import time


def getName(item, type):
    type = getType(type)
    objName = item.split(type)[0]
    return objName

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
    return number

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

def findEdgeLoop(evenEdges):
    """ find an edge loop by comparing all the edges of neighboring faces to all the edges of neighboring vertices
        the difference is the edgeloop"""
    
    faces = cmds.polyListComponentConversion(evenEdges, tf = True, bo = True)
    faces = removeBrackets(faces, "face")
    fEdges = [] 
    for face in faces:
        fEdges.extend(cmds.polyListComponentConversion(face, te= True, bo = True))
    fEdges = removeBrackets(fEdges, "edge")   

    vertices = cmds.polyListComponentConversion(evenEdges, tv = True, bo = True)
    vertices = removeBrackets(vertices, "vertex")
    
    vEdges = []
    for v in vertices:
        vEdges.extend(cmds.polyListComponentConversion(v, te = True, bo = True))
    vEdges = removeBrackets(vEdges, "edge")
    edgeLoop = []
    for edge in vEdges:
        if edge not in fEdges:
            if edge in edgeLoop:
                edgeLoop.remove(edge)
            else:
                edgeLoop.append(edge)
    return edgeLoop

def getEdges(objName, index):
    """ find every other edge in edgeRing and the find edge loop of each edge"""
    edgeRing = cmds.polySelect( objName, edgeRing= index )
    evenEdges = [] # get every other edge in ring
    oddEdges = []
    for j in range(len(edgeRing)):
        if j  % 2 != 0:
            evenEdges.append(objName + '.e[' + str(edgeRing[j]) + "]")
        else:
            oddEdges.append(objName + '.e[' + str(edgeRing[j]) + "]")

    cmds.select(evenEdges)
    first = True
    allEdges = []
    # evenEdges = evenEdges[2:4]
    nextEdge = []
    listb = []
    
    total_iters = 30
    for each in evenEdges:
        lista = cmds.select(each)
        mel.eval('PolySelectTraverse 4')
        listb = cmds.ls(orderedSelection=True, fl=True)
        nextEdge.extend(listb)
        #for a in range(total_iters):
        edgeLoopLength = len(listb)
        for i in range(edgeLoopLength):
            print("listb", listb[i])
            try:
                secondEdge =  findEdgeLoop(listb[i])    
            except:
                break
            if len(secondEdge) > 2: 
                corner = []
                first = True
                corner.extend(getCornerEdgeLoop(listb[i]))
                for edge in corner:
                    if edge not in oddEdges:
                        secondEdge.append(edge)
                    
                for each in secondEdge:
                    if each not in nextEdge:
                        nextEdge.append(each)   
                        # assert'soccer_outfit_kit_01_1001.e[5384]' not in nextEdge
                        # assert'soccer_outfit_kit_01_1001.e[3940]' not in nextEdge
                        # assert'soccer_outfit_kit_01_1001.e[3391]' not in nextEdge    
            #assert'soccer_outfit_kit_01_1001.e[5384]' not in edgeLoop
        allEdges.extend(nextEdge)
    return allEdges 

def getCornerEdgeLoop(edge):
    edgeLoop = []
    #get all edges of corner
    vertices = cmds.polyListComponentConversion(edge, tv = True, bo = True)
    vertices = removeBrackets(vertices, "vertex")
    for vertex in vertices:
        edgeLoop = []
        print("vertex" + vertex)
        vEdges = []
        vEdges.extend(cmds.polyListComponentConversion(vertex, te = True, bo = True))
        vEdges = removeBrackets(vEdges, "edge")
        for vEdge in vEdges:
            if vEdge != edge:
                edgeLoop.append(vEdge)
        print(len(edgeLoop))
        if len(edgeLoop) <= 3:
            edgeLoop = []
            print("new: " + str(len(edgeLoop)))
        else:
            print(edgeLoop)
            total_iters = 30 # number just needs to be large enough
            # assert'soccer_outfit_kit_01_1001.e[5384]' not in edgeLoop
            nextEdge = []
            listb = []
            lista = cmds.select(edgeLoop[0])
            for edge in edgeLoop:
                    try:
                        assert edge != 'soccer_outfit_kit_01_1001.e[5589]' 
                    except AssertionError as e:
                        print (e)
                        break
                    cmds.select(edge)
                    mel.eval('PolySelectTraverse 4')
                    listb = cmds.ls(orderedSelection=True, fl=True)
                    listb = removeBrackets(listb, "edge")
                    nextEdge.extend(listb)
                
    cmds.select(nextEdge)
    return nextEdge

   

def start():
    
    selected = removeBrackets(cmds.ls(sl = True), "edge")
    objName = getName(selected[0], "edge")
    edgeNums = []
    for edge in selected:
        edgeNums.append(getNumber(edge, "edge"))
    
    allEdges = []
    for num in edgeNums:
        allEdges.extend(getEdges(objName, int(num)))
    
    cmds.select(clear = True)
    cmds.select(allEdges)
    #cmds.polyDelEdge( cv = True, ch = 1)

def fifty():
    cmds.select(clear = True)
    cmds.select(['pCube1.e[1427]', 'pCube1.e[1044]'])
    start()


start()

#getCornerEdgeLoop('soccer_outfit_kit_01_1001.e[3334]')



