# -*- coding: utf-8 -*-
"""Reorganize 八股预备 into finer topic folders and link into 秋招准备."""
from __future__ import annotations
import os, re, shutil, json, subprocess
from pathlib import Path

HOME = Path(os.environ["USERPROFILE"]) / "Desktop"
BAGU = HOME / "八股预备"
QIU = HOME / "秋招准备"
TY = BAGU / "Typora题库"
SRC_JS = BAGU / "top-javascript-interview-questions"
SRC_REACT = BAGU / "top-reactjs-interview-questions"

JS_RULES = [
    ("01-类型与相等", [r"类型", r"typeof", r"==", r"===", r"NaN", r"null", r"undefined", r"原始", r"包装对象", r"Integer", r"浮点", r"精度", r"falsy", r"truthy"]),
    ("02-作用域闭包与this", [r"作用域", r"闭包", r"hoisting", r"提升", r"this", r"call", r"apply", r"bind", r"词法", r"暂时性死区", r"TDZ", r"var", r"let", r"const"]),
    ("03-原型与面向对象", [r"原型", r"prototype", r"继承", r"new ", r"new\b", r"类", r"class", r"构造", r"实例", r"面向对象", r"Person"]),
    ("04-异步事件循环与Promise", [r"Promise", r"async", r"await", r"微任务", r"宏任务", r"事件循环", r"event loop", r"callback", r"Generator", r"并发", r"并行", r"finally"]),
    ("05-函数与数组对象", [r"函数", r"箭头", r"柯里", r"curry", r"数组", r"对象", r"解构", r"展开", r"rest", r"Map", r"Set", r"WeakMap", r"迭代", r"生成器", r"深拷贝", r"浅拷贝", r"冻结", r"seal"]),
    ("06-DOM事件与浏览器API", [r"DOM", r"事件", r"冒泡", r"捕获", r"委托", r"preventDefault", r"stopPropagation", r"innerHTML", r"textContent", r"document", r"window", r"Worker", r"Intl", r"load", r"DOMContentLoaded", r"attribute", r"property"]),
    ("07-网络存储与安全", [r"cookie", r"localStorage", r"sessionStorage", r"CORS", r"XSS", r"CSRF", r"HTTP", r"fetch", r"Ajax", r"JSONP", r"安全", r"同源"]),
    ("08-ES新特性与模块工程", [r"ES6", r"ES2015", r"模块", r"import", r"export", r"Symbol", r"Proxy", r"Reflect", r"可选链", r"空值合并", r"严格模式", r"use strict", r"Tree.?shaking", r"打包", r"Babel"]),
]

REACT_RULES = [
    ("01-核心概念与渲染", [r"什么是 React", r"Virtual DOM", r"虚拟 DOM", r"JSX", r"Fiber", r"协调", r"reconcile", r"渲染", r"render", r"key", r"单向数据流", r"组合"]),
    ("02-Hooks", [r"Hook", r"useState", r"useEffect", r"useMemo", r"useCallback", r"useRef", r"useContext", r"useReducer", r"自定义 Hook", r"Rules of Hooks"]),
    ("03-状态与数据流", [r"state", r"状态", r"props", r"Context", r"Redux", r"状态提升", r"受控", r"非受控", r"合成事件"]),
    ("04-性能优化", [r"性能", r"memo", r"懒加载", r"lazy", r"Suspense", r"code.?split", r"重渲染", r"优化"]),
    ("05-SSR-RSC与路由", [r"SSR", r"SSG", r"hydration", r"水合", r"Server Component", r"RSC", r"路由", r"Next"]),
    ("06-模式与工程实践", [r"模式", r"HOC", r"高阶", r"Portal", r"错误边界", r"Error Boundary", r"严格模式", r"Fragment", r"ref", r"forwardRef"]),
]

