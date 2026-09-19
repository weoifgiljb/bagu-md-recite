# bagu-md-recite · 八股 MD 背诵本

一套可复用的**前端 / AI 前端面试八股**学习套件：Typora 友好题库 + 本地 HTML 背诵本（先问后答、按主题筛选、掌握度 / 笔记）。

适合拿来：

- 秋招 / 社招八股过背
- Fork 后换成自己的题库，继续用同一套背诵 UI
- 当作「Markdown 题库 → 本地背诵 Web」的模板项目

## 功能

- **Typora 题库**：按主题分文件夹的 Markdown 卡片（AI 前端、RAG/Agent、Vue3、CSS、安全、DevTools、算法 Hot100…）
- **背诵本**：本地小服务 `http://127.0.0.1:8765`，支持显示答案、掌握标记、笔记（SQLite 存在本机）
- **一键重建**：改完 Markdown 后运行 `重建背诵本.py` 重新灌入背诵本

## 快速开始

### 环境

- Windows / macOS / Linux（仓库附带 Windows `.bat`；其它系统直接跑 Python）
- Python 3.10+

### 启动背诵本

**Windows**

```bat
启动背诵本.bat
```

浏览器打开：<http://127.0.0.1:8765>（不要直接双击 `index.html`）

**手动**

```bash
cd 背诵本
python3 server.py
```

### 改题库后重建

```bash
python3 重建背诵本.py
```

然后强制刷新背诵本页面（Ctrl+F5）。

## 目录结构

```
bagu-md-recite/
  Typora题库/           # 源头 Markdown 题库（按主题）
  背诵本/               # 本地背诵 Web + server.py
  重建背诵本.py         # 扫描 Typora题库 → 写入背诵本
  启动背诵本.bat
  LICENSE               # MIT
```

## 如何复用到你自己的题库

1. Fork / 克隆本仓库
2. 在 `Typora题库/` 下按文件夹增删 `.md` 卡片
3. 若有新主题文件夹：编辑 `重建背诵本.py` 里的 `SCAN_FOLDERS` / `WEEK_MAP` / `WEEK_ORDER`
4. 运行 `python3 重建背诵本.py`
5. 重新打开背诵本并强刷

## 卡片格式建议

```markdown
# 题 N：标题

## 面试官可能怎么问
- ...

## 口述结构（90 秒）
1. ...

## 参考答案
...

## 我的笔记
```

## 说明

- 题库来自个人秋招整理与公开面试高频知识点，**不保证**与任何公司真题一致。
- 「项目深挖」等卡片含作者项目口径示例，Fork 后请改成你自己的项目故事。
- 未内置第三方整库；掌握度数据在本机 `背诵本/recite.db`（已 gitignore）。

## License

MIT — 欢迎 Star / Fork / 改造成你的背诵体系。
