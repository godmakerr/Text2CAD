"""
合并所有类别的FreeCAD Python脚本样本到一个JSON文件
"""
import json
import os

def merge_json_files():
    # 定义要合并的文件列表
    json_files = [
        '../freecad_samples/category1_basic_geometry.json',
        '../freecad_samples/category2_boolean_operations.json',
        '../freecad_samples/category3_sketch_drawing.json',
        '../freecad_samples/category4_sketch_constraints.json',
        '../freecad_samples/category5_feature_modeling.json'
    ]
    
    # 存储所有样本
    all_samples = []
    
    # 读取并合并所有JSON文件
    for file_path in json_files:
        with open(file_path, 'r', encoding='utf-8') as f:
            samples = json.load(f)
            all_samples.extend(samples)
    
    # 打印每个类别的样本数量
    print(f"类别1（基本几何体创建）: {len(json.load(open(json_files[0], 'r', encoding='utf-8')))}")
    print(f"类别2（布尔运算）: {len(json.load(open(json_files[1], 'r', encoding='utf-8')))}")
    print(f"类别3（草图绘制）: {len(json.load(open(json_files[2], 'r', encoding='utf-8')))}")
    print(f"类别4（草图约束）: {len(json.load(open(json_files[3], 'r', encoding='utf-8')))}")
    print(f"类别5（特征建模操作）: {len(json.load(open(json_files[4], 'r', encoding='utf-8')))}")
    print(f"总样本数: {len(all_samples)}")
    
    # 将合并后的样本保存到新文件
    output_file = '../freecad_samples/freecad_all_samples.json'
    with open(output_file, 'w', encoding='utf-8') as f:
        json.dump(all_samples, f, ensure_ascii=False, indent=2)
    
    print(f"已将所有样本合并到: {output_file}")
    return output_file, len(all_samples)

if __name__ == "__main__":
    output_file, total_samples = merge_json_files()
