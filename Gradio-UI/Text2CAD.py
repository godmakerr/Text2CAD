# -*- coding: utf-8 -*-
"""
Text ➜ FreeCAD demo (finetuned Qwen3‑4B)
==================================================
最后一个问题：`.STL` 预览未生成，日志提示 *No module named 'torch'*——原因是上一版把整套 UI 脚本当成参数交给 `freecadcmd` 执行，结果 FreeCAD 环境里没有 `torch`。

✅ **修复策略**
----------------
1. **导出 STL** 时不再调用整份 UI，而是用 *一行小脚本*：
   `freecadcmd -c "import FreeCAD,Mesh; ... Mesh.export(...)"`
2. 若系统没有 `freecadcmd`，直接跳过 STL 生成（保持 UI 可用）。
3. 其余逻辑（模型生成、FCStd 下载、日志回显）不变。
"""

import sys
import shutil
import re
import subprocess
from pathlib import Path
from typing import Optional, Tuple

import torch
from transformers import AutoTokenizer, AutoModelForCausalLM, GenerationConfig
import gradio as gr

# --------------------------------------------------
# Config
# --------------------------------------------------
ROOT = Path(__file__).resolve().parent
MODEL_DIR = Path("/root/autodl-tmp/LLaMA-Factory/saves/train_1").resolve()

DEVICE = "cuda" if torch.cuda.is_available() else "cpu"
DTYPE = torch.float16 if DEVICE == "cuda" else torch.float32

# --------------------------------------------------------------------
# Prompt template (与 JSONL 数据集一致)
# --------------------------------------------------------------------
STOP_WORDS = ["<|im_end|>"]

def build_standard_prompt(description: str) -> str:
    return (
        f"<|im_start|>user\n你是一位 CAD 代码专家，根据以下自然语言描述生成可运行的 FreeCAD Python 脚本，创建 2D 或 3D 几何形状。脚本要求：1. 导入 FreeCAD支持的合适的包；2. 创建新文档；3. 使用合适的 Part 模块对象（如 Part::Box、Part::Cylinder、Part::Torus 等）构建描述的形状；4. 设置毫米单位；5. 调用 doc.recompute()；6. 脚本需完整正确，放在最后。简要推理尺寸和位置（100 字内），输出脚本在‘```python\n...\n```’中。示例：描述‘100mm长50mm宽的矩形’推理‘2D 矩形，尺寸明确’后输出‘```python\nimport FreeCAD, Part\ndoc = FreeCAD.newDocument(\"Rect\")\nrect = doc.addObject(\"Part::Box\", \"Rect\")\nrect.Length = 100\nrect.Width = 50\nrect.Height = 0\ndoc.recompute()\n```’。\n{description.strip()}<|im_end|>\n<|im_start|>assistant\n"
    )

# 自动追加 saveAs 的片段
SAVE_STUB = """
# 自动保存 .FCStd 供后续预览 / 下载
import os
_out = os.path.join(os.path.dirname(__file__), "model.FCStd")
try:
    doc.saveAs(_out)
except Exception as _e:
    print('Skip saveAs:', _e)
"""

# --------------------------------------------------------------------
# Load model（全局只初始化一次）
# --------------------------------------------------------------------

def load_model():
    tok = AutoTokenizer.from_pretrained(str(MODEL_DIR), trust_remote_code=True)
    model = AutoModelForCausalLM.from_pretrained(
        str(MODEL_DIR),
        torch_dtype=DTYPE,
        device_map="auto" if DEVICE == "cuda" else None,
        trust_remote_code=True,
    )
    model.generation_config = GenerationConfig(max_new_tokens=1024, do_sample=False)
    return tok, model

TOKENIZER, MODEL = load_model()

# --------------------------------------------------------------------
# Helpers
# --------------------------------------------------------------------

def extract_python_block(text: str) -> str:
    m = re.search(r"```python\s*(.*?)```", text, re.S)
    return m.group(1).strip() if m else text.strip()


def _freecadcmd() -> Optional[str]:
    """Path to freecadcmd / FreeCADCmd if available."""
    for cmd in ("freecadcmd", "FreeCADCmd"):
        path = shutil.which(cmd)
        if path:
            return path
    return None


