"""
生成草图绘制（Sketcher工作台）的FreeCAD Python脚本样本
包括：直线(Line)、矩形、多段折线(PolyLine)、圆(Circle)、弧(Arc)、多边形等
"""
import json
import random
import math

def generate_line_samples(num_samples=60):
    samples = []
    for _ in range(num_samples):
        # 随机生成两个点的坐标
        x1 = random.randint(-50, 50)
        y1 = random.randint(-50, 50)
        x2 = random.randint(-50, 50)
        y2 = random.randint(-50, 50)
        
        # 计算线段长度
        length = round(math.sqrt((x2-x1)**2 + (y2-y1)**2), 2)
        
        # 随机决定描述方式
        desc_type = random.choice(['points', 'length_angle'])
        
        if desc_type == 'points':
            description = f"在草图中绘制一条从点({x1}, {y1})到点({x2}, {y2})的直线。"
        else:
            # 计算角度（相对于水平线）
            angle = round(math.degrees(math.atan2(y2-y1, x2-x1)), 1)
            if angle < 0:
                angle += 360
            description = f"在草图中绘制一条长度为{length}mm、角度为{angle}度的直线，起点在({x1}, {y1})。"
        
        # 生成代码
        code = f"""import FreeCAD, Part, Sketcher
doc = FreeCAD.newDocument("Line")
sketch = doc.addObject('Sketcher::SketchObject', 'Sketch')
line = Part.LineSegment(FreeCAD.Vector({x1}, {y1}, 0), FreeCAD.Vector({x2}, {y2}, 0))
sketch.addGeometry(line, False)
doc.recompute()"""
        
        samples.append({
            "input": description,
            "output": code
        })
    
    return samples

def generate_rectangle_samples(num_samples=50):
    samples = []
    for _ in range(num_samples):
        # 随机决定矩形的描述方式
        desc_type = random.choice(['center_size', 'corner_size', 'two_points'])
        
        if desc_type == 'center_size':
            # 中心点和尺寸
            center_x = random.randint(-30, 30)
            center_y = random.randint(-30, 30)
            width = random.randint(10, 100)
            height = random.randint(10, 100)
            
            # 计算四个角点
            x1 = center_x - width/2
            y1 = center_y - height/2
            x2 = center_x + width/2
            y2 = center_y + height/2
            
            description = f"在草图中绘制一个中心点在({center_x}, {center_y})、宽{width}mm、高{height}mm的矩形。"
        
        elif desc_type == 'corner_size':
            # 左下角点和尺寸
            x1 = random.randint(-50, 30)
            y1 = random.randint(-50, 30)
            width = random.randint(10, 100)
            height = random.randint(10, 100)
            
            # 计算其他角点
            x2 = x1 + width
            y2 = y1 + height
            
            description = f"在草图中绘制一个左下角在点({x1}, {y1})、宽{width}mm、高{height}mm的矩形。"
        
        else:  # two_points
            # 对角两点
            x1 = random.randint(-50, 30)
            y1 = random.randint(-50, 30)
            x2 = random.randint(x1+10, x1+100)
            y2 = random.randint(y1+10, y1+100)
            
            # 计算宽高
            width = x2 - x1
            height = y2 - y1
            
            description = f"在草图中绘制一个对角点分别为({x1}, {y1})和({x2}, {y2})的矩形。"
        
        # 生成代码
        code = f"""import FreeCAD, Part, Sketcher
doc = FreeCAD.newDocument("Rectangle")
sketch = doc.addObject('Sketcher::SketchObject', 'Sketch')
# 绘制矩形的四条边
line1 = Part.LineSegment(FreeCAD.Vector({x1}, {y1}, 0), FreeCAD.Vector({x2}, {y1}, 0))
line2 = Part.LineSegment(FreeCAD.Vector({x2}, {y1}, 0), FreeCAD.Vector({x2}, {y2}, 0))
line3 = Part.LineSegment(FreeCAD.Vector({x2}, {y2}, 0), FreeCAD.Vector({x1}, {y2}, 0))
line4 = Part.LineSegment(FreeCAD.Vector({x1}, {y2}, 0), FreeCAD.Vector({x1}, {y1}, 0))
sketch.addGeometry(line1, False)
sketch.addGeometry(line2, False)
sketch.addGeometry(line3, False)
sketch.addGeometry(line4, False)
doc.recompute()"""
        
        samples.append({
            "input": description,
            "output": code
        })
    
    return samples

