#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
生成 PartDesign 工作台特征建模脚本样本（Pad / Revolve / Pocket / Sweep / Loft /
Fillet / Chamfer / Pattern）。共 300 条，保存为 JSON。
"""

import json
import random
import math
from pathlib import Path


# ────────────────────────────────────────────
# 1. Pad / Extrude
# ────────────────────────────────────────────
def generate_pad_samples(num_samples: int = 60):
    samples = []
    for _ in range(num_samples):
        sketch_type = random.choice(['rectangle', 'circle', 'polygon', 'complex'])
        length = random.randint(10, 100)

        # 双向拉伸
        if random.choice([True, False]):
            length2 = random.randint(10, 100)
            length_text = f"正向 {length} mm、反向 {length2} mm"
            length_code = f"pad.Length = {length}\npad.Length2 = {length2}"
        else:
            length_text = f"{length} mm"
            length_code = f"pad.Length = {length}"

        # 斜度
        if random.choice([True, False]):
            taper = random.randint(1, 15)
            taper_text = f"，斜度 {taper}°"
            taper_code = f"pad.TaperAngle = {taper}"
        else:
            taper_text = ""
            taper_code = ""

        # 草图
        if sketch_type == 'rectangle':
            w, h = random.randint(20, 150), random.randint(20, 150)
            sk_text = f"矩形（{w}×{h} mm）"
            sk_code = (
                "sketch = doc.addObject('Sketcher::SketchObject', 'Sketch')\n"
                f"sketch.addGeometry(Part.LineSegment(FreeCAD.Vector(0,0,0), FreeCAD.Vector({w},0,0)), False)\n"
                f"sketch.addGeometry(Part.LineSegment(FreeCAD.Vector({w},0,0), FreeCAD.Vector({w},{h},0)), False)\n"
                f"sketch.addGeometry(Part.LineSegment(FreeCAD.Vector({w},{h},0), FreeCAD.Vector(0,{h},0)), False)\n"
                f"sketch.addGeometry(Part.LineSegment(FreeCAD.Vector(0,{h},0), FreeCAD.Vector(0,0,0)), False)"
            )
        elif sketch_type == 'circle':
            r = random.randint(10, 50)
            sk_text = f"圆（半径 {r} mm）"
            sk_code = (
                "sketch = doc.addObject('Sketcher::SketchObject', 'Sketch')\n"
                f"sketch.addGeometry(Part.Circle(FreeCAD.Vector(0,0,0), FreeCAD.Vector(0,0,1), {r}), False)"
            )
        elif sketch_type == 'polygon':
            n = random.randint(3, 8)
            rad = random.randint(20, 60)
            sk_text = f"{n} 边形（外接圆半径 {rad} mm）"
            sk_code = (
                "sketch = doc.addObject('Sketcher::SketchObject', 'Sketch')\n"
                f"verts=[]\nfor i in range({n}):\n"
                f"    a=2*math.pi*i/{n}\n    verts.append(FreeCAD.Vector({rad}*math.cos(a), {rad}*math.sin(a), 0))\n"
                f"for i in range({n}):\n"
                f"    sketch.addGeometry(Part.LineSegment(verts[i], verts[(i+1)%{n}]), False)"
            )
        else:
            sk_text = "复杂轮廓"
            sk_code = (
                "sketch = doc.addObject('Sketcher::SketchObject', 'Sketch')\n"
                "# 外矩形\n"
                "sketch.addGeometry(Part.LineSegment(FreeCAD.Vector(0,0,0), FreeCAD.Vector(60,0,0)), False)\n"
                "sketch.addGeometry(Part.LineSegment(FreeCAD.Vector(60,0,0), FreeCAD.Vector(60,40,0)), False)\n"
                "sketch.addGeometry(Part.LineSegment(FreeCAD.Vector(60,40,0), FreeCAD.Vector(0,40,0)), False)\n"
                "sketch.addGeometry(Part.LineSegment(FreeCAD.Vector(0,40,0), FreeCAD.Vector(0,0,0)), False)\n"
                "# 内圆\n"
                "sketch.addGeometry(Part.Circle(FreeCAD.Vector(20,20,0), FreeCAD.Vector(0,0,1), 10), False)"
            )

        desc = f"创建 {sk_text} 草图并拉伸 {length_text}{taper_text}。"
        code = f"""import FreeCAD, Part, PartDesign, Sketcher, math
