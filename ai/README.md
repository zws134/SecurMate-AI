# AI 检测模块（周伟森负责）

## 当前状态

✅ `detect_demo.py` —— 反诈检测最小 Demo（中期检查的 AI 环节基础）

## 快速运行

### 1. 安装 Ollama

- 下载：https://ollama.com/download （Windows 安装包，装完默认自启）

### 2. 拉取中文模型（二选一）

```bash
ollama pull qwen2.5:3b   # 小模型，普通电脑能跑，约 2GB（推荐先用这个）
ollama pull qwen2.5:7b   # 效果更好，需 8GB+ 内存
```

> 如果用 7b，记得改 `detect_demo.py` 里的 `MODEL_NAME = "qwen2.5:7b"`

### 3. 安装 Python 依赖并运行

```bash
pip install requests
python detect_demo.py
```

- 直接回车：跑 5 条内置测试样本（诈骗短信、假客服、假冒熟人等）
- 输入任意文本：检测你输入的内容
- 输出：是否诈骗 + 诈骗类型 + 风险等级 + 判断理由（JSON）

## 后续计划

| 阶段 | 内容 |
|------|------|
| 中期检查前 | 本 Demo 接入后端 `/detect` 接口，跑通全链路 |
| 寒假前 | 加 RAG：检索反诈案例库，让判断"附依据" |
| 2027 春 | 用积累的数据集 + LoRA 微调反诈专用小模型 |