def generate_polyline_samples(num_samples=50):
    samples = []
    for _ in range(num_samples):
        # 随机决定折线的点数
        num_points = random.randint(3, 8)
        
        # 生成点列表
        points = []
        for i in range(num_points):
            x = random.randint(-50, 50)
            y = random.randint(-50, 50)
            points.append((x, y))
        
        # 随机决定是否闭合
        is_closed = random.choice([True, False])
        
        # 生成描述
        points_text = ", ".join([f"({x}, {y})" for x, y in points])
        closed_text = "闭合" if is_closed else "开放"
        description = f"在草图中绘制一条经过点{points_text}的{closed_text}折线。"
        
        # 生成代码
        code_lines = [
            "import FreeCAD, Part, Sketcher",
            "doc = FreeCAD.newDocument(\"PolyLine\")",
            "sketch = doc.addObject('Sketcher::SketchObject', 'Sketch')"
        ]
        
        # 添加线段
        for i in range(len(points) - 1):
            x1, y1 = points[i]
            x2, y2 = points[i+1]
            code_lines.append(f"line{i+1} = Part.LineSegment(FreeCAD.Vector({x1}, {y1}, 0), FreeCAD.Vector({x2}, {y2}, 0))")
            code_lines.append(f"sketch.addGeometry(line{i+1}, False)")
        
        # 如果闭合，添加最后一条线段
        if is_closed:
            x1, y1 = points[-1]
            x2, y2 = points[0]
            code_lines.append(f"line{len(points)} = Part.LineSegment(FreeCAD.Vector({x1}, {y1}, 0), FreeCAD.Vector({x2}, {y2}, 0))")
            code_lines.append(f"sketch.addGeometry(line{len(points)}, False)")
        
        code_lines.append("doc.recompute()")
        code = "\n".join(code_lines)
        
        samples.append({
            "input": description,
            "output": code
        })
    
    return samples

def generate_circle_samples(num_samples=50):
    samples = []
    for _ in range(num_samples):
        # 随机决定圆的描述方式
        desc_type = random.choice(['center_radius', 'center_diameter', 'three_points'])
        
        if desc_type in ['center_radius', 'center_diameter']:
            # 中心点和半径
            center_x = random.randint(-40, 40)
            center_y = random.randint(-40, 40)
            radius = random.randint(5, 50)
            
            if desc_type == 'center_radius':
                description = f"在草图中绘制一个中心点在({center_x}, {center_y})、半径为{radius}mm的圆。"
            else:
                description = f"在草图中绘制一个中心点在({center_x}, {center_y})、直径为{radius*2}mm的圆。"
            
            # 生成代码
            code = f"""import FreeCAD, Part, Sketcher
doc = FreeCAD.newDocument("Circle")
sketch = doc.addObject('Sketcher::SketchObject', 'Sketch')
circle = Part.Circle(FreeCAD.Vector({center_x}, {center_y}, 0), FreeCAD.Vector(0, 0, 1), {radius})
sketch.addGeometry(circle, False)
doc.recompute()"""
        
        else:  # three_points
            # 生成三个点，确保不共线
            while True:
                x1 = random.randint(-50, 50)
                y1 = random.randint(-50, 50)
                x2 = random.randint(-50, 50)
                y2 = random.randint(-50, 50)
                x3 = random.randint(-50, 50)
                y3 = random.randint(-50, 50)
                
                # 检查三点是否共线
                area = abs((x1*(y2-y3) + x2*(y3-y1) + x3*(y1-y2))/2)
                if area > 10:  # 面积足够大，说明不共线
                    break
            
            description = f"在草图中绘制一个经过点({x1}, {y1})、({x2}, {y2})和({x3}, {y3})的圆。"
            
            # 生成代码
            code = f"""import FreeCAD, Part, Sketcher
doc = FreeCAD.newDocument("Circle")
sketch = doc.addObject('Sketcher::SketchObject', 'Sketch')
# 通过三点创建圆
p1 = FreeCAD.Vector({x1}, {y1}, 0)
p2 = FreeCAD.Vector({x2}, {y2}, 0)
p3 = FreeCAD.Vector({x3}, {y3}, 0)
# 计算圆心和半径
ma = (p2.y - p1.y) / (p2.x - p1.x) if p2.x != p1.x else float('inf')
mb = (p3.y - p2.y) / (p3.x - p2.x) if p3.x != p2.x else float('inf')
center_x = (ma * mb * (p1.y - p3.y) + mb * (p1.x + p2.x) - ma * (p2.x + p3.x)) / (2 * (mb - ma)) if ma != mb else 0
center_y = (-1 / ma) * (center_x - (p1.x + p2.x) / 2) + (p1.y + p2.y) / 2 if ma != float('inf') else (p2.y + p3.y) / 2
center = FreeCAD.Vector(center_x, center_y, 0)
radius = center.sub(p1).Length
circle = Part.Circle(center, FreeCAD.Vector(0, 0, 1), radius)
sketch.addGeometry(circle, False)
doc.recompute()"""
        
        samples.append({
            "input": description,
            "output": code
        })
    
    return samples

