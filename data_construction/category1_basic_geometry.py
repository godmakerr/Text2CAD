"""
生成基本几何体创建（Part工作台）的FreeCAD Python脚本样本
包括：立方体/长方体(Box)、圆柱(Cylinder)、圆锥(Cone)、球体(Sphere)、圆环(Torus)等
"""
import json
import random

def generate_box_samples(num_samples=60):
    samples = []
    for _ in range(num_samples):
        length = random.randint(10, 200)
        width = random.randint(10, 200)
        height = random.randint(10, 200)
        
        # 随机决定是否添加位置信息
        has_position = random.choice([True, False])
        if has_position:
            x = random.randint(-100, 100)
            y = random.randint(-100, 100)
            z = random.randint(-100, 100)
            position_text = f"，位置在坐标({x}, {y}, {z})"
            position_code = f"\nbox.Placement.Base = FreeCAD.Vector({x}, {y}, {z})"
        else:
            position_text = ""
            position_code = ""
        
        # 随机决定是否添加旋转信息
        has_rotation = random.choice([True, False])
        if has_rotation:
            axis_x = random.uniform(-1, 1)
            axis_y = random.uniform(-1, 1)
            axis_z = random.uniform(-1, 1)
            angle = random.randint(0, 360)
            rotation_text = f"，绕轴({axis_x:.2f}, {axis_y:.2f}, {axis_z:.2f})旋转{angle}度"
            rotation_code = f"\nbox.Placement.Rotation = FreeCAD.Rotation(FreeCAD.Vector({axis_x:.2f}, {axis_y:.2f}, {axis_z:.2f}), {angle})"
        else:
            rotation_text = ""
            rotation_code = ""
        
        # 生成描述和代码
        description = f"创建一个{length}mm长、{width}mm宽、{height}mm高的长方体{position_text}{rotation_text}。"
        
        code = f"import FreeCAD, Part\ndoc = FreeCAD.newDocument(\"Box\")\nbox = doc.addObject(\"Part::Box\", \"Box\")\nbox.Length = {length}\nbox.Width = {width}\nbox.Height = {height}{position_code}{rotation_code}\ndoc.recompute()"
        
        samples.append({
            "input": description,
            "output": code
        })
    
    return samples

def generate_cylinder_samples(num_samples=60):
    samples = []
    for _ in range(num_samples):
        radius = random.randint(5, 100)
        height = random.randint(10, 200)
        
        # 随机决定是否使用直径而非半径描述
        use_diameter = random.choice([True, False])
        if use_diameter:
            size_text = f"{radius*2}mm直径"
        else:
            size_text = f"{radius}mm半径"
        
        # 随机决定是否添加位置信息
        has_position = random.choice([True, False])
        if has_position:
            x = random.randint(-100, 100)
            y = random.randint(-100, 100)
            z = random.randint(-100, 100)
            position_text = f"，位置在坐标({x}, {y}, {z})"
            position_code = f"\ncylinder.Placement.Base = FreeCAD.Vector({x}, {y}, {z})"
        else:
            position_text = ""
            position_code = ""
        
        # 随机决定是否添加旋转信息
        has_rotation = random.choice([True, False])
        if has_rotation:
            axis_x = random.uniform(-1, 1)
            axis_y = random.uniform(-1, 1)
            axis_z = random.uniform(-1, 1)
            angle = random.randint(0, 360)
            rotation_text = f"，绕轴({axis_x:.2f}, {axis_y:.2f}, {axis_z:.2f})旋转{angle}度"
            rotation_code = f"\ncylinder.Placement.Rotation = FreeCAD.Rotation(FreeCAD.Vector({axis_x:.2f}, {axis_y:.2f}, {axis_z:.2f}), {angle})"
        else:
            rotation_text = ""
            rotation_code = ""
        
        # 生成描述和代码
        description = f"创建一个{size_text}、{height}mm高的圆柱体{position_text}{rotation_text}。"
        
        code = f"import FreeCAD, Part\ndoc = FreeCAD.newDocument(\"Cylinder\")\ncylinder = doc.addObject(\"Part::Cylinder\", \"Cylinder\")\ncylinder.Radius = {radius}\ncylinder.Height = {height}{position_code}{rotation_code}\ndoc.recompute()"
        
        samples.append({
            "input": description,
            "output": code
        })
    
    return samples

