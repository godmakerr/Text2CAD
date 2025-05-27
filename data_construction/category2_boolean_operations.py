"""
生成布尔运算（Part 工作台）的 FreeCAD Python 脚本样本
包括：并集 (Fuse / Union)、差集 (Cut / Subtract)、交集 (Common / Intersect)、
以及 2–3 步混合布尔操作。
"""
import json
import random
from pathlib import Path

# —————————————————————————————————————
# 1. 并集 (Fuse) ————————————————————
# —————————————————————————————————————
def generate_fuse_samples(num_samples: int = 100):
    samples = []
    for _ in range(num_samples):
        # 随机选两种形体
        shapes = random.sample(['Box', 'Cylinder', 'Cone', 'Sphere', 'Torus'], 2)
        shape1, shape2 = shapes

        # ——— 形体 1 ———
        if shape1 == 'Box':
            l1, w1, h1 = [random.randint(20, 150) for _ in range(3)]
            p1 = f"长{l1} mm、宽{w1} mm、高{h1} mm的长方体"
            c1 = (f"shape1 = doc.addObject('Part::Box', 'Box')\n"
                  f"shape1.Length = {l1}\nshape1.Width = {w1}\nshape1.Height = {h1}")
        elif shape1 == 'Cylinder':
            r1, h1 = random.randint(10, 70), random.randint(20, 150)
            p1 = f"半径{r1} mm、高{h1} mm的圆柱体"
            c1 = (f"shape1 = doc.addObject('Part::Cylinder', 'Cylinder')\n"
                  f"shape1.Radius = {r1}\nshape1.Height = {h1}")
        elif shape1 == 'Cone':
            r1, h1 = random.randint(10, 70), random.randint(20, 150)
            p1 = f"底面半径{r1} mm、高{h1} mm的圆锥体"
            c1 = (f"shape1 = doc.addObject('Part::Cone', 'Cone')\n"
                  f"shape1.Radius1 = {r1}\nshape1.Radius2 = 0\nshape1.Height = {h1}")
        elif shape1 == 'Sphere':
            r1 = random.randint(10, 70)
            p1 = f"半径{r1} mm的球体"
            c1 = (f"shape1 = doc.addObject('Part::Sphere', 'Sphere')\n"
                  f"shape1.Radius = {r1}")
        else:  # Torus
            r1_1 = random.randint(30, 100)
            r1_2 = random.randint(5, 20)
            p1 = f"主半径{r1_1} mm、管半径{r1_2} mm的圆环"
            c1 = (f"shape1 = doc.addObject('Part::Torus', 'Torus')\n"
                  f"shape1.Radius1 = {r1_1}\nshape1.Radius2 = {r1_2}")

        # ——— 形体 2 ———
        if shape2 == 'Box':
            l2, w2, h2 = [random.randint(20, 150) for _ in range(3)]
            p2 = f"长{l2} mm、宽{w2} mm、高{h2} mm的长方体"
            c2 = (f"shape2 = doc.addObject('Part::Box', 'Box2')\n"
                  f"shape2.Length = {l2}\nshape2.Width = {w2}\nshape2.Height = {h2}")
        elif shape2 == 'Cylinder':
            r2, h2 = random.randint(10, 70), random.randint(20, 150)
            p2 = f"半径{r2} mm、高{h2} mm的圆柱体"
            c2 = (f"shape2 = doc.addObject('Part::Cylinder', 'Cylinder2')\n"
                  f"shape2.Radius = {r2}\nshape2.Height = {h2}")
        elif shape2 == 'Cone':
            r2, h2 = random.randint(10, 70), random.randint(20, 150)
            p2 = f"底面半径{r2} mm、高{h2} mm的圆锥体"
            c2 = (f"shape2 = doc.addObject('Part::Cone', 'Cone2')\n"
                  f"shape2.Radius1 = {r2}\nshape2.Radius2 = 0\nshape2.Height = {h2}")
        elif shape2 == 'Sphere':
            r2 = random.randint(10, 70)
            p2 = f"半径{r2} mm的球体"
            c2 = (f"shape2 = doc.addObject('Part::Sphere', 'Sphere2')\n"
                  f"shape2.Radius = {r2}")
        else:  # Torus
            r2_1 = random.randint(30, 100)
            r2_2 = random.randint(5, 20)
            p2 = f"主半径{r2_1} mm、管半径{r2_2} mm的圆环"
            c2 = (f"shape2 = doc.addObject('Part::Torus', 'Torus2')\n"
                  f"shape2.Radius1 = {r2_1}\nshape2.Radius2 = {r2_2}")

        # ——— 形体 2 的位置 / 旋转 ———
        x2, y2, z2 = [random.randint(-50, 50) for _ in range(3)]
        pos_txt = f"位置在({x2}, {y2}, {z2})"
        pos_code = f"shape2.Placement.Base = FreeCAD.Vector({x2}, {y2}, {z2})"
        if random.choice([True, False]):
            ax, ay, az = [random.uniform(-1, 1) for _ in range(3)]
            ang = random.randint(0, 360)
            rot_txt = f"，并绕轴({ax:.2f}, {ay:.2f}, {az:.2f})旋转{ang}°"
            rot_code = f"\nshape2.Placement.Rotation = FreeCAD.Rotation(FreeCAD.Vector({ax:.2f}, {ay:.2f}, {az:.2f}), {ang})"
        else:
            rot_txt, rot_code = "", ""

        union_word = random.choice(["并集", "合并", "融合", "组合"])
        description = (
            f"创建一个{p1}和一个{p2}（{pos_txt}{rot_txt}），然后计算它们的{union_word}。"
        )
        code = (
            "import FreeCAD, Part\n"
            "doc = FreeCAD.newDocument('Fusion')\n"
            f"{c1}\n{c2}\n{pos_code}{rot_code}\n"
            "fusion = doc.addObject('Part::Fuse', 'Fusion')\n"
            "fusion.Base = shape1\nfusion.Tool = shape2\n"
            "doc.recompute()"
        )
        samples.append({"input": description, "output": code})
    return samples