doc = FreeCAD.newDocument("Pad")
body = doc.addObject('PartDesign::Body', 'Body')
{sk_code}
body.addObject(sketch)
pad = doc.addObject('PartDesign::Pad','Pad')
pad.Profile = sketch
{length_code}
{taper_code}
doc.recompute()"""
        samples.append({"input": desc, "output": code})
    return samples


# ────────────────────────────────────────────
# 2. Revolve
# ────────────────────────────────────────────
def generate_revolve_samples(num_samples: int = 50):
    samples = []
    for _ in range(num_samples):
        sketch_type = random.choice(['rectangle', 'trapezoid', 'semicircle', 'complex'])
        angle = random.randint(90, 360)
        angle_text = "360°" if angle == 360 else f"{angle}°"

        axis_type = random.choice(['x_axis', 'y_axis', 'custom'])
        if axis_type == 'x_axis':
            axis_text = "X 轴"
            axis_code = "revolve.ReferenceAxis = (sketch, ['V_Axis'])"
        elif axis_type == 'y_axis':
            axis_text = "Y 轴"
            axis_code = "revolve.ReferenceAxis = (sketch, ['H_Axis'])"
        else:
            p1 = (random.randint(-50, 50), random.randint(-50, 50))
            p2 = (random.randint(-50, 50), random.randint(-50, 50))
            axis_text = f"自定义轴 ({p1[0]},{p1[1]})→({p2[0]},{p2[1]})"
            axis_code = (
                f"edge = sketch.addGeometry(Part.LineSegment(FreeCAD.Vector({p1[0]},{p1[1]},0), "
                f"FreeCAD.Vector({p2[0]},{p2[1]},0)), True)\n"
                "revolve.ReferenceAxis = (sketch, [f'Edge{{edge+1}}'])"
            )

        # 草图
        if sketch_type == 'rectangle':
            w, h = random.randint(10, 50), random.randint(20, 80)
            off = random.randint(10, 30)
            sk_text = f"矩形（{w}×{h} mm）"
            sk_code = (
                "sketch = doc.addObject('Sketcher::SketchObject','Sketch')\n"
                f"sketch.addGeometry(Part.LineSegment(FreeCAD.Vector({off},0,0),FreeCAD.Vector({off+w},0,0)),False)\n"
                f"sketch.addGeometry(Part.LineSegment(FreeCAD.Vector({off+w},0,0),FreeCAD.Vector({off+w},{h},0)),False)\n"
                f"sketch.addGeometry(Part.LineSegment(FreeCAD.Vector({off+w},{h},0),FreeCAD.Vector({off},{h},0)),False)\n"
                f"sketch.addGeometry(Part.LineSegment(FreeCAD.Vector({off},{h},0),FreeCAD.Vector({off},0,0)),False)"
            )
        elif sketch_type == 'trapezoid':
            w1, w2, h = random.randint(10, 40), random.randint(20, 60), random.randint(20, 80)
            off = random.randint(10, 30)
            sk_text = f"梯形（顶 {w1} mm、底 {w2} mm、高 {h} mm）"
            top = off + (w2 - w1) / 2
            sk_code = (
                "sketch = doc.addObject('Sketcher::SketchObject','Sketch')\n"
                f"sketch.addGeometry(Part.LineSegment(FreeCAD.Vector({off},0,0),FreeCAD.Vector({off+w2},0,0)),False)\n"
                f"sketch.addGeometry(Part.LineSegment(FreeCAD.Vector({off+w2},0,0),FreeCAD.Vector({top+w1},{h},0)),False)\n"
                f"sketch.addGeometry(Part.LineSegment(FreeCAD.Vector({top+w1},{h},0),FreeCAD.Vector({top},{h},0)),False)\n"
                f"sketch.addGeometry(Part.LineSegment(FreeCAD.Vector({top},{h},0),FreeCAD.Vector({off},0,0)),False)"
            )
        elif sketch_type == 'semicircle':
            r = random.randint(20, 50)
            off = random.randint(10, 30)
            sk_text = f"半圆（半径 {r} mm）"
            sk_code = (
                "sketch = doc.addObject('Sketcher::SketchObject','Sketch')\n"
                f"sketch.addGeometry(Part.ArcOfCircle(Part.Circle(FreeCAD.Vector({off},0,0),FreeCAD.Vector(0,0,1),{r}),0,math.pi),False)\n"
                f"sketch.addGeometry(Part.LineSegment(FreeCAD.Vector({off}, {r}, 0), FreeCAD.Vector({off}, -{r}, 0)), False)"
            )
        else:
            sk_text = "复杂轮廓"
            sk_code = (
                "sketch = doc.addObject('Sketcher::SketchObject','Sketch')\n"
                "sketch.addGeometry(Part.LineSegment(FreeCAD.Vector(10,0,0),FreeCAD.Vector(40,0,0)),False)\n"
                "sketch.addGeometry(Part.LineSegment(FreeCAD.Vector(40,0,0),FreeCAD.Vector(40,20,0)),False)\n"
                "sketch.addGeometry(Part.LineSegment(FreeCAD.Vector(40,20,0),FreeCAD.Vector(30,20,0)),False)\n"
                "sketch.addGeometry(Part.LineSegment(FreeCAD.Vector(30,20,0),FreeCAD.Vector(30,40,0)),False)\n"
                "sketch.addGeometry(Part.LineSegment(FreeCAD.Vector(30,40,0),FreeCAD.Vector(10,40,0)),False)\n"
                "sketch.addGeometry(Part.LineSegment(FreeCAD.Vector(10,40,0),FreeCAD.Vector(10,0,0)),False)"
            )

        desc = f"创建 {sk_text} 草图并绕 {axis_text} 旋转 {angle_text} 放样实体。"
        code = f"""import FreeCAD, Part, PartDesign, Sketcher, math
