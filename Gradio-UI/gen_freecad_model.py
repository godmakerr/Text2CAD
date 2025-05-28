import sys
sys.path.append('/usr/lib/freecad-python3/lib')
import FreeCAD, Part
doc = FreeCAD.newDocument("Box")
box = doc.addObject("Part::Box", "Box")
box.Length = 47
box.Width = 175
box.Height = 186
doc.recompute()
# 自动保存 .FCStd 供后续预览 / 下载
import os
_out = os.path.join(os.path.dirname(__file__), "model.FCStd")
try:
    doc.saveAs(_out)
except Exception as _e:
    print('Skip saveAs:', _e)
