# SecurMate —— 端云协同智能安全防护助手

一个本地运行、保护隐私、AI 驱动的个人反诈与安全防护智能助手。

## 项目简介

敏感数据全程在端侧（本地）处理，云端仅做轻量辅助（风险库更新、模型迭代文件推送），从架构上杜绝隐私泄露，解决传统纯云端方案"隐私差、成本高、断网就废"的痛点。

## 技术栈

- 前端：Vue 3 + Element Plus
- 后端：Python + FastAPI
- AI 检测：Ollama（本地大模型）+ Prompt + RAG（反诈案例库检索）
- 语音：Whisper（识别）+ TTS（合成）
- 数据库：SQLite（本地）
- 安全：Snort / Suricata

## 团队成员

| 成员 | 角色 |
|------|------|
| 周伟森（组长） | AI 模型 / 数据 |
| 邱添 | 后端 + AI 模型 |
| 许媛琦 | 前端 |
| 刘炎婷 | 端云架构 |
| 叶佳俊 | 渗透测试 |

## 快速开始

> 环境安装和启动步骤，等各自模块跑通后在这里补全。

```bash
# 1. 克隆仓库
git clone https://github.com/zws134/SecurMate-AI.git
cd SecurMate-AI

# 2. 后端（邱添）
cd backend
pip install -r requirements.txt
# 启动命令待补充

# 3. AI 检测（周伟森）
# 先安装 Ollama，再运行 ai/ 下的脚本

# 4. 前端（许媛琦）
cd frontend
npm install
# 启动命令待补充
```

## 目录结构

```
SecurMate-AI/
├── README.md              # 项目说明
├── docs/                  # 项目文档
├── backend/               # 后端（邱添）
│   ├── app/
│   │   ├── main.py        # FastAPI 入口
│   │   ├── api/           # 接口
│   │   └── models/        # 数据模型
│   ├── requirements.txt
│   └── tests/
├── frontend/              # 前端（许媛琦）
│   ├── src/
│   └── package.json
├── ai/                    # AI 模型（周伟森 + 邱添）
│   ├── data/              # 数据集
│   ├── train/             # 训练脚本
│   ├── models/            # 训练好的模型
│   └── quantize/          # 轻量化脚本
├── security/              # 安全测试（叶佳俊）
│   ├── test-cases/        # 测试用例
│   └── rules/             # Snort/Suricata 规则
├── architecture/          # 端云架构（刘炎婷）
│   ├── 架构图.png
│   └── 部署文档.md
└── .gitignore
```

## 贡献规范

- 从 `dev` 拉分支开发，提交 Pull Request
- 提交信息用中文，格式：`feat: 添加xxx功能` / `fix: 修复xxx`
- 每人只改自己负责的目录，跨模块改动先和对应负责人沟通