doc=FreeCAD.newDocument('Revolve')
body=doc.addObject('PartDesign::Body','Body')
{sk_code}
body.addObject(sketch)
revolve=doc.addObject('PartDesign::Revolution','Revolve')
revolve.Profile=sketch
revolve.Angle={angle}
{axis_code}
doc.recompute()"""
        samples.append({"input": desc, "output": code})
    return samples


# ────────────────────────────────────────────
# 3. Pocket
# ────────────────────────────────────────────
def generate_pocket_samples(num_samples: int = 50):
    samples = []
    for _ in range(num_samples):
        base_type = random.choice(['box', 'cylinder'])

        if base_type == 'box':
            L, W, H = random.randint(50, 150), random.randint(50, 150), random.randint(30, 100)
            base_desc = f"长方体（{L}×{W}×{H} mm）"
            base_code = f"""body=doc.addObject('PartDesign::Body','Body')
sk0=doc.addObject('Sketcher::SketchObject','BaseSketch')
sk0.addGeometry(Part.LineSegment(FreeCAD.Vector(0,0,0),FreeCAD.Vector({L},0,0)),False)
sk0.addGeometry(Part.LineSegment(FreeCAD.Vector({L},0,0),FreeCAD.Vector({L},{W},0)),False)
sk0.addGeometry(Part.LineSegment(FreeCAD.Vector({L},{W},0),FreeCAD.Vector(0,{W},0)),False)
sk0.addGeometry(Part.LineSegment(FreeCAD.Vector(0,{W},0),FreeCAD.Vector(0,0,0)),False)
body.addObject(sk0)
pad0=doc.addObject('PartDesign::Pad','BasePad')
pad0.Profile=sk0
pad0.Length={H}
doc.recompute()"""
        else:
            R, H = random.randint(30, 80), random.randint(30, 100)
            base_desc = f"圆柱体（半径 {R} mm，高 {H} mm）"
            base_code = f"""body=doc.addObject('PartDesign::Body','Body')
