import maya.cmds as cmds
import re 


def removeBrackets(set):
    if type(set) is list:
        typ= getType(set[0])
        correctedNames = []
        for item in set:
            objName, bracket = item.split(typ)
            if ":" in bracket:
                nPattern = re.compile(r'(\d+)') 
                numbers = nPattern.findall(bracket)
                for i in range(int(numbers[0]), int(numbers[1])+1):
                    correctedNames.append(objName + typ + "[" + str(i) + "]")
                    i += 1
            else:
                correctedNames.append(item)
    else:
        typ= getType(set)
        objName, bracket = item.split(typ)
        if ":" in bracket:
            correctedNames = []
            nPattern = re.compile(r'(\d+)') 
            numbers = nPattern.findall(bracket)
            for i in range(int(numbers[0]), int(numbers[1])+1):
                correctedNames.append(objName + typ+ "[" + str(i) + "]")
                i += 1
        else:
            correctedNames=item
    return correctedNames

def getType(n):
    if '.e[' in n:
        typ= '.e'
    if '.vtx[' in n:
        typ= '.vtx'

    return typ

        
def getNumber(edges):
    try:
        bracket = edges.split('.e[')[1]
        nPattern = re.compile(r'(\d+)') 
        number = nPattern.findall(bracket)[0]
        return int(number)
    except:
        bracket = edges.split('.f[')[1]
        nPattern = re.compile(r'(\d+)') 
        number = nPattern.findall(bracket)[0]
        return int(number)
    
borders = ['polySurface21.e[215]', 'polySurface21.e[219]', 'polySurface21.e[223]', 'polySurface21.e[226]', 'polySurface21.e[229]', 'polySurface21.e[232]', 'polySurface21.e[235]', 'polySurface21.e[238]', 'polySurface21.e[241]', 'polySurface21.e[244]', 'polySurface21.e[247]', 'polySurface21.e[250]', 'polySurface21.e[253]', 'polySurface21.e[256]', 'polySurface21.e[259]', 'polySurface21.e[262]', 'polySurface21.e[265]', 'polySurface21.e[267]', 'polySurface21.e[269]', 'polySurface21.e[272]', 'polySurface21.e[275]', 'polySurface21.e[278]', 'polySurface21.e[281]', 'polySurface21.e[284]', 'polySurface21.e[287]', 'polySurface21.e[290]', 'polySurface21.e[293]', 'polySurface21.e[296]', 'polySurface21.e[299]', 'polySurface21.e[302]', 'polySurface21.e[307]', 'polySurface21.e[310]']

def getLongName(edges):
    try:
        longN = []
        for edge in edges:
            longN.append('polySurface21' + ".e[" + str(edge) + "]")
    except:
        longN = ('polySurface21' + ".e[" + str(edges) + "]")
    return longN



def getEdges(borders):
    tested = []
    edges50 = []
    x = 0
    y = len(borders)
    z = 0
    edgesAll =[]
    breakpoint = []
    check = 0
    newCheck = 0
    close = removeBrackets(cmds.polySelect('polySurface21', eb = True, q = 1, ass = 1))
    save = ""
    broken = []
    for edge in borders:
        if edge not in tested:
            x += 1
            edgeNum = getNumber(edge)
            edgeRing = removeBrackets(cmds.polySelect('polySurface21', er= edgeNum, q = 1, ass = 1))
            verts = removeBrackets(cmds.polyListComponentConversion( edge, fe=True, tv=True ))

            vEdges = removeBrackets(cmds.polyListComponentConversion(verts, fv=True, te=True ))

            for v in vEdges:

                if v not in close and v != edge:
                    perpEdge = getNumber(v)
            found = False
            for e in edgeRing:
                if e in tested:
                    found = True
            if found == True:
                print(x, ": ", edge, len(broken))
                broken.append(edge)
            else:
            
                for e in edgeRing:
                    tested.extend(removeBrackets(cmds.polySelect('polySurface21', el= getNumber(e), q = True, ass = 1)))
                    tested = list(set(tested))
                check = 0
                edgeLoop = removeBrackets(cmds.polySelect('polySurface21', el= int(perpEdge) , q = True, ass = 1))
                if len(edgeLoop) == len(edgeRing) -1:
                    overlap = list(set(edgeRing) - set(borders)) 
                    edges50 = cmds.polySelect('polySurface21', er=edgeNum, en = 2, q = True, ass = 1)
                    use = cmds.polySelect('polySurface21', er=edgeNum, en = 2, q = True)
                    cmds.select(cl = 1)
                    for each in use:
                        cross = removeBrackets(cmds.polySelect('polySurface21', el= each, q = True, ass = 1))
                        if len(cross) == check:
                            edgesAll.extend(removeBrackets(cmds.polySelect('polySurface21', el= each, q = True, ass = 1)))
                        elif len(cross) > check:
                            check = len(cross)
                            edgesAll.extend(removeBrackets(cmds.polySelect('polySurface21', el= each, q = True, ass = 1)))
                        elif len(cross) < check and newCheck == len(cross):
                            check = len(cross)
                            edgesAll.extend(removeBrackets(cmds.polySelect('polySurface21', el= each, q = True, ass = 1)))
                            edgesAll.extend(removeBrackets(cmds.polySelect('polySurface21', el= save, q = True, ass = 1)))
                            
                            broken.remove(getLongName(save))
                            save = ""
                        else:
                            newCheck = len(cross)
                            save = each
                            broken.append(getLongName(each))
                            print("newSave")
                else:
                    z+=1
            # for over in overlap:
            #     tested.append(over)

            
            
                
  
        else:
            z +=1
            broken.append(edge)
    edges50 = []
    for i in range(0,len(edgesAll), 1):
        if edgesAll[i] not in borders:
            edges50.append(edgesAll[i])

    bEdges = []
    # for i in range(0,len(broken), 1):
    #     if broken[i] not in close:
    #         bEdges.append(broken[i])

    # print(edgesAll)
    print(y, " : ", x, " : ", z)    
    print(len(broken))
    cmds.select(broken)
    return(edgesAll)

a = getEdges(borders)
reversed = []
for i in range(len(borders)-1, -1, -1):
    reversed.append(borders[i])


#b = getEdges(reversed)

#cmds.select(a)


