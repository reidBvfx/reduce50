import maya.cmds as cmds
import re

cmds.polySelect( 'pCube1', edgeRing=1 )
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


testEdge = orderedEdges[0]
def findEdgeLoop(testEdge):
    testV = cmds.polyListComponentConversion(testEdge, tv = True, bo = True)
    testV = correctNameVertex(testV)
    testF = cmds.polyListComponentConversion(testEdge, tf = True, bo = True)
    testF = correctNameFace(testF)
    testE = [] 
    for each in testF:
        edge = cmds.polyListComponentConversion(each, te= True, bo = True)
        for e in edge:
            testE.append(e)
    testE = correctEdgeFace(testE)   
    nextEdge = []
    for v in testV:
        
        rEdges = cmds.polyListComponentConversion(v, te = True, bo = True)
        for e in rEdges:
            
            nextEdge.append(e)
    nextEdge = correctEdgeFace(nextEdge)
    next = ""
    edgeLoop = []
    #edgeLoop.append(testEdge)
    for each in nextEdge:
        if each not in testE:
            edgeLoop.append(each)
    return edgeLoop

def test(index):
    orderedEdges = cmds.polySelect( 'pCube1', edgeRing= index )
    evenOE = []
    for j in range(len(orderedEdges)):
         if j  % 2 != 0:
            evenOE.append('pCube1.e[' + str(orderedEdges[j]) + "]")

    cmds.select(evenOE)
    for each in evenOE:
        edgeLoop = [each]
        for i in range(100):
            try:
                secondEdge =  findEdgeLoop(edgeLoop[i])
            except:
                break
            
            if secondEdge == "":
                i = 200
            else:
                newE = False
                for each in secondEdge:
                    if each not in edgeLoop:
                        edgeLoop.append(each)
                        newE = True
                if newE == False:
                    i = 200           
                else:
                    i += 1            

        
            cmds.select(edgeLoop, add = True)
    selected = cmds.ls(sl=True,long=True)
    return selected 

def fifty():
    first = test(1427)
    second = test(1044)
    cmds.select(first, second)
    cmds.polyDelEdge( cv = True, ch = 1)

fifty()
