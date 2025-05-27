import json
import random

# 读取原始数据
with open('../freecad_samples/freecad_all_samples_with_instruction.json', 'r', encoding='utf-8') as f:
    data = json.load(f)

train_set = []
test_set = []

chunk_size = 300
test_per_chunk = 6

# 每 300 条为一组处理
for i in range(0, len(data), chunk_size):
    chunk = data[i:i + chunk_size]
    if len(chunk) < test_per_chunk:
        train_set.extend(chunk)
        continue

    test_indices = set(random.sample(range(len(chunk)), test_per_chunk))
    for idx, item in enumerate(chunk):
        if idx in test_indices:
            test_set.append(item)
        else:
            train_set.append(item)

# 保存为 JSON 文件
with open('../final_data/train.json', 'w', encoding='utf-8') as f:
    json.dump(train_set, f, ensure_ascii=False, indent=2)

with open('../final_data/test.json', 'w', encoding='utf-8') as f:
    json.dump(test_set, f, ensure_ascii=False, indent=2)

print(f"✅ Finished: {len(train_set)} train samples, {len(test_set)} test samples.")