EMPTY_SCAFFOLD = {
    "03-AI前端": [
        ("SSE与流式输出.md", "# SSE 与流式输出\n\n> 第 1 周重点。先自己口述，再补笔记。\n\n## 我的四行\n- 定义：\n- 原理：\n- 业务例子：\n- 可能追问：\n"),
        ("打字机渲染与Markdown安全.md", "# 打字机渲染与 Markdown 安全\n\n## 我的四行\n- 定义：\n- 原理：\n- 业务例子：\n- 可能追问：\n"),
        ("请求取消与断线重连.md", "# 请求取消与断线重连\n\n## 我的四行\n- 定义：\n- 原理：\n- 业务例子：\n- 可能追问：\n"),
    ],
    "04-RAG与Agent": [
        ("RAG链路前端职责.md", "# RAG 链路里前端做什么\n\n## 我的四行\n- 定义：\n- 原理：\n- 业务例子：\n- 可能追问：\n"),
        ("Tool-Calling与人机确认.md", "# Tool Calling 与人机确认\n\n## 我的四行\n- 定义：\n- 原理：\n- 业务例子：\n- 可能追问：\n"),
    ],
    "05-Flutter": [
        ("三棵树与重建.md", "# Flutter 三棵树与重建\n\n## 我的四行\n- 定义：\n- 原理：\n- 业务例子：\n- 可能追问：\n"),
        ("Isolate与Platform-Channel.md", "# Isolate 与 Platform Channel\n\n## 我的四行\n- 定义：\n- 原理：\n- 业务例子：\n- 可能追问：\n"),
    ],
    "06-Taro小程序": [
        ("运行时与DOM模拟.md", "# Taro 运行时与 DOM 模拟\n\n## 我的四行\n- 定义：\n- 原理：\n- 业务例子：\n- 可能追问：\n"),
        ("多端API映射与性能.md", "# 多端 API 映射与性能\n\n## 我的四行\n- 定义：\n- 原理：\n- 业务例子：\n- 可能追问：\n"),
    ],
    "07-浏览器网络补洞": [
        ("缓存与跨域.md", "# 缓存与跨域\n\n## 我的四行\n- 定义：\n- 原理：\n- 业务例子：\n- 可能追问：\n"),
    ],
}


def classify(title: str, rules):
    t = title
    for folder, kws in rules:
        for kw in kws:
            if re.search(kw, t, re.I):
                return folder
    return "09-其他"


def move_topic_files(src_dir: Path, rules, prefix: str):
    """Move flat md files into topic subfolders. Returns catalog list."""
    if not src_dir.exists():
        return []
    files = [f for f in src_dir.glob("*.md")]
    catalog = []
    for f in files:
        folder = classify(f.stem, rules)
        dest_dir = src_dir / folder
        dest_dir.mkdir(parents=True, exist_ok=True)
        dest = dest_dir / f.name
        if dest.exists():
            # already there
            pass
        else:
            shutil.move(str(f), str(dest))
        rel = dest.relative_to(TY).as_posix()
        catalog.append((folder, f.stem, rel))
    # write per-topic + section index
    by = {}
    for folder, title, rel in catalog:
        by.setdefault(folder, []).append((title, rel))
    lines = [f"# {prefix}", "", f"共 {len(catalog)} 题，按主题拆分如下。", ""]
    for folder in sorted(by):
        lines.append(f"## {folder}（{len(by[folder])}）")
        lines.append("")
        for title, rel in sorted(by[folder], key=lambda x: x[0]):
            # link relative to section index file in src_dir
            local = Path(rel).name
            lines.append(f"- [{title}](./{folder}/{local})")
        lines.append("")
        # topic mini index
        tlines = [f"# {folder}", ""]
        for title, rel in sorted(by[folder], key=lambda x: x[0]):
            tlines.append(f"- [{title}](./{Path(rel).name})")
        (src_dir / folder / "目录.md").write_text("\n".join(tlines) + "\n", encoding="utf-8")
    (src_dir / "目录.md").write_text("\n".join(lines) + "\n", encoding="utf-8")
    return catalog


