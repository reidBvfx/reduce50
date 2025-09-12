# STYLE ***************************************************************************
# content = evenly reduce polymesh by 50 %
#           selects everyother edge loop
#           requires selection of one vertical and one horizontal line
# date    = 2025-09-12
#
# author  = Reid Bryan (reidwarhola@gmail.com)
# **********************************************************************************
import maya.cmds as cmds
import re


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
            edgeLoop.append(edge)
    return edgeLoop

def getEdges(objName, index):
    """ find every other edge in edgeRing and the find edge loop of each edge"""
    edgeRing = cmds.polySelect( objName, edgeRing= index )
    evenEdges = [] # get every other edge in ring
    for j in range(len(edgeRing)):
         if j  % 2 != 0:
            evenEdges.append(objName + '.e[' + str(edgeRing[j]) + "]")

    cmds.select(evenEdges)
    first = True
    allEdges = []
    for each in evenEdges:
        edgeLoop = [each]
        edgeLoopLength = 100
        for i in range(edgeLoopLength):
            try:
                secondEdge =  findEdgeLoop(edgeLoop[i])
            except:
                break
            
            if secondEdge == "":
                i = edgeLoopLength + 100 
            else:
                newE = False
                for each in secondEdge:
                    if each not in edgeLoop:
                        edgeLoop.append(each)
                        newE = True
                if newE == False:
                    i = edgeLoopLength + 100           
                else:
                    i += 1            

        allEdges.extend(edgeLoop)
    return allEdges 

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