sk0=doc.addObject('Sketcher::SketchObject','BaseSketch')
sk0.addGeometry(Part.Circle(FreeCAD.Vector(0,0,0),FreeCAD.Vector(0,0,1),{R}),False)
body.addObject(sk0)
pad0=doc.addObject('PartDesign::Pad','BasePad')
pad0.Profile=sk0
pad0.Length={H}
doc.recompute()"""

        pocket_shape = random.choice(['circle', 'rectangle', 'polygon'])
        depth = random.randint(10, 50)
        through = random.choice([True, False])

        if pocket_shape == 'circle':
            r = random.randint(10, 30)
            pocket_desc = f"圆（半径 {r} mm）"
            pocket_geo = f"p_sk.addGeometry(Part.Circle(FreeCAD.Vector(0,0,0),FreeCAD.Vector(0,0,1),{r}),False)"
        elif pocket_shape == 'rectangle':
            a, b = random.randint(20, 80), random.randint(20, 80)
            pocket_desc = f"矩形（{a}×{b} mm）"
            pocket_geo = (
                f"p_sk.addGeometry(Part.LineSegment(FreeCAD.Vector(-{a/2},-{b/2},0),FreeCAD.Vector({a/2},-{b/2},0)),False)\n"
                f"p_sk.addGeometry(Part.LineSegment(FreeCAD.Vector({a/2},-{b/2},0),FreeCAD.Vector({a/2},{b/2},0)),False)\n"
                f"p_sk.addGeometry(Part.LineSegment(FreeCAD.Vector({a/2},{b/2},0),FreeCAD.Vector(-{a/2},{b/2},0)),False)\n"
                f"p_sk.addGeometry(Part.LineSegment(FreeCAD.Vector(-{a/2},{b/2},0),FreeCAD.Vector(-{a/2},-{b/2},0)),False)"
            )
        else:
            n = random.randint(3, 6)
            rad = random.randint(15, 30)
            pocket_desc = f"{n} 边形（外接圆半径 {rad} mm）"
            poly_geo = (
                "verts=[]\n"
                f"for i in range({n}):\n"
                f"    ang=2*math.pi*i/{n}\n"
                f"    verts.append(FreeCAD.Vector({rad}*math.cos(ang), {rad}*math.sin(ang),0))\n"
                f"for i in range({n}):\n"
                f"    p_sk.addGeometry(Part.LineSegment(verts[i], verts[(i+1)%{n}]),False)"
            )
            pocket_geo = poly_geo

        depth_desc = "通孔" if through else f"深度 {depth} mm"
        depth_code = "pocket.Type = 1" if through else f"pocket.Length = {depth}"

        desc = f"在 {base_desc} 顶面挖一个 {pocket_desc} 的 {depth_desc} 沟槽。"
        code = f"""import FreeCAD, Part, PartDesign, Sketcher, math