def ensure_scaffold():
    plan = TY / "00-计划与打卡"
    plan.mkdir(parents=True, exist_ok=True)
    (plan / "四周计划.md").write_text(
        """# 四周计划（低自律版）

每天 45 分钟封顶；每晚 21:00 打卡。

| 周 | 主题 | 主看目录 |
| --- | --- | --- |
| 第1周 | AI 前端交互 | `03-AI前端` |
| 第2周 | RAG / Agent | `04-RAG与Agent` |
| 第3周 | Flutter | `05-Flutter` |
| 第4周 | Taro + 浏览器补洞 | `06-Taro小程序` + `07-浏览器网络补洞` |

JS / React 当「概念补洞库」：哪天卡概念，就进对应主题文件夹刷 1～2 题。

关联材料（秋招准备）：
- 简历：`秋招准备/资料/简历`
- 面经：`秋招准备/资料/面经`
- 作品 PDF：`秋招准备/output/pdf`
""",
        encoding="utf-8",
    )
    (plan / "打卡模板.md").write_text(
        """# 打卡模板

日期：
今日主题：
刷了哪题：
卡住的概念：
口述是否完成：是 / 否

## 四行笔记
- 定义：
- 原理：
- 业务例子：
- 可能追问：
""",
        encoding="utf-8",
    )
    for folder, files in EMPTY_SCAFFOLD.items():
        d = TY / folder
        d.mkdir(parents=True, exist_ok=True)
        for name, content in files:
            p = d / name
            if not p.exists():
                p.write_text(content, encoding="utf-8")
        # folder readme
        rm = d / "README.md"
        if not rm.exists():
            rm.write_text(f"# {folder}\n\n按文件名顺序准备；每题写四行笔记。\n", encoding="utf-8")


def write_master_index(js_cat, react_cat):
    lines = [
        "# 八股预备 · Typora 总目录",
        "",
        "用 Typora：**文件 → 打开文件夹** → 选 `Typora题库`。",
        "",
        "## 怎么用",
        "",
        "1. 先看 `00-计划与打卡/四周计划.md`",
        "2. 按当周主题进对应文件夹",
        "3. JS/React 只在概念卡壳时补洞，不要平行刷完",
        "4. 个人复盘写到 `../我的笔记/`，避免重建覆盖",
        "",
        "## 本周主线",
        "",
        "- [00 计划与打卡](./00-计划与打卡/四周计划.md)",
        "- [03 AI前端](./03-AI前端/README.md)",
        "- [04 RAG与Agent](./04-RAG与Agent/README.md)",
        "- [05 Flutter](./05-Flutter/README.md)",
        "- [06 Taro小程序](./06-Taro小程序/README.md)",
        "- [07 浏览器网络补洞](./07-浏览器网络补洞/README.md)",
        "",
        f"## 概念补洞 · JavaScript（{len(js_cat)}）",
        "",
        "- [JS 主题目录](./01-JavaScript/目录.md)",
        "",
        f"## 概念补洞 · React（{len(react_cat)}）",
        "",
        "- [React 主题目录](./02-React/目录.md)",
        "",
        "## 关联 · 秋招准备",
        "",
        "- 桌面 `秋招准备` 已通过目录联接挂到本库（见上级或秋招准备内的 `八股预备`）",
        "- 简历 PDF：`../../秋招准备/资料/简历`",
        "- 面经 PDF：`../../秋招准备/资料/面经`",
        "",
    ]
    (TY / "目录.md").write_text("\n".join(lines) + "\n", encoding="utf-8")


