"""
生成草图约束（Sketcher 工作台）的 FreeCAD Python 脚本样本
包括：几何约束（重合、平行、垂直、水平、切线等）
      尺寸约束（长度、水平/垂直距离、半径、直径、角度等）
      组合约束（同一草图 2–3 条混合约束）
"""
import json
import random
import math
from pathlib import Path


# ————————————————————————
# 1. 几何约束
# ————————————————————————
def generate_coincident_constraint_samples(num_samples: int = 40):
    """点-点、点-原点、线段端点重合"""
    samples = []
    for _ in range(num_samples):
        x1, y1 = random.randint(-50, 50), random.randint(-50, 50)
        x2, y2 = random.randint(-50, 50), random.randint(-50, 50)
        constraint_type = random.choice(["point_to_point", "point_to_origin", "line_endpoints"])

        if constraint_type == "point_to_point":
            x3, y3 = random.randint(-50, 50), random.randint(-50, 50)
            desc = f"在草图中创建两个点，分别位于({x1}, {y1}) 和 ({x3}, {y3})，然后添加重合约束使它们重合。"
            code = f"""import FreeCAD, Part, Sketcher
doc = FreeCAD.newDocument("Coincident")
sketch = doc.addObject("Sketcher::SketchObject", "Sketch")
l1 = Part.LineSegment(FreeCAD.Vector({x1}, {y1}, 0), FreeCAD.Vector({x1+1}, {y1+1}, 0))
l2 = Part.LineSegment(FreeCAD.Vector({x3}, {y3}, 0), FreeCAD.Vector({x3+1}, {y3+1}, 0))
g1 = sketch.addGeometry(l1, False)
g2 = sketch.addGeometry(l2, False)
sketch.addConstraint(Sketcher.Constraint("Coincident", g1, 1, g2, 1))
doc.recompute()"""
        elif constraint_type == "point_to_origin":
            desc = f"在草图中创建一个位于({x1}, {y1}) 的点，然后添加重合约束使其与原点重合。"
            code = f"""import FreeCAD, Part, Sketcher
doc = FreeCAD.newDocument("Coincident")
sketch = doc.addObject("Sketcher::SketchObject", "Sketch")
l = Part.LineSegment(FreeCAD.Vector({x1}, {y1}, 0), FreeCAD.Vector({x1+1}, {y1+1}, 0))
g = sketch.addGeometry(l, False)
sketch.addConstraint(Sketcher.Constraint("Coincident", g, 1, -1, 1))
doc.recompute()"""
        else:  # line_endpoints
            x3, y3, x4, y4 = (random.randint(-50, 50) for _ in range(4))
            desc = (f"在草图中创建两条线段，一条从({x1}, {y1}) 到 ({x2}, {y2})，"
                    f"另一条从({x3}, {y3}) 到 ({x4}, {y4})，然后添加重合约束使第一条线段的终点与第二条线段的起点重合。")
            code = f"""import FreeCAD, Part, Sketcher
doc = FreeCAD.newDocument("Coincident")
sketch = doc.addObject("Sketcher::SketchObject", "Sketch")
l1 = Part.LineSegment(FreeCAD.Vector({x1}, {y1}, 0), FreeCAD.Vector({x2}, {y2}, 0))
l2 = Part.LineSegment(FreeCAD.Vector({x3}, {y3}, 0), FreeCAD.Vector({x4}, {y4}, 0))
g1 = sketch.addGeometry(l1, False)
g2 = sketch.addGeometry(l2, False)
sketch.addConstraint(Sketcher.Constraint("Coincident", g1, 2, g2, 1))
doc.recompute()"""
        samples.append({"input": desc, "output": code})
    return samples


def generate_parallel_perpendicular_samples(num_samples: int = 40):
    """平行 / 垂直"""
    samples = []
    for _ in range(num_samples):
        pts = [random.randint(-50, 50) for _ in range(8)]
        x1, y1, x2, y2, x3, y3, x4, y4 = pts
        ctype = random.choice(["parallel", "perpendicular"])
        if ctype == "parallel":
            desc = (f"在草图中创建两条线段，一条从({x1}, {y1}) 到 ({x2}, {y2})，"
                    f"另一条从({x3}, {y3}) 到 ({x4}, {y4})，然后添加平行约束使它们平行。")
            cstr = "Parallel"
            doc_name = "Parallel"
        else:
            desc = (f"在草图中创建两条线段，一条从({x1}, {y1}) 到 ({x2}, {y2})，"
                    f"另一条从({x3}, {y3}) 到 ({x4}, {y4})，然后添加垂直约束使它们相互垂直。")
            cstr = "Perpendicular"
            doc_name = "Perpendicular"
        code = f"""import FreeCAD, Part, Sketcher
doc = FreeCAD.newDocument("{doc_name}")
sketch = doc.addObject("Sketcher::SketchObject", "Sketch")
l1 = Part.LineSegment(FreeCAD.Vector({x1}, {y1}, 0), FreeCAD.Vector({x2}, {y2}, 0))
l2 = Part.LineSegment(FreeCAD.Vector({x3}, {y3}, 0), FreeCAD.Vector({x4}, {y4}, 0))
g1 = sketch.addGeometry(l1, False)
g2 = sketch.addGeometry(l2, False)
sketch.addConstraint(Sketcher.Constraint("{cstr}", g1, g2))
doc.recompute()"""
        samples.append({"input": desc, "output": code})
    return samples