# --------------------------------------------------------------------
# LLM → FreeCAD script
# --------------------------------------------------------------------

def text_to_freecad_script(nl_description: str) -> str:
    prompt = build_standard_prompt(nl_description)
    inputs = TOKENIZER(prompt, return_tensors="pt").to(DEVICE)
    with torch.no_grad():
        output_ids = MODEL.generate(**inputs, generation_config=MODEL.generation_config)[0]
    full_output = TOKENIZER.decode(output_ids, skip_special_tokens=False)
    assistant_part = full_output.split("<|im_start|>assistant\n", 1)[-1]
    for sw in STOP_WORDS:
        assistant_part = assistant_part.split(sw)[0]
    code_block = extract_python_block(assistant_part)

    if "doc.saveAs" not in code_block:
        code_block += SAVE_STUB

    prepend = "import sys\nsys.path.append('/usr/lib/freecad-python3/lib')\n"
    return prepend + code_block

# --------------------------------------------------------------------
# Run FreeCAD script
# --------------------------------------------------------------------

def run_freecad_script(script_code: str) -> Tuple[str, Optional[Path]]:
    if not script_code:
        return "[Error] Empty code", None

    temp_py = ROOT / "gen_freecad_model.py"
    temp_py.write_text(script_code, encoding="utf-8")

    cmd = _freecadcmd() or sys.executable
    result = subprocess.run(
        [cmd, str(temp_py)],
        stdout=subprocess.PIPE,
        stderr=subprocess.STDOUT,
        text=True,
    )
    log = result.stdout

    if result.returncode != 0:
        return f"[Script error]\n{log}", None

    model_file = ROOT / "model.FCStd"
    if not model_file.exists():
        return f"[Error] 脚本执行正常，但未找到 .FCStd。日志:\n{log}", None

    return log, model_file

# --------------------------------------------------------------------
# STL export helper
# --------------------------------------------------------------------

def try_export_stl(model_path: Path) -> Tuple[Optional[Path], str]:
    """Return (stl_path | None, log)."""
    fc_cmd = _freecadcmd()
    if not fc_cmd:
        return None, "freecadcmd 未找到，跳过 STL 导出"

    stl_path = model_path.with_suffix(".stl")
    code = (
        "import FreeCAD, Mesh; doc=FreeCAD.open(r'{}'); "
        "Mesh.export([o for o in doc.Objects], r'{}')".format(model_path, stl_path)
    )
    res = subprocess.run([fc_cmd, "-c", code], stdout=subprocess.PIPE, stderr=subprocess.STDOUT, text=True)
    if res.returncode != 0:
        return None, res.stdout
    return stl_path if stl_path.exists() else None, res.stdout

# --------------------------------------------------------------------
# Gradio pipeline
# --------------------------------------------------------------------

def pipeline(user_text: str):
    code = text_to_freecad_script(user_text)
    log, model_file = run_freecad_script(code)

    if not model_file:
        return f"{code}\n\n# --- 执行日志 ---\n{log}", None, None

    stl_path, stl_log = try_export_stl(model_file)

    return (
        code,  # 生成成功时不回显日志，保持简洁。如需查看可改此行
        str(stl_path) if stl_path else None,
        str(model_file),
    )

# --------------------------------------------------------------------
# Gradio UI
# --------------------------------------------------------------------
with gr.Blocks() as demo:
    gr.Markdown("# Text ➜ FreeCAD (Qwen3‑4B)")
    txt = gr.Textbox(lines=3, placeholder="请输入自然语言 CAD 描述…")
    btn = gr.Button("生成并建模")
    out_code = gr.Code(label="脚本", language="python")
    out_model = gr.Model3D(label="STL 预览")
    out_file = gr.File(label="下载 .FCStd")
    btn.click(pipeline, txt, [out_code, out_model, out_file])

# --------------------------------------------------------------------
# Main
# --------------------------------------------------------------------
if __name__ == "__main__":
    import argparse
    ap = argparse.ArgumentParser()
    ap.add_argument("--host", default="0.0.0.0")
    ap.add_argument("--port", type=int, default=7862)
    ap.add_argument("--share", action="store_true")
    args = ap.parse_args()
    demo.launch(server_name=args.host, server_port=args.port, share=args.share)