def write_root_readme():
    text = """# 八股预备

秋招面试复习库（Typora 友好）。已与桌面 `秋招准备` 目录联接。

## 结构

```
八股预备/
  Typora题库/                 ← 日常打开这个
    00-计划与打卡/
    01-JavaScript/            ← 按主题拆细
    02-React/                 ← 按主题拆细
    03-AI前端/
    04-RAG与Agent/
    05-Flutter/
    06-Taro小程序/
    07-浏览器网络补洞/
    目录.md
  top-javascript-interview-questions/   ← 源仓库
  top-reactjs-interview-questions/      ← 源仓库
  我的笔记/
  生成Typora题库.py
```

## 和秋招准备的关系

- `秋招准备`：作品集、简历、面经、项目代码
- `八股预备`：概念题与打卡
- 在 `秋招准备/八股预备` 可直接进入本库（Windows 目录联接）

## 更新题库

```powershell
$env:Path = "C:\\Program Files\\Git\\usr\\bin;C:\\Program Files\\Git\\cmd;" + $env:Path
cd $env:USERPROFILE\\Desktop\\八股预备\\top-javascript-interview-questions; git pull
cd $env:USERPROFILE\\Desktop\\八股预备\\top-reactjs-interview-questions; git pull
cd $env:USERPROFILE\\Desktop\\八股预备
py -3 .\\生成Typora题库.py
py -3 .\\拆分主题.py
```
"""
    (BAGU / "README.md").write_text(text, encoding="utf-8")


def link_into_qiuzhao():
    link = QIU / "八股预备"
    if link.exists():
        # if already junction/symlink or dir, leave if correct
        if link.is_symlink() or link.is_dir():
            # check if same target roughly by presence of Typora题库
            if (link / "Typora题库").exists() or (link / "README.md").exists():
                return "exists"
    # create junction
    if link.exists():
        return "blocked"
    cmd = ["cmd", "/c", "mklink", "/J", str(link), str(BAGU)]
    r = subprocess.run(cmd, capture_output=True, text=True, encoding="utf-8", errors="replace")
    return f"rc={r.returncode} out={(r.stdout or '') + (r.stderr or '')}"


def write_qiuzhao_pointer():
    # small markdown in 秋招准备 docs
    docs = QIU / "docs"
    docs.mkdir(exist_ok=True)
    (docs / "八股复习入口.md").write_text(
        """# 八股复习入口

面试概念复习不在本仓库源码里，而在同级联接目录：

- [../八股预备/Typora题库/目录.md](../八股预备/Typora题库/目录.md)
- 计划：[../八股预备/Typora题库/00-计划与打卡/四周计划.md](../八股预备/Typora题库/00-计划与打卡/四周计划.md)

本仓库（秋招准备）负责：

- `资料/简历`、`资料/面经`
- `output/pdf` 作品与投递材料
- 项目代码（doc-review-* 等）
""",
        encoding="utf-8",
    )
    # append tip to README if not present
    readme = QIU / "README.md"
    if readme.exists():
        raw = readme.read_text(encoding="utf-8")
        if "八股预备" not in raw:
            raw = raw.rstrip() + "\n\n## 八股复习\n\n- 目录联接：`八股预备/`（指向桌面「八股预备」）\n- 说明：`docs/八股复习入口.md`\n"
            readme.write_text(raw, encoding="utf-8")


def main():
    # Rename English folder names if needed - already 01-JavaScript
    js_dir = TY / "01-JavaScript"
    react_dir = TY / "02-React"
    ensure_scaffold()
    js_cat = move_topic_files(js_dir, JS_RULES, "JavaScript 主题目录")
    react_cat = move_topic_files(react_dir, REACT_RULES, "React 主题目录")
    write_master_index(js_cat, react_cat)
    write_root_readme()
    link_status = link_into_qiuzhao()
    write_qiuzhao_pointer()
    # save split script copy for regeneration
    summary = {
        "js": len(js_cat),
        "react": len(react_cat),
        "js_by": {},
        "react_by": {},
        "link": link_status,
    }
    for folder, title, rel in js_cat:
        summary["js_by"][folder] = summary["js_by"].get(folder, 0) + 1
    for folder, title, rel in react_cat:
        summary["react_by"][folder] = summary["react_by"].get(folder, 0) + 1
    (BAGU / "_reorganize_summary.json").write_text(json.dumps(summary, ensure_ascii=False, indent=2), encoding="utf-8")
    print(json.dumps(summary, ensure_ascii=False, indent=2))

if __name__ == "__main__":
    main()