def generate_arc_samples(num_samples=50):
    samples = []
    for _ in range(num_samples):
        # 随机决定弧的描述方式
        desc_type = random.choice(['center_radius_angles', 'three_points'])
        
        if desc_type == 'center_radius_angles':
            # 中心点、半径和角度
            center_x = random.randint(-40, 40)
            center_y = random.randint(-40, 40)
            radius = random.randint(10, 50)
            start_angle = random.randint(0, 330)
            end_angle = start_angle + random.randint(30, 330)
            if end_angle >= 360:
                end_angle = end_angle % 360
                if end_angle <= start_angle:
                    end_angle = start_angle + 30
            
            # 计算起点和终点
            start_x = center_x + radius * math.cos(math.radians(start_angle))
            start_y = center_y + radius * math.sin(math.radians(start_angle))
            end_x = center_x + radius * math.cos(math.radians(end_angle))
            end_y = center_y + radius * math.sin(math.radians(end_angle))
            
            description = f"在草图中绘制一个中心点在({center_x}, {center_y})、半径为{radius}mm、起始角度{start_angle}度、终止角度{end_angle}度的圆弧。"
            
            # 生成代码
            code = f"""import FreeCAD, Part, Sketcher
doc = FreeCAD.newDocument("Arc")
sketch = doc.addObject('Sketcher::SketchObject', 'Sketch')
center = FreeCAD.Vector({center_x}, {center_y}, 0)
start = FreeCAD.Vector({start_x:.2f}, {start_y:.2f}, 0)
end = FreeCAD.Vector({end_x:.2f}, {end_y:.2f}, 0)
arc = Part.ArcOfCircle(Part.Circle(center, FreeCAD.Vector(0, 0, 1), {radius}), math.radians({start_angle}), math.radians({end_angle}))
sketch.addGeometry(arc, False)
doc.recompute()"""
        
        else:  # three_points
            # 生成三个点，确保不共线
            while True:
                x1 = random.randint(-50, 50)
                y1 = random.randint(-50, 50)
                x2 = random.randint(-50, 50)
                y2 = random.randint(-50, 50)
                x3 = random.randint(-50, 50)
                y3 = random.randint(-50, 50)
                
                # 检查三点是否共线
                area = abs((x1*(y2-y3) + x2*(y3-y1) + x3*(y1-y2))/2)
                if area > 10:  # 面积足够大，说明不共线
                    break
            
            description = f"在草图中绘制一个起点为({x1}, {y1})、经过点({x2}, {y2})、终点为({x3}, {y3})的圆弧。"
            
            # 生成代码
            code = f"""import FreeCAD, Part, Sketcher, math
doc = FreeCAD.newDocument("Arc")
sketch = doc.addObject('Sketcher::SketchObject', 'Sketch')
# 通过三点创建圆弧
p1 = FreeCAD.Vector({x1}, {y1}, 0)  # 起点
p2 = FreeCAD.Vector({x2}, {y2}, 0)  # 中间点
p3 = FreeCAD.Vector({x3}, {y3}, 0)  # 终点
# 计算圆心和半径
ma = (p2.y - p1.y) / (p2.x - p1.x) if p2.x != p1.x else float('inf')
mb = (p3.y - p2.y) / (p3.x - p2.x) if p3.x != p2.x else float('inf')
center_x = (ma * mb * (p1.y - p3.y) + mb * (p1.x + p2.x) - ma * (p2.x + p3.x)) / (2 * (mb - ma)) if ma != mb else 0
center_y = (-1 / ma) * (center_x - (p1.x + p2.x) / 2) + (p1.y + p2.y) / 2 if ma != float('inf') else (p2.y + p3.y) / 2
center = FreeCAD.Vector(center_x, center_y, 0)
radius = center.sub(p1).Length
# 计算角度
v1 = p1.sub(center)
v3 = p3.sub(center)
start_angle = math.atan2(v1.y, v1.x)
end_angle = math.atan2(v3.y, v3.x)
arc = Part.ArcOfCircle(Part.Circle(center, FreeCAD.Vector(0, 0, 1), radius), start_angle, end_angle)
sketch.addGeometry(arc, False)
doc.recompute()"""
        
        samples.append({
            "input": description,
            "output": code
        })
    
    return samples