def generate_cone_samples(num_samples=60):
    samples = []
    for _ in range(num_samples):
        radius1 = random.randint(5, 100)
        radius2 = random.randint(0, radius1-1) if random.random() > 0.3 else 0  # 30%概率生成标准圆锥
        height = random.randint(10, 200)
        
        # 随机决定是否使用直径而非半径描述
        use_diameter = random.choice([True, False])
        if use_diameter:
            if radius2 == 0:
                size_text = f"{radius1*2}mm底面直径"
            else:
                size_text = f"底面直径{radius1*2}mm、顶面直径{radius2*2}mm"
        else:
            if radius2 == 0:
                size_text = f"{radius1}mm底面半径"
            else:
                size_text = f"底面半径{radius1}mm、顶面半径{radius2}mm"
        
        # 随机决定是否添加位置信息
        has_position = random.choice([True, False])
        if has_position:
            x = random.randint(-100, 100)
            y = random.randint(-100, 100)
            z = random.randint(-100, 100)
            position_text = f"，位置在坐标({x}, {y}, {z})"
            position_code = f"\ncone.Placement.Base = FreeCAD.Vector({x}, {y}, {z})"
        else:
            position_text = ""
            position_code = ""
        
        # 随机决定是否添加旋转信息
        has_rotation = random.choice([True, False])
        if has_rotation:
            axis_x = random.uniform(-1, 1)
            axis_y = random.uniform(-1, 1)
            axis_z = random.uniform(-1, 1)
            angle = random.randint(0, 360)
            rotation_text = f"，绕轴({axis_x:.2f}, {axis_y:.2f}, {axis_z:.2f})旋转{angle}度"
            rotation_code = f"\ncone.Placement.Rotation = FreeCAD.Rotation(FreeCAD.Vector({axis_x:.2f}, {axis_y:.2f}, {axis_z:.2f}), {angle})"
        else:
            rotation_text = ""
            rotation_code = ""
        
        # 生成描述和代码
        if radius2 == 0:
            description = f"创建一个{size_text}、{height}mm高的圆锥体{position_text}{rotation_text}。"
        else:
            description = f"创建一个{size_text}、{height}mm高的圆台{position_text}{rotation_text}。"
        
        code = f"import FreeCAD, Part\ndoc = FreeCAD.newDocument(\"Cone\")\ncone = doc.addObject(\"Part::Cone\", \"Cone\")\ncone.Radius1 = {radius1}\ncone.Radius2 = {radius2}\ncone.Height = {height}{position_code}{rotation_code}\ndoc.recompute()"
        
        samples.append({
            "input": description,
            "output": code
        })
    
    return samples

def generate_sphere_samples(num_samples=40):
    samples = []
    for _ in range(num_samples):
        radius = random.randint(5, 100)
        
        # 随机决定是否使用直径而非半径描述
        use_diameter = random.choice([True, False])
        if use_diameter:
            size_text = f"{radius*2}mm直径"
        else:
            size_text = f"{radius}mm半径"
        
        # 随机决定是否添加位置信息
        has_position = random.choice([True, False])
        if has_position:
            x = random.randint(-100, 100)
            y = random.randint(-100, 100)
            z = random.randint(-100, 100)
            position_text = f"，中心位置在坐标({x}, {y}, {z})"
            position_code = f"\nsphere.Placement.Base = FreeCAD.Vector({x}, {y}, {z})"
        else:
            position_text = ""
            position_code = ""
        
        # 生成描述和代码
        description = f"创建一个{size_text}的球体{position_text}。"
        
        code = f"import FreeCAD, Part\ndoc = FreeCAD.newDocument(\"Sphere\")\nsphere = doc.addObject(\"Part::Sphere\", \"Sphere\")\nsphere.Radius = {radius}{position_code}\ndoc.recompute()"
        
        samples.append({
            "input": description,
            "output": code
        })
    
    return samples