def generate_horizontal_vertical_samples(num_samples: int = 40):
    """水平 / 垂直"""
    samples = []
    for _ in range(num_samples):
        x1, y1 = random.randint(-50, 50), random.randint(-50, 50)
        x2, y2 = random.randint(-50, 50), random.randint(-50, 50)
        ctype = random.choice(["horizontal", "vertical"])
        if ctype == "horizontal":
            desc = f"在草图中创建一条从({x1}, {y1}) 到 ({x2}, {y2}) 的线段，然后添加水平约束使其水平。"
            cstr = "Horizontal"
            doc_name = "Horizontal"
        else:
            desc = f"在草图中创建一条从({x1}, {y1}) 到 ({x2}, {y2}) 的线段，然后添加垂直约束使其垂直。"
            cstr = "Vertical"
            doc_name = "Vertical"
        code = f"""import FreeCAD, Part, Sketcher
doc = FreeCAD.newDocument("{doc_name}")
sketch = doc.addObject("Sketcher::SketchObject", "Sketch")
line = Part.LineSegment(FreeCAD.Vector({x1}, {y1}, 0), FreeCAD.Vector({x2}, {y2}, 0))
g = sketch.addGeometry(line, False)
sketch.addConstraint(Sketcher.Constraint("{cstr}", g))
doc.recompute()"""
        samples.append({"input": desc, "output": code})
    return samples


def generate_tangent_samples(num_samples: int = 20):
    """线-圆切 / 圆-圆切"""
    samples = []
    for _ in range(num_samples):
        ttype = random.choice(["line_circle", "circle_circle"])
        if ttype == "line_circle":
            cx, cy = random.randint(-30, 30), random.randint(-30, 30)
            r = random.randint(10, 40)
            ang = random.uniform(0, 2 * math.pi)
            tx, ty = cx + r * math.cos(ang), cy + r * math.sin(ang)
            tang_ang = ang + math.pi / 2
            ex, ey = tx + 30 * math.cos(tang_ang), ty + 30 * math.sin(tang_ang)
            desc = (f"在草图中创建一个中心在({cx}, {cy})、半径为{r} mm的圆，"
                    f"以及一条从({tx:.1f}, {ty:.1f}) 到 ({ex:.1f}, {ey:.1f}) 的线段，"
                    "然后添加切线约束使线段与圆相切。")
            code = f"""import FreeCAD, Part, Sketcher
doc = FreeCAD.newDocument("Tangent")
sketch = doc.addObject("Sketcher::SketchObject", "Sketch")
circle = Part.Circle(FreeCAD.Vector({cx}, {cy}, 0), FreeCAD.Vector(0, 0, 1), {r})
g1 = sketch.addGeometry(circle, False)
line = Part.LineSegment(FreeCAD.Vector({tx:.1f}, {ty:.1f}, 0), FreeCAD.Vector({ex:.1f}, {ey:.1f}, 0))
g2 = sketch.addGeometry(line, False)
sketch.addConstraint(Sketcher.Constraint("Tangent", g1, g2))
doc.recompute()"""
        else:  # circle_circle
            c1x, c1y = random.randint(-40, 0), random.randint(-30, 30)
            r1 = random.randint(10, 30)
            r2 = random.randint(10, 30)
            ang = random.uniform(0, 2 * math.pi)
            dx = (r1 + r2) * math.cos(ang)
            dy = (r1 + r2) * math.sin(ang)
            c2x, c2y = c1x + dx, c1y + dy
            desc = (f"在草图中创建两个圆："
                    f"圆 1 中心({c1x}, {c1y})、半径{r1} mm；"
                    f"圆 2 中心({c2x:.1f}, {c2y:.1f})、半径{r2} mm，"
                    "然后添加切线约束使两圆相切。")
            code = f"""import FreeCAD, Part, Sketcher
doc = FreeCAD.newDocument("Tangent")
sketch = doc.addObject("Sketcher::SketchObject", "Sketch")
c1 = Part.Circle(FreeCAD.Vector({c1x}, {c1y}, 0), FreeCAD.Vector(0, 0, 1), {r1})
c2 = Part.Circle(FreeCAD.Vector({c2x:.1f}, {c2y:.1f}, 0), FreeCAD.Vector(0, 0, 1), {r2})
g1 = sketch.addGeometry(c1, False)
g2 = sketch.addGeometry(c2, False)
sketch.addConstraint(Sketcher.Constraint("Tangent", g1, g2))
doc.recompute()"""
        samples.append({"input": desc, "output": code})
    return samples


