import json
instruction = "你是一位 CAD 代码专家，根据以下自然语言描述生成可运行的 FreeCAD Python 脚本，创建 2D 或 3D 几何形状。脚本要求：1. 仅导入 FreeCAD 和 Part；2. 创建新文档；3. 使用合适的 Part 模块对象（如 Part::Box、Part::Cylinder、Part::Torus 等）构建描述的形状；4. 设置毫米单位；5. 调用 doc.recompute()；6. 脚本需完整正确，放在最后。简要推理尺寸和位置（100 字内），输出脚本在‘```python\n...\n```’中。示例：描述‘100mm长50mm宽的矩形’推理‘2D 矩形，尺寸明确’后输出‘```python\nimport FreeCAD, Part\ndoc = FreeCAD.newDocument(\"Rect\")\nrect = doc.addObject(\"Part::Box\", \"Rect\")\nrect.Length = 100\nrect.Width = 50\nrect.Height = 0\ndoc.recompute()\n```’。"
with open('../freecad_samples/freecad_all_samples.json', 'r', encoding='utf-8') as f:
    data = json.load(f)
new_data = []
for item in data:
    new_data.append({
        'instruction': instruction,
        'input': item['input'],
        'output': item['output'],
    })
with open('../freecad_samples/freecad_all_samples_with_instruction.json', 'w', encoding='utf-8') as f:
    json.dump(new_data, f, ensure_ascii=False, indent=2)
print(f"✅ 已为 {len(data)} 条样本添加指令。")