def generate_torus_samples(num_samples=40):
    samples = []
    for _ in range(num_samples):
        radius1 = random.randint(20, 150)  # 主半径
        radius2 = random.randint(5, min(radius1//2, 50))  # 管半径
        
        # 随机决定是否使用直径而非半径描述
        use_diameter = random.choice([True, False])
        if use_diameter:
            size_text = f"主直径{radius1*2}mm、管直径{radius2*2}mm"
        else:
            size_text = f"主半径{radius1}mm、管半径{radius2}mm"
        
        # 随机决定是否添加位置信息
        has_position = random.choice([True, False])
        if has_position:
            x = random.randint(-100, 100)
            y = random.randint(-100, 100)
            z = random.randint(-100, 100)
            position_text = f"，中心位置在坐标({x}, {y}, {z})"
            position_code = f"\ntorus.Placement.Base = FreeCAD.Vector({x}, {y}, {z})"
        else:
            position_text = ""
            position_code = ""
        
        # 随机决定是否添加旋转信息
        has_rotation = random.choice([True, False])
        if has_rotation:
            axis_x = random.uniform(-1, 1)
            axis_y = random.uniform(-1, 1)
            axis_z = random.uniform(-1, 1)
            angle = random.randint(0, 360)
            rotation_text = f"，绕轴({axis_x:.2f}, {axis_y:.2f}, {axis_z:.2f})旋转{angle}度"
            rotation_code = f"\ntorus.Placement.Rotation = FreeCAD.Rotation(FreeCAD.Vector({axis_x:.2f}, {axis_y:.2f}, {axis_z:.2f}), {angle})"
        else:
            rotation_text = ""
            rotation_code = ""
        
        # 生成描述和代码
        description = f"创建一个{size_text}的圆环{position_text}{rotation_text}。"
        
        code = f"import FreeCAD, Part\ndoc = FreeCAD.newDocument(\"Torus\")\ntorus = doc.addObject(\"Part::Torus\", \"Torus\")\ntorus.Radius1 = {radius1}\ntorus.Radius2 = {radius2}{position_code}{rotation_code}\ndoc.recompute()"
        
        samples.append({
            "input": description,
            "output": code
        })
    
    return samples

def generate_prism_samples(num_samples=40):
    samples = []
    for _ in range(num_samples):
        sides = random.randint(3, 12)
        radius = random.randint(10, 100)
        height = random.randint(10, 200)
        
        # 随机决定是否添加位置信息
        has_position = random.choice([True, False])
        if has_position:
            x = random.randint(-100, 100)
            y = random.randint(-100, 100)
            z = random.randint(-100, 100)
            position_text = f"，位置在坐标({x}, {y}, {z})"
            position_code = f"\nprism.Placement.Base = FreeCAD.Vector({x}, {y}, {z})"
        else:
            position_text = ""
            position_code = ""
        
        # 随机决定是否添加旋转信息
        has_rotation = random.choice([True, False])
        if has_rotation:
            axis_x = random.uniform(-1, 1)
            axis_y = random.uniform(-1, 1)
            axis_z = random.uniform(-1, 1)
            angle = random.randint(0, 360)
            rotation_text = f"，绕轴({axis_x:.2f}, {axis_y:.2f}, {axis_z:.2f})旋转{angle}度"
            rotation_code = f"\nprism.Placement.Rotation = FreeCAD.Rotation(FreeCAD.Vector({axis_x:.2f}, {axis_y:.2f}, {axis_z:.2f}), {angle})"
        else:
            rotation_text = ""
            rotation_code = ""
        
        # 生成描述和代码
        description = f"创建一个{sides}边形棱柱，底面外接圆半径{radius}mm，高度{height}mm{position_text}{rotation_text}。"
        
        code = f"import FreeCAD, Part\ndoc = FreeCAD.newDocument(\"Prism\")\nprism = doc.addObject(\"Part::Prism\", \"Prism\")\nprism.Polygon = {sides}\nprism.Circumradius = {radius}\nprism.Height = {height}{position_code}{rotation_code}\ndoc.recompute()"
        
        samples.append({
            "input": description,
            "output": code
        })
    
    return samples

def generate_wedge_samples(num_samples=40):
    samples = []
    for _ in range(num_samples):
        xmin = random.randint(-50, 0)
        ymin = random.randint(-50, 0)
        zmin = random.randint(-50, 0)
        x2min = random.randint(-50, 0)
        z2min = random.randint(-50, 0)
        xmax = random.randint(10, 100)
        ymax = random.randint(10, 100)
        zmax = random.randint(10, 100)
        x2max = random.randint(10, 100)
        z2max = random.randint(10, 100)
        
        # 随机决定是否添加位置信息
        has_position = random.choice([True, False])
        if has_position:
            x = random.randint(-100, 100)
            y = random.randint(-100, 100)
            z = random.randint(-100, 100)
            position_text = f"，位置在坐标({x}, {y}, {z})"
            position_code = f"\nwedge.Placement.Base = FreeCAD.Vector({x}, {y}, {z})"
        else:
            position_text = ""
            position_code = ""
        
        # 生成描述和代码
        description = f"创建一个楔形，X范围[{xmin},{xmax}]mm，Y范围[{ymin},{ymax}]mm，Z范围[{zmin},{zmax}]mm，X2范围[{x2min},{x2max}]mm，Z2范围[{z2min},{z2max}]mm{position_text}。"
        
        code = f"import FreeCAD, Part\ndoc = FreeCAD.newDocument(\"Wedge\")\nwedge = doc.addObject(\"Part::Wedge\", \"Wedge\")\nwedge.Xmin = {xmin}\nwedge.Ymin = {ymin}\nwedge.Zmin = {zmin}\nwedge.X2min = {x2min}\nwedge.Z2min = {z2min}\nwedge.Xmax = {xmax}\nwedge.Ymax = {ymax}\nwedge.Zmax = {zmax}\nwedge.X2max = {x2max}\nwedge.Z2max = {z2max}{position_code}\ndoc.recompute()"
        
        samples.append({
            "input": description,
            "output": code
        })
    
    return samples

def generate_all_basic_geometry_samples():
    # 生成各类基本几何体样本
    box_samples = generate_box_samples(60)
    cylinder_samples = generate_cylinder_samples(60)
    cone_samples = generate_cone_samples(60)
    sphere_samples = generate_sphere_samples(40)
    torus_samples = generate_torus_samples(40)
    prism_samples = generate_prism_samples(40)
    wedge_samples = generate_wedge_samples(40)
    
    # 合并所有样本
    all_samples = box_samples + cylinder_samples + cone_samples + sphere_samples + torus_samples + prism_samples + wedge_samples
    
    # 确保样本数量为300
    if len(all_samples) > 300:
        all_samples = all_samples[:300]
    
    # 保存到JSON文件
    with open('../freecad_samples/category1_basic_geometry.json', 'w', encoding='utf-8') as f:
        json.dump(all_samples, f, ensure_ascii=False, indent=2)
    
    return len(all_samples)

if __name__ == "__main__":
    count = generate_all_basic_geometry_samples()
    print(f"已生成{count}条基本几何体创建样本")