# ————————————————————————
# 2. 尺寸约束
# ————————————————————————
def generate_distance_samples(num_samples: int = 40):
    """点-点距离、线段长度、水平 / 垂直距离"""
    samples = []
    for _ in range(num_samples):
        ctype = random.choice(["distance_points", "distance_line", "distance_x", "distance_y"])
        if ctype == "distance_points":
            x1, y1, x2, y2 = (random.randint(-50, 50) for _ in range(4))
            dist = round(math.hypot(x2 - x1, y2 - y1))
            desc = f"在草图中创建两个点 ({x1}, {y1}) 和 ({x2}, {y2})，然后添加距离约束，设置它们之间距离为 {dist} mm。"
            code = f"""import FreeCAD, Part, Sketcher
doc = FreeCAD.newDocument("Distance")
sketch = doc.addObject("Sketcher::SketchObject", "Sketch")
p1 = Part.LineSegment(FreeCAD.Vector({x1}, {y1}, 0), FreeCAD.Vector({x1+1}, {y1+1}, 0))
p2 = Part.LineSegment(FreeCAD.Vector({x2}, {y2}, 0), FreeCAD.Vector({x2+1}, {y2+1}, 0))
g1 = sketch.addGeometry(p1, False)
g2 = sketch.addGeometry(p2, False)
sketch.addConstraint(Sketcher.Constraint("Distance", g1, 1, g2, 1, {dist}))
doc.recompute()"""
        elif ctype == "distance_line":
            x1, y1, x2, y2 = (random.randint(-50, 50) for _ in range(4))
            length = round(math.hypot(x2 - x1, y2 - y1))
            desc = f"在草图中创建一条从({x1}, {y1}) 到 ({x2}, {y2}) 的线段，然后添加长度约束，设置长度为 {length} mm。"
            code = f"""import FreeCAD, Part, Sketcher
doc = FreeCAD.newDocument("Distance")
sketch = doc.addObject("Sketcher::SketchObject", "Sketch")
line = Part.LineSegment(FreeCAD.Vector({x1}, {y1}, 0), FreeCAD.Vector({x2}, {y2}, 0))
g = sketch.addGeometry(line, False)
sketch.addConstraint(Sketcher.Constraint("Distance", g, {length}))
doc.recompute()"""
        elif ctype == "distance_x":
            x1, y1, x2, y2 = (random.randint(-50, 50) for _ in range(4))
            dx = abs(x2 - x1)
            desc = f"在草图中创建两个点 ({x1}, {y1}) 和 ({x2}, {y2})，然后添加水平距离约束，设置 X 方向距离为 {dx} mm。"
            code = f"""import FreeCAD, Part, Sketcher
doc = FreeCAD.newDocument("DistanceX")
sketch = doc.addObject("Sketcher::SketchObject", "Sketch")
p1 = Part.LineSegment(FreeCAD.Vector({x1}, {y1}, 0), FreeCAD.Vector({x1+1}, {y1+1}, 0))
p2 = Part.LineSegment(FreeCAD.Vector({x2}, {y2}, 0), FreeCAD.Vector({x2+1}, {y2+1}, 0))
g1 = sketch.addGeometry(p1, False)
g2 = sketch.addGeometry(p2, False)
sketch.addConstraint(Sketcher.Constraint("DistanceX", g1, 1, g2, 1, {dx}))
doc.recompute()"""
        else:  # distance_y
            x1, y1, x2, y2 = (random.randint(-50, 50) for _ in range(4))
            dy = abs(y2 - y1)
            desc = f"在草图中创建两个点 ({x1}, {y1}) 和 ({x2}, {y2})，然后添加垂直距离约束，设置 Y 方向距离为 {dy} mm。"
            code = f"""import FreeCAD, Part, Sketcher
doc = FreeCAD.newDocument("DistanceY")
sketch = doc.addObject("Sketcher::SketchObject", "Sketch")
p1 = Part.LineSegment(FreeCAD.Vector({x1}, {y1}, 0), FreeCAD.Vector({x1+1}, {y1+1}, 0))
p2 = Part.LineSegment(FreeCAD.Vector({x2}, {y2}, 0), FreeCAD.Vector({x2+1}, {y2+1}, 0))
g1 = sketch.addGeometry(p1, False)
g2 = sketch.addGeometry(p2, False)
sketch.addConstraint(Sketcher.Constraint("DistanceY", g1, 1, g2, 1, {dy}))
doc.recompute()"""
        samples.append({"input": desc, "output": code})
    return samples