doc=FreeCAD.newDocument('Pocket')
{base_code}
p_sk=doc.addObject('Sketcher::SketchObject','PocketSketch')
{pocket_geo}
p_sk.MapMode='FlatFace'
p_sk.Support=[(doc.getObject('BasePad'),'Face6')]
body.addObject(p_sk)
pocket=doc.addObject('PartDesign::Pocket','Pocket')
pocket.Profile=p_sk
{depth_code}
doc.recompute()"""
        samples.append({"input": desc, "output": code})
    return samples


# ────────────────────────────────────────────
# 4. Sweep
# ────────────────────────────────────────────
def generate_sweep_samples(num_samples: int = 40):
    samples = []
    for _ in range(num_samples):
        profile = random.choice(['circle', 'rectangle'])
        path = random.choice(['line', 'arc'])

        if profile == 'circle':
            pr = random.randint(5, 20)
            pr_desc = f"圆（半径 {pr} mm）"
            pr_code = (
                "profile = doc.addObject('Sketcher::SketchObject','Profile')\n"
                f"profile.addGeometry(Part.Circle(FreeCAD.Vector(0,0,0),FreeCAD.Vector(0,0,1),{pr}),False)"
            )
        else:
            w, h = random.randint(5, 20), random.randint(5, 20)
            pr_desc = f"矩形（{w}×{h} mm）"
            pr_code = (
                "profile = doc.addObject('Sketcher::SketchObject','Profile')\n"
                f"profile.addGeometry(Part.LineSegment(FreeCAD.Vector(0,0,0),FreeCAD.Vector({w},0,0)),False)\n"
                f"profile.addGeometry(Part.LineSegment(FreeCAD.Vector({w},0,0),FreeCAD.Vector({w},{h},0)),False)\n"
                f"profile.addGeometry(Part.LineSegment(FreeCAD.Vector({w},{h},0),FreeCAD.Vector(0,{h},0)),False)\n"
                f"profile.addGeometry(Part.LineSegment(FreeCAD.Vector(0,{h},0),FreeCAD.Vector(0,0,0)),False)"
            )

        if path == 'line':
            L = random.randint(40, 100)
            path_desc = f"直线（{L} mm）"
            path_code = (
                "path=doc.addObject('Part::Feature','Path')\n"
                f"path.Shape=Part.LineSegment(FreeCAD.Vector(0,0,0),FreeCAD.Vector({L},0,0)).toShape()"
            )
        else:
            r = random.randint(40, 80)
            ang = random.randint(90, 180)
            path_desc = f"圆弧（半径 {r} mm，{ang}°）"
            path_code = (
                "path=doc.addObject('Part::Feature','Path')\n"
                f"path.Shape=Part.ArcOfCircle(Part.Circle(FreeCAD.Vector(0,0,0),FreeCAD.Vector(0,0,1),{r}),0,math.radians({ang})).toShape()"
            )

        desc = f"沿 {path_desc} 扫描 {pr_desc} 截面生成管状特征。"
        code = f"""import FreeCAD, Part, PartDesign, Sketcher, math
