# 2025年春季学期复旦大学计算机图形学`COMP130018.01`课程项目
# Text2CAD

数据集详见：[https://modelscope.cn/datasets/shireshire/freecad_data](https://modelscope.cn/datasets/shireshire/freecad_data)

模型详见：[https://modelscope.cn/models/shireshire/Qwen3-4B-FreeCAD](https://modelscope.cn/models/shireshire/Qwen3-4B-FreeCAD)

接下来是我们的具体流程：
## 1. 数据构建
我们为不同类型数据写了数据构建代码
`cd data_construction`，查看`readme.md`并运行数据构建脚本。
## 2. 模型训练
我们使用开源[LLaMA-Factory](https://llamafactory.readthedocs.io/zh-cn/latest/index.html)进行模型训练，请先进入链接下载所需的依赖。
请使用[modelscope](https://modelscope.cn/models/Qwen/Qwen3-4B)下载Qwen3-4B模型，并将`LLaMA-Factory/examples/train_full/train_qwen3_4b.yaml`中的模型路径换成你的。

`cd LLaMA-Factory`，运行`llamafactory-cli train examples/train_full/train_qwen3_4b.yaml`开始训练。

## 3. 用户交互
运行`python Gradio-UI/Text2CAD.py`以启动后台Gradio程序，在浏览器中输入http://localhost:7861/  进入Gradio界面 

在输入框中输入自然语言描述，点击“生成并建模”即可开始推理，等待一段时间后会展示出从自然语言得到的CAD代码，渲染出的STL预览以及供下载的FCStd文件
