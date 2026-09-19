# bagu-md-recite · 八股 MD 背诵本

一套可复用的**前端 / AI 前端面试八股**学习套件：Typora 友好题库 + 本地 HTML 背诵本（先问后答、按主题筛选、掌握度 / 笔记）。

适合拿来：

- 秋招 / 社招八股过背
- Fork 后换成自己的题库，继续用同一套背诵 UI
- 当作「Markdown 题库 → 本地背诵 Web」的模板项目

## 功能

- **Typora 题库**：按主题分文件夹的 Markdown 卡片
- **背诵本**：本地小服务 `http://127.0.0.1:8765`
- **一键重建**：`重建背诵本.py`
- **题库管理**：`manage_bank.py`（导入 / 新建 / 删除）

## 快速开始

### 环境

- Windows / macOS / Linux
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

然后强制刷新（Ctrl+F5）。

---

## 如何导入 MD

题库源头在 `Typora题库/<主题文件夹>/某个题.md`。背诵本**不会**自动监视文件夹，导入后必须重建。

### 方式 A：命令行导入（推荐）

先看有哪些主题：

```bash
python3 manage_bank.py list
```

**导入单个文件到已有主题**

```bash
python3 manage_bank.py import ./我的卡片.md --theme 10-Vue3 --rebuild
```

**导入整个文件夹里的全部 .md**

```bash
python3 manage_bank.py import ./exported_cards/ --theme 11-CSS与样式 --force --rebuild
```

**新建一个主题再导入**

```bash
python3 manage_bank.py import ./extra/ --theme 16-我的专题 --create-theme --week "补洞 · 我的专题" --rebuild
```

参数说明：

| 参数 | 作用 |
|------|------|
| `--theme` | 目标主题文件夹名（先 `list` 查看） |
| `--create-theme` | 主题不存在则创建 |
| `--week` | 背诵本里显示的分类标签 |
| `--force` | 覆盖同名文件 |
| `--rebuild` | 导入后立刻重建背诵本 |

### 方式 B：手动复制

1. 把 `.md` 拷进 `Typora题库/某主题/`
2. 若是**全新主题**：文件夹名建议 `数字-名称`（如 `16-系统设计`），重建时会自动发现
3. 运行 `python3 重建背诵本.py`，背诵本 Ctrl+F5

### 方式 C：从模板新建空白卡

```bash
python3 manage_bank.py new --theme 10-Vue3 --name 99-我的新题.md --title "说说 nextTick" --rebuild
```

再用编辑器补全答案。

### 卡片格式（方便拆成「问 / 答」）

```markdown
# 题：标题

## 面试官可能怎么问
- ...

## 口述结构（90 秒）
1. ...

## 参考答案
...

## 可能追问
- ...

## 我的笔记
```

标题用一级 `#`；问法、参考答案用二级 `##`（标题里带「面试官 / 怎么问」「参考答」等字样即可被识别）。

---

## 如何删除 MD

### 删单题 / 多题

```bash
# 按路径
python3 manage_bank.py remove --path "Typora题库/10-Vue3/某题.md" --rebuild

# 按主题 + 文件名
python3 manage_bank.py remove --theme 10-Vue3 --name "06-keep-alive.md" --rebuild

# 按通配（建议先 dry-run）
python3 manage_bank.py remove --theme 15-算法Hot100 --glob "*爬楼梯*" --dry-run
python3 manage_bank.py remove --theme 15-算法Hot100 --glob "*爬楼梯*" --rebuild
```

### 删整个主题

```bash
# 从配置去掉标签（文件先留着）
python3 manage_bank.py remove-theme 16-我的专题 --rebuild

# 连文件夹一起删
python3 manage_bank.py remove-theme 16-我的专题 --delete-files --rebuild
```

### 手动删

直接删除 `Typora题库/...` 下的 `.md`，再跑 `python3 重建背诵本.py`。  
本机掌握度在 `背诵本/recite.db`，删题后旧进度可能残留，一般无影响。

---

## 目录结构

```
bagu-md-recite/
  Typora题库/           # 源头 Markdown（按主题）
  背诵本/               # 本地背诵 Web + server.py
  重建背诵本.py         # 扫描题库 → 写入背诵本
  manage_bank.py        # 导入 / 新建 / 删除
  启动背诵本.bat
  LICENSE               # MIT
```

## 说明

- 题库来自个人秋招整理与公开高频点，**不保证**与公司真题一致。
- 「项目深挖」含作者项目口径示例，Fork 后请改成你的故事。
- 掌握度数据在本机 `背诵本/recite.db`（已 gitignore）。

## License

MIT — 欢迎 Star / Fork / 改造成你的背诵体系。
