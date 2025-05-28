import sys
sys.path.append("/usr/lib/freecad-python3/lib")

import FreeCAD, Part

doc = FreeCAD.newDocument("Cone")
FreeCAD.setActiveDocument("Cone")
print(1)

cone = doc.addObject("Part::Cylinder", "Cone")
cone.Radius = 49.99
cone.Height = 1
print(2)

cone.Placement = FreeCAD.Placement(FreeCAD.Vector(0, 0.01, -5), FreeCAD.Rotation())
print(3)

doc.recompute()
print(4)

output_path = "/root/Gradio-UI/test_cone.FCStd"
try:
    doc.saveAs(output_path)
    print(f"✅ 模型保存成功：{output_path}")
except Exception as e:
    print(f"❌ 保存失败：{e}")
