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
import time
import maya.mel as mel

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

def isBorder(edge):
    try:
        border = cmds.polySelect( objName, eb= int(getNumber(edge,"edge")), q = True) 
    except:
        border = cmds.polySelect( objName, eb= int(edge), q = True)  
    try:
        if len(border) > 0:
            return True
        else:
            return False
    except:
        return False   
def getLongName(edges):
    try:
        longN = []
        for edge in edges:
            longN.append(objName + ".e[" + str(edge) + "]")
    except:
        longN = (objName + ".e[" + str(edges) + "]")
    return longN

def getEdges(edges, extracted, checks):

    eoEdge = cmds.polySelect( 'polySurface21', er= edges, en = 2, q = True)
    

    erEnd = eoEdge[0]
    partial = cmds.polySelect('polySurface21', erp= [erEnd,edges], en = 2, q = True)
    print("ext: ", extracted)
    fullEdgeRings = []
    for edge in partial:
        fullEdgeRings.extend(cmds.polySelect('polySurface21', el= edge, q = True))
    if erEnd == edges:
        erEnd = eoEdge[len(eoEdge)-1]
        partial = cmds.polySelect('polySurface21', erp= [erEnd,edges], en = 2, q = True)
    use = []
    #get intersection and keep order of list
    if eoEdge[0] != edges:
        while(True):
            for i in range(len(eoEdge) - 1, -1, -1):
                if eoEdge[i] in partial:
                    use.append(eoEdge[i])
                i -= 1
                if i < 0:
                    break
            break
    else:
        for i in range(len(eoEdge)):
            if eoEdge[i] in partial :
                use.append(eoEdge[i])
            i+=1
    # assert use[0] == edges
    avg = True
    prev = 0
    
    el = []
    next = []
    print("start", edges)
    first = True
    for i in range(len(use)):
        if not isBorder(use[i]):
            if avg:
                avgLength = len(cmds.polySelect( 'polySurface21', el= use[i], q = True))
                avg = False
            edgeLoop = cmds.polySelect('polySurface21', el= use[i], q = True)
            if len(edgeLoop) == avgLength:
                el.extend(edgeLoop)
            elif len(edgeLoop) > avgLength:
                el.extend(edgeLoop)
                avgLength = len(edgeLoop)

            else:
                el.extend(edgeLoop)
                cmds.select(getLongName(use[i]))
                mel.eval('PolySelectTraverse 4')
                newLoopN =  removeBrackets(cmds.ls(sl = True), "edge")
                newLoop = []
                
                for name in newLoopN:
                    newLoop.append(getNumber(name, "edge"))
                
                if len(newLoop) > len(edgeLoop) and len(newLoop) != avgLength:
                    el.extend(newLoop)
                    diff = 0#(list(set(newLoopN) - set(edgeLoop)))
                    for each in newLoop:
                        if each not in edgeLoop:
                            testDiff = len(cmds.polySelect( 'polySurface21', er= each))
                            if testDiff > diff:
                                diff = testDiff
                                prev = each

                            
                    # if first == False:
                    #     next = []
                    next.append(prev)
                    first = False
                    #avgLength = len(edgeLoop)
                # else:
                #     next.append(edgeLoop[int(len(edgeLoop)-1)])
                #     first = False
              
                i += 1
        else:
            i +=1
            #break
    print(el)

    #checks.extend()
    el = checkFull(el, checks)
    print("prev", el)
    print("-----------------------------------------")
    return [el, next, fullEdgeRings]

def checkFull(selected, full):
    if needsCheck == False:
        print("ture no check")
        return selected
    else:
        newSel = []
        for each in selected:
            if each not in full:
                newSel.append(each)
        return newSel
    
def start():
    global objName
    #selected = removeBrackets(cmds.ls(sl = True), "edge")[0:2]
    objName = 'polySurface21'


    totalEdges = cmds.polyEvaluate(objName, e = True)
    reduced = totalEdges/2

    current = 0    
    cmds.select(cl = True)    
  
    edges = 246
    allowedtime = time.time() + (60)
    all = []
    x = 0
    while(True):
        if time.time() > allowedtime:
            print("timed out")
            break
        try:
            el, newEdgeLoop = getEdges(edges)

        except Exception as e:

            print("Exception: ", e)
            print(newEdgeLoop[0])
            break
        if len(set(all)) > reduced:
                print("too long", len(all))
                break
    cmds.select(all, add = True)
                
    
def test(edge, ext, checks):
    global objName
    #selected = removeBrackets(cmds.ls(sl = True), "edge")[0:2]
    objName = 'polySurface21'
    all = []
    el, newEdgeLoop, check = getEdges(edge, ext, checks)


    return el, newEdgeLoop, check

def testing(edge):
    global needsCheck
    needsCheck = False
    allowedtime = time.time() + (20)
    all = []
    x = 0
    addedEdges = []
    checks = []
    edges = []
    allel = []
    remove = []
    while(True and x < 2):
        if time.time() > allowedtime:
            print("timed out")
            break
         
        
        
        try:
            if edges not in addedEdges:
                el, newEdge, check = test(edge, all, checks)
                needsCheck = True
                all.extend(el)
                addedEdges.append(edges)
                edge = newEdge
                checks.extend(check)
                x += 1
                print("x = ", x) 
                print("NextEdge : ", edge)    
        except:
            for each in edge:
                if each not in addedEdges:
                    print("testing", each)
                    el, newEdge, check = test(int(each), all, checks)
                    needsCheck = True
                    addedEdges.append(each)
                    try:
                        edges.extend(newEdge)
                        all.extend(el)
                        checks.extend(check)
                    except:
                        pass
                    
                else:
                    remove.append(each)
                    pass
            
            edge = edges
            for each in remove:
                try:
                    edge.remove(each)
                except:
                    pass

        print(edge)
        if edge == []:
            break
            

    
    
        
    
    print("x = ", x)      
    cmds.select(getLongName(all))

testing([228, 145])