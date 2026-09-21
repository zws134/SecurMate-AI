# -*- coding: utf-8 -*-
"""
SecurMate 反诈检测最小 Demo（Ollama + Prompt）
================================================
作用：输入一段短信/通话文本，调用本地 Ollama 大模型，
     输出【是否诈骗 + 诈骗类型 + 风险等级 + 判断理由】的 JSON。

使用前提：
1. 安装 Ollama：https://ollama.com/download 下载安装
2. 拉取中文模型（任选其一，建议 qwen2.5，对中文反诈场景效果好）：
   ollama pull qwen2.5:3b        # 小模型，普通电脑能跑（约 2GB）
   ollama pull qwen2.5:7b        # 效果更好，需要 8GB+ 内存
3. 确认 Ollama 在运行（安装后默认自启，命令行 ollama list 能看到模型即可）

运行方式：
   python detect_demo.py
   然后按提示输入要检测的文本，或直接用内置测试样本。

作者：周伟森（SecurMate 项目组）
"""

import json
import requests

# ================== 配置区（按需修改） ==================
OLLAMA_URL = "http://localhost:11434/api/chat"   # Ollama 本地服务地址
MODEL_NAME = "qwen2.5:3b"                        # 用的模型，和 ollama pull 的一致

# 系统提示词：这是整个检测的核心，告诉模型怎么判断、输出什么格式
SYSTEM_PROMPT = """你是一个网络安全反诈助手，专门识别针对个人的诈骗信息。

请分析用户给出的短信/通话/消息文本，严格按以下 JSON 格式输出，不要输出任何其他内容：
{
  "is_fraud": true或false,
  "fraud_type": "诈骗类型（如：虚假投资理财/冒充客服/冒充公检法/钓鱼链接/刷单返利/无风险），is_fraud为false时填'无风险'",
  "risk_level": "高/中/低",
  "reason": "50字以内的判断理由，指出文本中的可疑点"
}

判断参考：
- 冒充公检法要求转账、配合调查 → 高风险
- 虚假投资理财、稳赚不赔、内部消息 → 高风险
- 刷单返利、先垫付后返款 → 高风险
- 冒充客服退款、引导点击链接/下载APP → 中高风险
- 中奖通知但要求先交费 → 中风险
- 正常通知、验证码类（用户本人操作） → 低风险/无风险
只输出 JSON，不要输出解释、不要用 markdown 代码块包裹。"""


def detect(text: str) -> dict:
    """调用本地 Ollama 检测一条文本，返回结构化结果"""
    payload = {
        "model": MODEL_NAME,
        "messages": [
            {"role": "system", "content": SYSTEM_PROMPT},
            {"role": "user", "content": f"请检测以下文本：\n{text}"},
        ],
        "stream": False,
        # temperature 调低让输出更稳定；format=json 强制模型输出合法 JSON
        "options": {"temperature": 0.1},
        "format": "json",
    }
    resp = requests.post(OLLAMA_URL, json=payload, timeout=120)
    resp.raise_for_status()
    content = resp.json()["message"]["content"]
    try:
        return json.loads(content)
    except json.JSONDecodeError:
        return {"is_fraud": None, "fraud_type": "解析失败", "risk_level": "未知",
                "reason": f"模型输出不是合法JSON：{content[:100]}"}


def pretty_print(text: str, result: dict):
    """把结果打印成人看得懂的样子"""
    fraud = result.get("is_fraud")
    flag = {True: "🚨 疑似诈骗", False: "✅ 未检出风险", None: "⚠️ 解析异常"}.get(fraud, "⚠️ 未知")
    print("=" * 50)
    print(f"原文：{text[:60]}{'...' if len(text) > 60 else ''}")
    print(f"结论：{flag}")
    print(f"类型：{result.get('fraud_type', '未知')}")
    print(f"等级：{result.get('risk_level', '未知')}")
    print(f"理由：{result.get('reason', '无')}")


# 内置测试样本（也可换成叶佳俊收集的真实诈骗样本）
TEST_SAMPLES = [
    "【平安金融】尊敬的用户，您有一笔50000元备用金待领取，点击链接 http://pingan-claim.xyz 立即申领，今日24点失效。",
    "您好，我是快递客服，您的包裹在运输中丢失，我们将双倍赔偿，请加QQ：8839201办理理赔。",
    "爸，我手机摔坏了换了新号，这是我的新号码，有事联系。",
    "【京东】您尾号8899的订单已签收，如非本人操作请联系客服 400-606-5500。",
    "我是公安局刑侦大队的，你名下银行卡涉嫌洗钱案，需要把钱转到安全账户配合调查，否则马上逮捕你。",
]


def main():
    print(f"SecurMate 反诈检测 Demo | 模型：{MODEL_NAME} | 服务：{OLLAMA_URL}")
    print("命令说明：直接回车跑内置测试样本，输入文本则检测该文本，输入 q 退出\n")

    while True:
        text = input(">>> 请输入要检测的文本（直接回车=跑测试样本）：").strip()
        if text.lower() == "q":
            break
        samples = TEST_SAMPLES if not text else [text]
        for s in samples:
            try:
                result = detect(s)
                pretty_print(s, result)
            except requests.exceptions.ConnectionError:
                print("❌ 连不上 Ollama！请先启动 Ollama 服务（运行 ollama serve 或打开 Ollama 应用）")
                return
            except requests.exceptions.HTTPError as e:
                print(f"❌ 请求出错：{e}，检查 MODEL_NAME 是否和 ollama pull 的一致（ollama list 查看）")
                return
        if not text:
            break  # 跑完内置样本即退出


if __name__ == "__main__":
    main()