def generate_radius_diameter_samples(num_samples: int = 40):
    """半径 / 直径"""
    samples = []
    for _ in range(num_samples):
        cx, cy = random.randint(-40, 40), random.randint(-40, 40)
        r = random.randint(10, 50)
        ctype = random.choice(["radius", "diameter"])
        if ctype == "radius":
            desc = f"在草图中创建一个中心在({cx}, {cy}) 的圆，然后添加半径约束，设置半径为 {r} mm。"
            cstr = "Radius"
            val = r
            doc_name = "Radius"
        else:
            desc = f"在草图中创建一个中心在({cx}, {cy}) 的圆，然后添加直径约束，设置直径为 {2*r} mm。"
            cstr = "Diameter"
            val = 2 * r
            doc_name = "Diameter"
        code = f"""import FreeCAD, Part, Sketcher
doc = FreeCAD.newDocument("{doc_name}")
sketch = doc.addObject("Sketcher::SketchObject", "Sketch")
circle = Part.Circle(FreeCAD.Vector({cx}, {cy}, 0), FreeCAD.Vector(0, 0, 1), {r})
g = sketch.addGeometry(circle, False)
sketch.addConstraint(Sketcher.Constraint("{cstr}", g, {val}))
doc.recompute()"""
        samples.append({"input": desc, "output": code})
    return samples


def generate_angle_samples(num_samples: int = 40):
    """角度"""
    samples = []
    for _ in range(num_samples):
        pts = [random.randint(-50, 50) for _ in range(8)]
        x1, y1, x2, y2, x3, y3, x4, y4 = pts
        ang = random.randint(15, 165)
        desc = (f"在草图中创建两条线段：({x1}, {y1})→({x2}, {y2}) 以及 "
                f"({x3}, {y3})→({x4}, {y4})，然后添加角度约束，设置它们之间夹角为 {ang}°。")
        code = f"""import FreeCAD, Part, Sketcher, math
doc = FreeCAD.newDocument("Angle")
sketch = doc.addObject("Sketcher::SketchObject", "Sketch")
l1 = Part.LineSegment(FreeCAD.Vector({x1}, {y1}, 0), FreeCAD.Vector({x2}, {y2}, 0))
l2 = Part.LineSegment(FreeCAD.Vector({x3}, {y3}, 0), FreeCAD.Vector({x4}, {y4}, 0))
g1 = sketch.addGeometry(l1, False)
g2 = sketch.addGeometry(l2, False)
sketch.addConstraint(Sketcher.Constraint("Angle", g1, g2, math.radians({ang})))
doc.recompute()"""
        samples.append({"input": desc, "output": code})
    return samples


