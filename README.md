# Mini Agent

从零实现的本地 Agent 运行环境，基于 Ollama 模型，不依赖 LangChain / LangGraph / AutoGen 等框架。

## 架构

```
User
  ↓
LLM (Ollama)
  ↓
Agent Runtime (loop)
  ↓
Tool Registry
  ↓
Tools → Sandbox → OS
```

## 快速开始

```bash
# 1. 安装依赖
python3 -m venv .venv && source .venv/bin/activate
pip install -r requirements.txt

# 2. 拉取模型
ollama pull qwen3:4b

# 3. 单次执行
python main.py "列出 workspace 中的文件"

# 4. 交互模式
python main.py

# 5. 指定模型和工作区
python main.py --model qwen3:8b --workspace ./my_project
```

## 可用工具

```bash
python main.py --list-tools
```

| 工具 | 说明 |
|------|------|
| `read_file` | 读取文件内容 |
| `list_directory` | 列出目录中的文件 |
| `write_file` | 写入/覆盖文件 |
| `diff_file` | 对比当前文件与提议内容的差异（不修改文件） |

## 选项

| 参数 | 说明 |
|------|------|
| `--model` | Ollama 模型名 (默认: qwen3:4b; 更快: qwen3:1.7b, qwen2.5:1.5b) |
| `--num-ctx` | 上下文窗口大小 (默认: 4096; 越小越快) |
| `--workspace` | 沙箱工作区目录 (默认: ./workspace) |
| `--list-tools` | 列出所有工具并退出 |
| `--no-memory` | 禁用对话记忆 |

## 速度优化

```bash
# ① 换更小的模型
ollama pull qwen3:1.7b
python main.py --model qwen3:1.7b

# ② 缩小上下文窗口（减少每次推理的计算量）
python main.py --num-ctx 2048

# ③ 组合使用
python main.py --model qwen3:1.7b --num-ctx 2048
```

## 项目结构

```
mini_agent/
├── main.py           CLI 入口
├── agent.py          Agent Runtime 循环
├── llm.py            Ollama API 客户端
├── sandbox.py        文件系统沙箱（路径越权防护）
├── tool.py           工具接口 + 注册中心
├── tools/
│   ├── read_file.py        读取文件
│   ├── list_directory.py   列出目录
│   ├── write_file.py       写入文件
│   └── diff_file.py        Diff 对比
├── workspace/        沙箱工作区根目录
├── .gitignore
├── pyproject.toml
└── requirements.txt
```

## 开发路线

- Phase 1: LLM + Tool Registry + read_file / list_directory
- Phase 2: write_file + workspace sandbox
- Phase 3: diff 生成（diff_file）
- Phase 4: 对话记忆（conversation memory）
- Phase 5: Docker 沙箱
- Phase 6: 规划 / 任务图 / 工作流