def generate_polygon_samples(num_samples=40):
    samples = []
    for _ in range(num_samples):
        # 随机决定多边形的边数
        sides = random.randint(3, 10)
        
        # 随机决定多边形的描述方式
        desc_type = random.choice(['center_radius', 'vertices'])
        
        if desc_type == 'center_radius':
            # 中心点和外接圆半径
            center_x = random.randint(-30, 30)
            center_y = random.randint(-30, 30)
            radius = random.randint(10, 50)
            
            description = f"在草图中绘制一个中心点在({center_x}, {center_y})、外接圆半径为{radius}mm的正{sides}边形。"
            
            # 生成代码
            code_lines = [
                "import FreeCAD, Part, Sketcher, math",
                "doc = FreeCAD.newDocument(\"Polygon\")",
                "sketch = doc.addObject('Sketcher::SketchObject', 'Sketch')",
                f"# 绘制正{sides}边形",
                f"center = FreeCAD.Vector({center_x}, {center_y}, 0)",
                f"radius = {radius}",
                f"sides = {sides}",
                "# 计算各个顶点",
                "vertices = []",
                "for i in range(sides):",
                "    angle = 2 * math.pi * i / sides",
                "    x = center.x + radius * math.cos(angle)",
                "    y = center.y + radius * math.sin(angle)",
                "    vertices.append(FreeCAD.Vector(x, y, 0))",
                "# 添加各边",
                "for i in range(sides):",
                "    line = Part.LineSegment(vertices[i], vertices[(i+1) % sides])",
                "    sketch.addGeometry(line, False)",
                "doc.recompute()"
            ]
            code = "\n".join(code_lines)
        
        else:  # vertices
            # 生成顶点
            vertices = []
            for i in range(sides):
                angle = 2 * math.pi * i / sides
                x = 30 * math.cos(angle)
                y = 30 * math.sin(angle)
                # 添加一些随机性
                x += random.randint(-5, 5)
                y += random.randint(-5, 5)
                vertices.append((round(x), round(y)))
            
            vertices_text = ", ".join([f"({x}, {y})" for x, y in vertices])
            description = f"在草图中绘制一个顶点依次为{vertices_text}的{sides}边形。"
            
            # 生成代码
            code_lines = [
                "import FreeCAD, Part, Sketcher",
                "doc = FreeCAD.newDocument(\"Polygon\")",
                "sketch = doc.addObject('Sketcher::SketchObject', 'Sketch')",
                "# 顶点坐标"
            ]
            
            for i, (x, y) in enumerate(vertices):
                code_lines.append(f"v{i+1} = FreeCAD.Vector({x}, {y}, 0)")
            
            code_lines.append("# 添加各边")
            for i in range(sides):
                code_lines.append(f"line{i+1} = Part.LineSegment(v{i+1}, v{(i+1) % sides + 1})")
                code_lines.append(f"sketch.addGeometry(line{i+1}, False)")
            
            code_lines.append("doc.recompute()")
            code = "\n".join(code_lines)
        
        samples.append({
            "input": description,
            "output": code
        })
    
    return samples

def generate_all_sketch_drawing_samples():
    # 生成各类草图绘制样本
    line_samples = generate_line_samples(60)
    rectangle_samples = generate_rectangle_samples(50)
    polyline_samples = generate_polyline_samples(50)
    circle_samples = generate_circle_samples(50)
    arc_samples = generate_arc_samples(50)
    polygon_samples = generate_polygon_samples(40)
    
    # 合并所有样本
    all_samples = line_samples + rectangle_samples + polyline_samples + circle_samples + arc_samples + polygon_samples
    
    # 确保样本数量为300
    if len(all_samples) > 300:
        all_samples = all_samples[:300]
    
    # 保存到JSON文件
    with open('../freecad_samples/category3_sketch_drawing.json', 'w', encoding='utf-8') as f:
        json.dump(all_samples, f, ensure_ascii=False, indent=2)
    
    return len(all_samples)

if __name__ == "__main__":
    count = generate_all_sketch_drawing_samples()
    print(f"已生成{count}条草图绘制样本")
