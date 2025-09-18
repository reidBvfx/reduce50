import maya.mel as mel
import maya.cmds as cmds

# cmds.select(['polySurface21.f[28]', 'polySurface21.f[75]', 'polySurface21.f[166]', 'polySurface21.f[205]', 'polySurface21.f[294]', 'polySurface21.f[355]', 'polySurface21.f[384]', 'polySurface21.f[441]', 'polySurface21.f[444:470]', 'polySurface21.f[812]', 'polySurface21.f[826:828]', 'polySurface21.f[839]', 'polySurface21.f[867]'])

faces = []
oddRow = []
for i in range(50):
    faces.extend(cmds.ls(sl = True))
    mel.eval('PolySelectTraverse 1')
    oddRow.extend(cmds.ls(sl = True))

cmds.select(faces, tgl = True)

# next = cmds.ls(sl = True)
# print((len(faces)), " : ", len(oddRow))
# cmds.select(oddRow)