# —————————————————————————————————————
# 2. 差集 (Cut) ————————————————————
# —————————————————————————————————————
def generate_cut_samples(num_samples: int = 100):
    samples = []
    for _ in range(num_samples):
        base_shape = random.choice(['Box', 'Cylinder', 'Sphere', 'Torus'])
        tool_shape = random.choice(['Box', 'Cylinder', 'Cone', 'Sphere'])

        # ——— 基体 ———
        if base_shape == 'Box':
            l, w, h = [random.randint(50, 200) for _ in range(3)]
            p1 = f"长{l} mm、宽{w} mm、高{h} mm的长方体"
            c1 = (f"base = doc.addObject('Part::Box', 'Base')\n"
                  f"base.Length = {l}\nbase.Width = {w}\nbase.Height = {h}")
            x2 = random.randint(0, l // 2)
            y2 = random.randint(0, w // 2)
            z2 = random.randint(0, h // 2)
        elif base_shape == 'Cylinder':
            r, h = random.randint(30, 100), random.randint(50, 200)
            p1 = f"半径{r} mm、高{h} mm的圆柱体"
            c1 = (f"base = doc.addObject('Part::Cylinder', 'Base')\n"
                  f"base.Radius = {r}\nbase.Height = {h}")
            x2, y2 = [random.randint(-r // 2, r // 2) for _ in range(2)]
            z2 = random.randint(0, h // 2)
        elif base_shape == 'Sphere':
            r = random.randint(50, 100)
            p1 = f"半径{r} mm的球体"
            c1 = (f"base = doc.addObject('Part::Sphere', 'Base')\n"
                  f"base.Radius = {r}")
            lim = int(r * 0.7)
            x2, y2, z2 = [random.randint(-lim, lim) for _ in range(3)]
        else:  # Torus
            r1 = random.randint(50, 120)
            r2 = random.randint(10, 30)
            p1 = f"主半径{r1} mm、管半径{r2} mm的圆环"
            c1 = (f"base = doc.addObject('Part::Torus', 'Base')\n"
                  f"base.Radius1 = {r1}\nbase.Radius2 = {r2}")
            x2 = random.randint(-20, 20)
            y2 = random.randint(-20, 20)
            z2 = random.randint(-r2, r2)

        # ——— 减体 ———
        if tool_shape == 'Box':
            l2, w2, h2 = [random.randint(20, 100) for _ in range(3)]
            p2 = f"长{l2} mm、宽{w2} mm、高{h2} mm的长方体"
            c2 = (f"tool = doc.addObject('Part::Box', 'Tool')\n"
                  f"tool.Length = {l2}\ntool.Width = {w2}\ntool.Height = {h2}")
        elif tool_shape == 'Cylinder':
            r2, h2 = random.randint(10, 50), random.randint(50, 250)
            p2 = f"半径{r2} mm、高{h2} mm的圆柱体"
            c2 = (f"tool = doc.addObject('Part::Cylinder', 'Tool')\n"
                  f"tool.Radius = {r2}\ntool.Height = {h2}")
        elif tool_shape == 'Cone':
            r2, h2 = random.randint(10, 50), random.randint(50, 150)
            p2 = f"底面半径{r2} mm、高{h2} mm的圆锥体"
            c2 = (f"tool = doc.addObject('Part::Cone', 'Tool')\n"
                  f"tool.Radius1 = {r2}\ntool.Radius2 = 0\ntool.Height = {h2}")
        else:  # Sphere
            r2 = random.randint(20, 50)
            p2 = f"半径{r2} mm的球体"
            c2 = (f"tool = doc.addObject('Part::Sphere', 'Tool')\n"
                  f"tool.Radius = {r2}")

        pos_txt = f"位置在({x2}, {y2}, {z2})"
        pos_code = f"tool.Placement.Base = FreeCAD.Vector({x2}, {y2}, {z2})"
        if random.choice([True, False]):
            ax, ay, az = [random.uniform(-1, 1) for _ in range(3)]
            ang = random.randint(0, 360)
            rot_txt = f"，并绕轴({ax:.2f}, {ay:.2f}, {az:.2f})旋转{ang}°"
            rot_code = f"\ntool.Placement.Rotation = FreeCAD.Rotation(FreeCAD.Vector({ax:.2f}, {ay:.2f}, {az:.2f}), {ang})"
        else:
            rot_txt, rot_code = "", ""

        cut_word = random.choice(["差集", "减去", "挖除", "切除", "打孔"])
        description = f"从一个{p1}中{cut_word}一个{p2}（{pos_txt}{rot_txt}）。"
        code = (
            "import FreeCAD, Part\n"
            "doc = FreeCAD.newDocument('Cut')\n"
            f"{c1}\n{c2}\n{pos_code}{rot_code}\n"
            "cut = doc.addObject('Part::Cut', 'Cut')\n"
            "cut.Base = base\ncut.Tool = tool\n"
            "doc.recompute()"
        )
        samples.append({"input": description, "output": code})
    return samples


# —————————————————————————————————————
# 3. 交集 (Common) ———————————————————
# —————————————————————————————————————
def generate_common_samples(num_samples: int = 50):
    samples = []
    for _ in range(num_samples):
        shape1, shape2 = random.sample(['Box', 'Cylinder', 'Sphere', 'Torus'], 2)

        # ——— 形体 1 ———
        if shape1 == 'Box':
            l1, w1, h1 = [random.randint(50, 150) for _ in range(3)]
            p1 = f"长{l1} mm、宽{w1} mm、高{h1} mm的长方体"
            c1 = (f"obj1 = doc.addObject('Part::Box', 'Box1')\n"
                  f"obj1.Length = {l1}\nobj1.Width = {w1}\nobj1.Height = {h1}")
            max_off = min(l1, w1, h1) // 2
            x2, y2, z2 = [random.randint(-max_off, max_off) for _ in range(3)]
        elif shape1 == 'Cylinder':
            r1, h1 = random.randint(30, 80), random.randint(50, 150)
            p1 = f"半径{r1} mm、高{h1} mm的圆柱体"
            c1 = (f"obj1 = doc.addObject('Part::Cylinder', 'Cylinder1')\n"
                  f"obj1.Radius = {r1}\nobj1.Height = {h1}")
            x2, y2 = [random.randint(-r1 // 2, r1 // 2) for _ in range(2)]
            z2 = random.randint(-h1 // 4, h1 // 4)
        elif shape1 == 'Sphere':
            r1 = random.randint(40, 80)
            p1 = f"半径{r1} mm的球体"
            c1 = (f"obj1 = doc.addObject('Part::Sphere', 'Sphere1')\n"
                  f"obj1.Radius = {r1}")
            lim = int(r1 * 0.7)
            x2, y2, z2 = [random.randint(-lim, lim) for _ in range(3)]
        else:  # Torus
            r1_1 = random.randint(50, 100)
            r1_2 = random.randint(10, 30)
            p1 = f"主半径{r1_1} mm、管半径{r1_2} mm的圆环"
            c1 = (f"obj1 = doc.addObject('Part::Torus', 'Torus1')\n"
                  f"obj1.Radius1 = {r1_1}\nobj1.Radius2 = {r1_2}")
            x2 = random.randint(-r1_1 // 2, r1_1 // 2)
            y2 = random.randint(-r1_1 // 2, r1_1 // 2)
            z2 = random.randint(-r1_2, r1_2)

        # ——— 形体 2 ———
        if shape2 == 'Box':
            l2, w2, h2 = [random.randint(50, 150) for _ in range(3)]
            p2 = f"长{l2} mm、宽{w2} mm、高{h2} mm的长方体"
            c2 = (f"obj2 = doc.addObject('Part::Box', 'Box2')\n"
                  f"obj2.Length = {l2}\nobj2.Width = {w2}\nobj2.Height = {h2}")
        elif shape2 == 'Cylinder':
            r2, h2 = random.randint(30, 80), random.randint(50, 150)
            p2 = f"半径{r2} mm、高{h2} mm的圆柱体"
            c2 = (f"obj2 = doc.addObject('Part::Cylinder', 'Cylinder2')\n"
                  f"obj2.Radius = {r2}\nobj2.Height = {h2}")
        elif shape2 == 'Sphere':
            r2 = random.randint(40, 80)
            p2 = f"半径{r2} mm的球体"
            c2 = (f"obj2 = doc.addObject('Part::Sphere', 'Sphere2')\n"
                  f"obj2.Radius = {r2}")
        else:  # Torus
            r2_1 = random.randint(50, 100)
            r2_2 = random.randint(10, 30)
            p2 = f"主半径{r2_1} mm、管半径{r2_2} mm的圆环"
            c2 = (f"obj2 = doc.addObject('Part::Torus', 'Torus2')\n"
                  f"obj2.Radius1 = {r2_1}\nobj2.Radius2 = {r2_2}")

        pos_txt = f"位置在({x2}, {y2}, {z2})"
        pos_code = f"obj2.Placement.Base = FreeCAD.Vector({x2}, {y2}, {z2})"
        if random.choice([True, False]):
            ax, ay, az = [random.uniform(-1, 1) for _ in range(3)]
            ang = random.randint(0, 360)
            rot_txt = f"，并绕轴({ax:.2f}, {ay:.2f}, {az:.2f})旋转{ang}°"
            rot_code = f"\nobj2.Placement.Rotation = FreeCAD.Rotation(FreeCAD.Vector({ax:.2f}, {ay:.2f}, {az:.2f}), {ang})"
        else:
            rot_txt, rot_code = "", ""

        common_word = random.choice(["交集", "相交部分", "重叠部分", "共同部分"])
        description = f"计算一个{p1}和一个{p2}（{pos_txt}{rot_txt}）的{common_word}。"
        code = (
            "import FreeCAD, Part\n"
            "doc = FreeCAD.newDocument('Common')\n"
            f"{c1}\n{c2}\n{pos_code}{rot_code}\n"
            "common = doc.addObject('Part::Common', 'Common')\n"
            "common.Base = obj1\ncommon.Tool = obj2\n"
            "doc.recompute()"
        )
        samples.append({"input": description, "output": code})
    return samples


# —————————————————————————————————————
# 4. 多体布尔组合 (2–3 步) ——————————
# —————————————————————————————————————
def generate_multi_boolean_samples(num_samples: int = 50):
    """
    随机执行 2–3 次 Fuse/Cut/Common，得到连锁布尔操作示例。
    """
    samples = []
    synonyms = {
        'Fuse': ["并集", "合并", "融合", "组合"],
        'Cut': ["差集", "减去", "切除", "打孔"],
        'Common': ["交集", "相交部分", "重叠部分", "共同部分"]
    }

    for _ in range(num_samples):
        steps = random.randint(2, 3)
        operations = random.choices(['Fuse', 'Cut', 'Common'], k=steps)

        # ——— 基体 ———
        base_shape = random.choice(['Box', 'Cylinder', 'Sphere'])
        if base_shape == 'Box':
            l, w, h = [random.randint(50, 150) for _ in range(3)]
            base_param = f"长{l} mm、宽{w} mm、高{h} mm的长方体"
            base_code = (f"base = doc.addObject('Part::Box', 'Base')\n"
                         f"base.Length = {l}\nbase.Width = {w}\nbase.Height = {h}")
        elif base_shape == 'Cylinder':
            r, h = random.randint(40, 100), random.randint(50, 200)
            base_param = f"半径{r} mm、高{h} mm的圆柱体"
            base_code = (f"base = doc.addObject('Part::Cylinder', 'Base')\n"
                         f"base.Radius = {r}\nbase.Height = {h}")
        else:  # Sphere
            r = random.randint(50, 100)
            base_param = f"半径{r} mm的球体"
            base_code = (f"base = doc.addObject('Part::Sphere', 'Base')\n"
                         f"base.Radius = {r}")

        description_parts = [f"创建一个{base_param}作为基体"]
        code_lines = ["import FreeCAD, Part",
                      "doc = FreeCAD.newDocument('MultiBoolean')",
                      base_code]
        current_base_var = "base"

        # ——— 连锁操作 ———
        for idx, op in enumerate(operations, start=1):
            tool_var = f"tool{idx}"
            # 形体类型
            tool_shape = random.choice(['Box', 'Cylinder', 'Cone', 'Sphere', 'Torus'])
            if tool_shape == 'Box':
                l, w, h = [random.randint(20, 120) for _ in range(3)]
                tool_param = f"长{l} mm、宽{w} mm、高{h} mm的长方体"
                tool_code = (f"{tool_var} = doc.addObject('Part::Box', '{tool_var.capitalize()}')\n"
                             f"{tool_var}.Length = {l}\n{tool_var}.Width = {w}\n{tool_var}.Height = {h}")
            elif tool_shape == 'Cylinder':
                r, h = random.randint(10, 70), random.randint(20, 150)
                tool_param = f"半径{r} mm、高{h} mm的圆柱体"
                tool_code = (f"{tool_var} = doc.addObject('Part::Cylinder', '{tool_var.capitalize()}')\n"
                             f"{tool_var}.Radius = {r}\n{tool_var}.Height = {h}")
            elif tool_shape == 'Cone':
                r, h = random.randint(10, 70), random.randint(20, 150)
                tool_param = f"底面半径{r} mm、高{h} mm的圆锥体"
                tool_code = (f"{tool_var} = doc.addObject('Part::Cone', '{tool_var.capitalize()}')\n"
                             f"{tool_var}.Radius1 = {r}\n{tool_var}.Radius2 = 0\n{tool_var}.Height = {h}")
            elif tool_shape == 'Sphere':
                r = random.randint(10, 70)
                tool_param = f"半径{r} mm的球体"
                tool_code = (f"{tool_var} = doc.addObject('Part::Sphere', '{tool_var.capitalize()}')\n"
                             f"{tool_var}.Radius = {r}")
            else:  # Torus
                r1 = random.randint(30, 100)
                r2 = random.randint(5, 25)
                tool_param = f"主半径{r1} mm、管半径{r2} mm的圆环"
                tool_code = (f"{tool_var} = doc.addObject('Part::Torus', '{tool_var.capitalize()}')\n"
                             f"{tool_var}.Radius1 = {r1}\n{tool_var}.Radius2 = {r2}")

            # 位置 & 旋转
            x, y, z = [random.randint(-60, 60) for _ in range(3)]
            pos_txt = f"位置在({x}, {y}, {z})"
            pos_code = f"{tool_var}.Placement.Base = FreeCAD.Vector({x}, {y}, {z})"
            if random.choice([True, False]):
                ax, ay, az = [random.uniform(-1, 1) for _ in range(3)]
                ang = random.randint(0, 360)
                rot_txt = f"，并绕轴({ax:.2f}, {ay:.2f}, {az:.2f})旋转{ang}°"
                rot_code = f"\n{tool_var}.Placement.Rotation = FreeCAD.Rotation(FreeCAD.Vector({ax:.2f}, {ay:.2f}, {az:.2f}), {ang})"
            else:
                rot_txt, rot_code = "", ""

            # 描述 & 代码
            op_word = random.choice(synonyms[op])
            description_parts.append(f"{op_word}一个{tool_param}（{pos_txt}{rot_txt}）")
            code_lines.extend([tool_code, pos_code + rot_code])

            result_var = f"res{idx}"
            op_class = {'Fuse': 'Part::Fuse', 'Cut': 'Part::Cut', 'Common': 'Part::Common'}[op]
            code_lines.append(f"{result_var} = doc.addObject('{op_class}', 'Result{idx}')")
            code_lines.append(f"{result_var}.Base = {current_base_var}")
            code_lines.append(f"{result_var}.Tool = {tool_var}")
            code_lines.append("doc.recompute()")

            # 下一步基体
            current_base_var = result_var

        full_description = "，然后".join(description_parts) + "。"
        full_code = "\n".join(code_lines)
        samples.append({"input": full_description, "output": full_code})

    return samples


# —————————————————————————————————————
# 5. 汇总 & 保存 ———————————————————
# —————————————————————————————————————
def generate_all_boolean_operation_samples():
    fuse_samples = generate_fuse_samples(100)
    cut_samples = generate_cut_samples(100)
    common_samples = generate_common_samples(50)
    multi_samples = generate_multi_boolean_samples(50)

    all_samples = fuse_samples + cut_samples + common_samples + multi_samples
    if len(all_samples) > 300:
        all_samples = all_samples[:300]

    out_dir = Path("../freecad_samples")
    out_dir.mkdir(parents=True, exist_ok=True)
    out_file = out_dir / "category2_boolean_operations.json"
    with out_file.open("w", encoding="utf-8") as f:
        json.dump(all_samples, f, ensure_ascii=False, indent=2)

    return len(all_samples)


if __name__ == "__main__":
    count = generate_all_boolean_operation_samples()
    print(f"已生成 {count} 条布尔运算样本并保存到 'category2_boolean_operations.json'")
