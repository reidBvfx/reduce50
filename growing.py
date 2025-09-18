import maya.cmds as cmds
import maya.mel as mel
import mayaNameFormat as mf
import time
import re


cmds.select('polySurface21.e[79]')
readBorder = []

class MeshWorm():
    def __init__(self):
        self.eaten = []
        self.eatenBE = []
        self.eatenVert = ""
        self.objName = 'polySurface21'
        self.borders = mf.removeBrackets(cmds.polySelect(self.objName, eb = True, q = 1, ass = 1))
    
    def getEfE(self):
        """ get edge loop from selected edge"""
        print("efe called")
        self.starterEdges = mf.removeBrackets(cmds.ls(sl =1))
        edgeLoop = []
        for edge in self.starterEdges:
            edgeTrans = mf.removeBrackets(cmds.polySelect(self.objName, el = mf.getNumber(edge), q = 1, ass = 1))
            if type(edgeTrans) is list:
                edgeTrans.remove(edge)
                edgeLoop.append(edgeTrans)
                
            else:
                edgeLoop.append(edgeTrans)
                try:
                    edgeLoop.remove(edge)
                except Exception as e:
                    print(e, " : ", edge)
            self.eaten.append(edge)
            self.eatenVert = mf.removeBrackets(cmds.polyListComponentConversion(edge, fe=True, tv=True ))
        return edgeLoop

    def getNextEdge(self, edgeLoop):
        print("getNexededge called")
        nextEdge = []
        for each in edgeLoop:
            
            verts = mf.removeBrackets(cmds.polyListComponentConversion( each, fe=True, tv=True ))
            for prevV in self.eatenVert:
                if prevV in verts:
                    verts.remove(prevV)
            vEdges = mf.removeBrackets(cmds.polyListComponentConversion(verts, fv=True, te=True ))
            for edge in vEdges:
                if edge in self.borders:
                    nextEdge.append(edge)
        if len(nextEdge) == 1:
            nextEdge = nextEdge[0]
        try:
            return nextEdge
        except:
            print("nextEdgeisEmpty")
            return
    
    def getNextStarter(self, bEdge):
        print("getNextStarted called")
        #remove any none returns
        path = []
        # print("bb: ", bEdge)
        if type(bEdge) is list and len(bEdge) > 1:
            # print("is list")
            bEdge = [border for border in bEdge if border is not None]
            for border in bEdge:
                cmds.select(border)
                mel.eval('PolySelectTraverse 5')
                firstStep = mf.removeBrackets(cmds.ls(sl = True))
                
                if border in firstStep:
                    firstStep.remove(border)
                if len(firstStep) == 1:
                    cmds.select(border)
                    mel.eval('PolySelectTraverse 1')
                    firstStep = mf.removeBrackets(cmds.ls(sl = True))
                    firstStep.remove(border)
                    borderPath = []
                    for edge in firstStep:
                        if edge in self.borders and edge not in self.eatenBE:
                            borderPath.append(edge)
                    firstStep = borderPath

                    for each in firstStep:
                        cmds.select(each)
                        mel.eval('PolySelectTraverse 5')
                        path.extend(mf.removeBrackets(cmds.ls(sl = True)))
                        if each in path:
                            path.remove(each)
    
                        if border in path:
                            path.remove(border)
                               
            
                for eatenB in self.eatenBE:
                    if eatenB in path:
                        path.remove(eatenB)
            self.eatenBE.extend(bEdge)
            # print("if: ", path) 
        else:
            if type(bEdge) is list:
                bEdge = bEdge[0]
            cmds.select(bEdge)
            mel.eval('PolySelectTraverse 5')
            firstStep = mf.removeBrackets(cmds.ls(sl = True))
            if bEdge in firstStep:
                firstStep.remove(bEdge)
    
            # if edge is on a corner
            if len(firstStep) == 1:
                cmds.select(bEdge)
                mel.eval('PolySelectTraverse 1')
                firstStep = mf.removeBrackets(cmds.ls(sl = True))
                firstStep.remove(bEdge)
                borderPath = []
                for edge in firstStep:
                    if edge in self.borders:
                        borderPath.append(edge)
                firstStep = borderPath
        
        
        for each in firstStep:
            cmds.select(each)
            mel.eval('PolySelectTraverse 5')
            path.extend(mf.removeBrackets(cmds.ls(sl = True)))
            if each in path:
                path.remove(each)
            if bEdge in path or bEdge in self.eatenBE:
                    path.remove(bEdge)
                
        self.eatenBE.extend(bEdge)
        # print("bf: ", path) 
        uniqueVerts = self.getUniqueVerts(bEdge, firstStep, path)
        nextEdges = self.getNonBorder(uniqueVerts)
        
        return nextEdges
    
    def getNonBorder(self, verts):
        print("gNB called")
        
        if type(verts) is list:
            verts = [vert for vert in verts if vert is not None]
            verts = [vert for vert in verts if vert != []]
        # print("vert", verts)
        nextEdges = []
        for vert in verts:
           edges = mf.removeBrackets(cmds.polyListComponentConversion(vert, fv=True, te=True))
           for edge in edges:
               if edge not in self.borders:
                   nextEdges.append(edge)
        
        return nextEdges
    
    def getUniqueVerts(self, bEdge, firstStep, path):
        print("getU called")
        print(path)
        uniqueVerts = []
        for each in path:
            nonUniqueVerts = mf.removeBrackets(cmds.polyListComponentConversion( bEdge, fe=True, tv=True ))
            nonUniqueVerts.extend(mf.removeBrackets(cmds.polyListComponentConversion( firstStep, fe=True, tv=True )))
            testVerts = mf.removeBrackets(cmds.polyListComponentConversion( each, fe=True, tv=True ))
            uniqueVerts.append(list(set(testVerts)- set(nonUniqueVerts)))
        # print(uniqueVerts)
        return uniqueVerts

    def eat(self):
        try:    
            for i in range (1):

                edgeLoop = self.getEfE()

                if len(edgeLoop) > 1:
                    nextEdge = []
                    for edges in edgeLoop:
                        nextEdge.extend(self.getNextEdge(edges))
                    self.eaten.extend(edgeLoop)
                else:
                    nextEdge = self.getNextEdge(edgeLoop)
                    self.eaten.extend(edgeLoop)
                if type(nextEdge) is list:
                    nextEdge = [edge for edge in nextEdge if edge is not None]
                    nextEdge = [edge for edge in nextEdge if edge != []]
                    removed = []
                    
                    for edge in nextEdge:
                        if edge not in self.eaten:
                            removed.append(edge)
                    nextEdge = removed
                else:
                    if nextEdge in self.eaten:
                        # nextEdge = self.getNextEdge(self.getEfE())
                        print("in self eaten")
                nextStarterEdge = self.getNextStarter(nextEdge) 
                cmds.select(nextStarterEdge)

            
        except Exception as e:
            print(e)  
        # cmds.select(cl =1)
        # # print(self.eaten)
        # for crumb in self.eaten:
        #         try:
        #             for c in crumb:
        #                 cmds.select(crumb, add = True)
        #         except:
        #             cmds.select(crumb, add = True)

worm = MeshWorm()
worm.eat()