doc=FreeCAD.newDocument('Sweep')
body=doc.addObject('PartDesign::Body','Body')
{pr_code}
body.addObject(profile)
{path_code}
sweep=doc.addObject('PartDesign::AdditivePipe','Sweep')
sweep.Profile=profile
sweep.Spine=(path,[])
doc.recompute()"""
        samples.append({"input": desc, "output": code})
    return samples


# ────────────────────────────────────────────
# 5. Loft
# ────────────────────────────────────────────
def generate_loft_samples(num_samples: int = 40):
    samples = []
    for _ in range(num_samples):
        sections = random.choice([2, 3])
        sec_descs, sec_codes = [], []
        z = 0
        for i in range(sections):
            stype = random.choice(['circle', 'polygon'])
            z += random.randint(20, 40)
            if stype == 'circle':
                r = random.randint(10, 30)
                sec_descs.append(f"圆（半径 {r} mm, Z={z} mm）")
                sec_codes.append(
                    f"sk{i}=doc.addObject('Sketcher::SketchObject','Sec{i}')\n"
                    f"sk{i}.Placement.Base.z={z}\n"
                    f"sk{i}.addGeometry(Part.Circle(FreeCAD.Vector(0,0,0),FreeCAD.Vector(0,0,1),{r}),False)\n"
                    "body.addObject(sk{i})".replace("{i}", str(i))
                )
            else:
                n = random.randint(3, 6)
                rad = random.randint(10, 25)
                sec_descs.append(f"{n} 边形（半径 {rad} mm, Z={z} mm）")
                poly = (
                    f"sk{i}=doc.addObject('Sketcher::SketchObject','Sec{i}')\n"
                    f"sk{i}.Placement.Base.z={z}\n"
                    "vs=[]\n"
                    f"for k in range({n}):\n"
                    f"    a=2*math.pi*k/{n}\n"
                    f"    vs.append(FreeCAD.Vector({rad}*math.cos(a),{rad}*math.sin(a),0))\n"
                    f"for k in range({n}):\n"
                    f"    sk{i}.addGeometry(Part.LineSegment(vs[k],vs[(k+1)%{n}]),False)\n"
                    "body.addObject(sk{i})"
                )
                sec_codes.append(poly)

        desc = "放样特征，截面：" + " → ".join(sec_descs) + "。"
        code_lines = [
            "import FreeCAD, Part, PartDesign, Sketcher, math",
            "doc=FreeCAD.newDocument('Loft')",
            "body=doc.addObject('PartDesign::Body','Body')",
            *sec_codes,
            "loft=doc.addObject('PartDesign::AdditiveLoft','Loft')",
            f"loft.Sections={[f'sk{i}' for i in range(sections)]}".replace("'", ""),
            "doc.recompute()"
        ]
        samples.append({"input": desc, "output": "\n".join(code_lines)})
    return samples


# ────────────────────────────────────────────
# 6. Fillet / Chamfer
# ────────────────────────────────────────────
def generate_fillet_chamfer_samples(num_samples: int,
                                    fillet_only: bool = False,
                                    chamfer_only: bool = False):
    samples = []
    for _ in range(num_samples):
        ftype = 'fillet' if fillet_only else ('chamfer' if chamfer_only else random.choice(['fillet','chamfer']))
        L, W, H = (random.randint(40, 100) for _ in range(3))
        size = random.randint(2, 10)
        desc_base = f"长方体（{L}×{W}×{H} mm）"

        head = f"""import FreeCAD, Part, PartDesign, Sketcher
doc=FreeCAD.newDocument('{ftype.capitalize()}')
body=doc.addObject('PartDesign::Body','Body')
sk=doc.addObject('Sketcher::SketchObject','Sketch')
sk.addGeometry(Part.LineSegment(FreeCAD.Vector(0,0,0),FreeCAD.Vector({L},0,0)),False)
sk.addGeometry(Part.LineSegment(FreeCAD.Vector({L},0,0),FreeCAD.Vector({L},{W},0)),False)
sk.addGeometry(Part.LineSegment(FreeCAD.Vector({L},{W},0),FreeCAD.Vector(0,{W},0)),False)
sk.addGeometry(Part.LineSegment(FreeCAD.Vector(0,{W},0),FreeCAD.Vector(0,0,0)),False)
body.addObject(sk)
pad=doc.addObject('PartDesign::Pad','Pad')
pad.Profile=sk
pad.Length={H}
doc.recompute()"""

        if ftype == 'fillet':
            desc = f"对 {desc_base} 所有边做半径 {size} mm 的圆角。"
            op = (f"fil=doc.addObject('PartDesign::Fillet','Fillet')\n"
                  f"fil.Base=pad\nfil.Radius={size}\nfil.Edges=[(pad,'Edge*')]\n"
                  "doc.recompute()")
        else:
            desc = f"对 {desc_base} 所有边做 {size} mm 倒角。"
            op = (f"ch=doc.addObject('PartDesign::Chamfer','Chamfer')\n"
                  f"ch.Base=pad\nch.Size={size}\nch.Edges=[(pad,'Edge*')]\n"
                  "doc.recompute()")
        samples.append({"input": desc, "output": head + "\n" + op})
    return samples


# ────────────────────────────────────────────
# 7. Pattern / Mirror
# ────────────────────────────────────────────
def generate_pattern_samples(num_samples: int = 15):
    samples = []
    for _ in range(num_samples):
        p_type = random.choice(['linear', 'polar', 'mirror'])
        L = random.randint(10, 30)
        head = f"""import FreeCAD, Part, PartDesign, Sketcher