# ————————————————————————
# 3. 组合约束
# ————————————————————————
def generate_combination_samples(num_samples: int = 40):
    """
    在同一草图中随机添加 2–3 条不同类型约束。
    结构：两条线段 + 1 圆，随机组合水平/垂直/平行/垂直/长度/半径/角度等。
    """
    samples = []
    for _ in range(num_samples):
        # 基础几何
        p = [random.randint(-60, 60) for _ in range(6)]
        x1, y1, x2, y2, cx, cy = p
        r = random.randint(15, 40)
        angle_line = random.randint(-30, 30)
        x3 = x1 + 40 * math.cos(math.radians(angle_line))
        y3 = y1 + 40 * math.sin(math.radians(angle_line))
        # 随机约束组合
        comb_options = [
            ("Parallel", "Distance", None),
            ("Perpendicular", "Distance", "Radius"),
            ("Horizontal", "Vertical", "DistanceX"),
            ("Angle", "Radius", None),
            ("Parallel", "DistanceX", "DistanceY"),
        ]
        ops = random.choice(comb_options)
        ops = [o for o in ops if o]  # 去掉 None
        desc_parts = []
        code_lines = [
            "import FreeCAD, Part, Sketcher, math",
            "doc = FreeCAD.newDocument('Combo')",
            "sketch = doc.addObject('Sketcher::SketchObject', 'Sketch')",
            # 线段 1
            f"l1 = Part.LineSegment(FreeCAD.Vector({x1}, {y1}, 0), FreeCAD.Vector({x2}, {y2}, 0))",
            # 线段 2
            f"l2 = Part.LineSegment(FreeCAD.Vector({x1}, {y1}, 0), FreeCAD.Vector({x3:.1f}, {y3:.1f}, 0))",
            # 圆
            f"circle = Part.Circle(FreeCAD.Vector({cx}, {cy}, 0), FreeCAD.Vector(0,0,1), {r})",
            "g1 = sketch.addGeometry(l1, False)",
            "g2 = sketch.addGeometry(l2, False)",
            "g3 = sketch.addGeometry(circle, False)",
        ]

        # 遍历约束
        for op in ops:
            if op == "Parallel":
                desc_parts.append("添加平行约束使两线段平行")
                code_lines.append("sketch.addConstraint(Sketcher.Constraint('Parallel', g1, g2))")
            elif op == "Perpendicular":
                desc_parts.append("添加垂直约束使两线段垂直")
                code_lines.append("sketch.addConstraint(Sketcher.Constraint('Perpendicular', g1, g2))")
            elif op == "Horizontal":
                desc_parts.append("添加水平约束使第一条线段水平")
                code_lines.append("sketch.addConstraint(Sketcher.Constraint('Horizontal', g1))")
            elif op == "Vertical":
                desc_parts.append("添加垂直约束使第二条线段垂直")
                code_lines.append("sketch.addConstraint(Sketcher.Constraint('Vertical', g2))")
            elif op == "Distance":
                length = round(math.hypot(x2 - x1, y2 - y1))
                desc_parts.append(f"添加长度约束，将第一条线段长度设为 {length} mm")
                code_lines.append(f"sketch.addConstraint(Sketcher.Constraint('Distance', g1, {length}))")
            elif op == "DistanceX":
                dx = abs(x2 - x1)
                desc_parts.append(f"添加水平距离约束，将两线段起点 X 方向距离设为 {dx} mm")
                code_lines.append(f"sketch.addConstraint(Sketcher.Constraint('DistanceX', g1, 1, g2, 1, {dx}))")
            elif op == "DistanceY":
                dy = abs(y2 - y1)
                desc_parts.append(f"添加垂直距离约束，将两线段起点 Y 方向距离设为 {dy} mm")
                code_lines.append(f"sketch.addConstraint(Sketcher.Constraint('DistanceY', g1, 1, g2, 1, {dy}))")
            elif op == "Radius":
                desc_parts.append(f"添加半径约束，将圆半径设为 {r} mm")
                code_lines.append(f"sketch.addConstraint(Sketcher.Constraint('Radius', g3, {r}))")
            elif op == "Angle":
                ang = random.randint(20, 160)
                desc_parts.append(f"添加角度约束，将两线段夹角设为 {ang}°")
                code_lines.append(f"sketch.addConstraint(Sketcher.Constraint('Angle', g1, g2, math.radians({ang})))")

        code_lines.append("doc.recompute()")
        desc = "在同一草图中创建两条线段和一个圆，" + "，".join(desc_parts) + "。"
        samples.append({"input": desc, "output": "\n".join(code_lines)})
    return samples


# ————————————————————————
# 4. 汇总并保存
# ————————————————————————
def generate_all_sketch_constraint_samples():
    geo_samples = (
        generate_coincident_constraint_samples(40)
        + generate_parallel_perpendicular_samples(40)
        + generate_horizontal_vertical_samples(40)
        + generate_tangent_samples(20)
    )
    dim_samples = (
        generate_distance_samples(40)
        + generate_radius_diameter_samples(40)
        + generate_angle_samples(40)
    )
    combo_samples = generate_combination_samples(40)

    all_samples = geo_samples + dim_samples + combo_samples
    assert len(all_samples) == 300

    out_dir = Path("../freecad_samples")
    out_dir.mkdir(parents=True, exist_ok=True)
    out_path = out_dir / "category4_sketch_constraints.json"
    with out_path.open("w", encoding="utf-8") as f:
        json.dump(all_samples, f, ensure_ascii=False, indent=2)

    return len(all_samples)


if __name__ == "__main__":
    cnt = generate_all_sketch_constraint_samples()
    print(f"已生成 {cnt} 条草图约束样本并保存到 'category4_sketch_constraints.json'")
