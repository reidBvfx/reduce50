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
    nextEdge = []
    listb = []
  
    for each in evenEdges:
        cmds.select(each)
        mel.eval('PolySelectTraverse 4')
        listb = cmds.ls(orderedSelection=True, fl=True)
        nextEdge.extend(listb)

        x = len(listb)
        for n in listb:
            verts = removeBrackets(cmds.polyListComponentConversion(n, tv = True, bo = True), "vertex")
            for vert in verts:
                vEdges = removeBrackets(cmds.polyListComponentConversion(vert, te = True, bo = True), "edge")
                corner = []
                if len(vEdges) > 4:
                    # corner = getCornerEdges(vEdges)
                    nextEdge.extend(corner)
                    print("corner: " , vert)
    return nextEdge


def getCornerEdges(e):
    nextEdge = []
    for each in e:
        cmds.select(each)
        mel.eval('PolySelectTraverse 4')
        listb = cmds.ls(orderedSelection=True, fl=True)
        nextEdge.extend(listb)
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