doc=FreeCAD.newDocument('Pattern')
body=doc.addObject('PartDesign::Body','Body')
sk=doc.addObject('Sketcher::SketchObject','Sketch')
sk.addGeometry(Part.LineSegment(FreeCAD.Vector(0,0,0),FreeCAD.Vector({L},0,0)),False)
sk.addGeometry(Part.LineSegment(FreeCAD.Vector({L},0,0),FreeCAD.Vector({L},{L},0)),False)
sk.addGeometry(Part.LineSegment(FreeCAD.Vector({L},{L},0),FreeCAD.Vector(0,{L},0)),False)
sk.addGeometry(Part.LineSegment(FreeCAD.Vector(0,{L},0),FreeCAD.Vector(0,0,0)),False)
body.addObject(sk)
pad=doc.addObject('PartDesign::Pad','Pad')
pad.Profile=sk
pad.Length={L}
doc.recompute()"""

        if p_type == 'linear':
            occ, step = random.randint(2,5), random.randint(20,40)
            desc = f"将正方 Pad 进行 X 方向线性阵列（数量 {occ}，间距 {step} mm）。"
            op = (f"pat=doc.addObject('PartDesign::LinearPattern','Pattern')\n"
                  f"pat.Originals=[pad]\npat.Direction=(1,0,0)\n"
                  f"pat.Occurrences={occ}\npat.Interval={step}\n"
                  "doc.recompute()")
        elif p_type == 'polar':
            occ, rad = random.randint(4,8), random.randint(30,60)
            desc = f"将正方 Pad 进行圆周阵列（数量 {occ}，半径 {rad} mm）。"
            op = (f"pat=doc.addObject('PartDesign::PolarPattern','Pattern')\n"
                  f"pat.Originals=[pad]\npat.Occurrences={occ}\npat.Angle=360\n"
                  f"pat.Axis=(0,0,1)\npat.ReferencePoint=FreeCAD.Vector({rad},0,0)\n"
                  "doc.recompute()")
        else:
            desc = "将正方 Pad 以 YZ 平面镜像。"
            op = ("mir=doc.addObject('PartDesign::Mirrored','Mirror')\n"
                  "mir.Originals=[pad]\nmir.MirrorPlane=(doc.getObject('YZ_Plane'))\n"
                  "doc.recompute()")

        samples.append({"input": desc, "output": head + "\n" + op})
    return samples


# ────────────────────────────────────────────
# 8. 汇总 & 保存
# ────────────────────────────────────────────
def generate_all_feature_modeling_samples():
    samples = (
        generate_pad_samples(60) +
        generate_revolve_samples(50) +
        generate_pocket_samples(50) +
        generate_sweep_samples(40) +
        generate_loft_samples(40) +
        generate_fillet_chamfer_samples(30, fillet_only=True) +
        generate_fillet_chamfer_samples(15, chamfer_only=True) +
        generate_pattern_samples(15)
    )
    assert len(samples) == 300

    out_path = Path("../freecad_samples")
    out_path.mkdir(parents=True, exist_ok=True)
    out_file = out_path / "category5_feature_modeling.json"
    out_file.write_text(json.dumps(samples, ensure_ascii=False, indent=2), encoding="utf-8")
    return len(samples)


if __name__ == "__main__":
    total = generate_all_feature_modeling_samples()
    print(f"已生成 {total} 条特征建模样本，文件存储于 ../freecad_samples/category5_feature_modeling.json")
