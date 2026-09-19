# -*- coding: utf-8 -*-
"""Import / remove Markdown cards for bagu-md-recite.

Examples:
  python manage_bank.py list
  python manage_bank.py import ./my.md --theme 10-Vue3
  python manage_bank.py import ./extra_cards/ --theme 16-我的专题 --create-theme --week "补洞 · 我的专题"
  python manage_bank.py remove --theme 10-Vue3 --name "01-ref与reactive.md"
  python manage_bank.py remove --theme 10-Vue3 --glob "*Pinia*"
  python manage_bank.py remove-theme 16-我的专题 --delete-files
"""
from __future__ import annotations

import argparse
import re
import shutil
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent
TY = ROOT / "Typora题库"
REBUILD = ROOT / "重建背诵本.py"
TEMPLATE = """# 题：{title}

## 面试官可能怎么问
- （把面试问法写在这里）

## 口述结构（90 秒）
1. 题意
2. 思路 / 复杂度
3. 边界与坑

## 参考答案
（写可操作的步骤或代码骨架）

## 可能追问
- 

## 我的笔记
"""


def themes() -> list[Path]:
    if not TY.is_dir():
        return []
    return sorted([p for p in TY.iterdir() if p.is_dir() and not p.name.startswith(".")])


def count_md(folder: Path) -> int:
    return sum(1 for p in folder.glob("*.md") if p.name.lower() != "readme.md")


def cmd_list(_: argparse.Namespace) -> int:
    print(f"题库目录: {TY}")
    if not themes():
        print("(空)")
        return 0
    for d in themes():
        print(f"  {d.name}\t{count_md(d)} 题")
    return 0


def ensure_theme(name: str, create: bool, week: str | None) -> Path:
    dest = TY / name
    if dest.is_dir():
        return dest
    if not create:
        raise SystemExit(
            f"主题不存在: {name}\n"
            f"可用: {', '.join(t.name for t in themes())}\n"
            f"若要新建，加上 --create-theme ，例如:\n"
            f'  python manage_bank.py import FILE --theme {name} --create-theme --week "补洞 · 自定义"'
        )
    dest.mkdir(parents=True, exist_ok=True)
    (dest / "README.md").write_text(
        f"# {name}\n\n本主题由 `manage_bank.py` 创建。改完题后请运行 `python 重建背诵本.py`。\n",
        encoding="utf-8",
    )
    # WEEK_MAP is optional now if rebuild auto-discovers; still patch for nicer labels
    if week:
        patch_week_map(name, week)
    print("CREATED_THEME", dest)
    return dest


def patch_week_map(folder: str, week: str) -> None:
    if not REBUILD.exists():
        return
    text = REBUILD.read_text(encoding="utf-8")
    if f'"{folder}"' in text and "WEEK_MAP" in text:
        # already mentioned
        if f'"{folder}":' in text:
            print("WEEK_MAP already has", folder)
            return
    # insert into WEEK_MAP before closing }
    m = re.search(r"WEEK_MAP\s*=\s*\{([\s\S]*?)\n\}", text)
    if not m:
        print("WARN: WEEK_MAP not found; rebuild will use folder name as week label")
        return
    body = m.group(1).rstrip()
    if not body.endswith(","):
        body += ","
    body += f'\n    "{folder}": "{week}",'
    new = text[: m.start(1)] + body + text[m.end(1) :]
    # WEEK_ORDER: append week if missing
    if week not in new:
        mo = re.search(r"WEEK_ORDER\s*=\s*\[([\s\S]*?)\]", new)
        if mo:
            ob = mo.group(1).rstrip()
            if not ob.endswith(","):
                ob += ","
            # put before 计划/其他 if present
            insert = f'\n    "{week}",'
            if '"计划"' in ob:
                ob = ob.replace('"计划"', f'"{week}",\n    "计划"', 1)
            else:
                ob += insert
            new = new[: mo.start(1)] + ob + new[mo.end(1) :]
    REBUILD.write_text(new, encoding="utf-8")
    print("PATCHED WEEK_MAP/ORDER for", folder, "->", week)


def cmd_import(args: argparse.Namespace) -> int:
    src = Path(args.path).expanduser().resolve()
    if not src.exists():
        raise SystemExit(f"找不到: {src}")
    theme = ensure_theme(args.theme, args.create_theme, args.week)
    copied: list[Path] = []
    if src.is_file():
        if src.suffix.lower() != ".md":
            raise SystemExit("只支持导入 .md 文件，或包含 .md 的文件夹")
        dest = theme / src.name
        if dest.exists() and not args.force:
            raise SystemExit(f"已存在 {dest} ，若覆盖请加 --force")
        shutil.copy2(src, dest)
        copied.append(dest)
    else:
        files = sorted(src.rglob("*.md"))
        files = [f for f in files if f.name.lower() != "readme.md"]
        if not files:
            raise SystemExit("文件夹里没有 .md")
        for f in files:
            dest = theme / f.name
            if dest.exists() and not args.force:
                print("SKIP exists", dest.name)
                continue
            shutil.copy2(f, dest)
            copied.append(dest)
            print("IMPORT", dest.relative_to(ROOT))
    if not copied and src.is_file():
        pass
    elif src.is_file():
        print("IMPORT", copied[0].relative_to(ROOT))
    print(f"已导入 {len(copied)} 个文件到 {theme.name}")
    if args.rebuild:
        return run_rebuild()
    print("下一步: python 重建背诵本.py   （或本次加 --rebuild）")
    return 0


def cmd_new(args: argparse.Namespace) -> int:
    theme = ensure_theme(args.theme, True, args.week or f"补洞 · {args.theme}")
    title = args.title or Path(args.name).stem
    name = args.name if args.name.endswith(".md") else args.name + ".md"
    dest = theme / name
    if dest.exists() and not args.force:
        raise SystemExit(f"已存在 {dest}")
    dest.write_text(TEMPLATE.format(title=title), encoding="utf-8")
    print("NEW", dest.relative_to(ROOT))
    if args.rebuild:
        return run_rebuild()
    print("编辑该文件后运行: python 重建背诵本.py")
    return 0


def cmd_remove(args: argparse.Namespace) -> int:
    targets: list[Path] = []
    if args.path:
        p = Path(args.path)
        if not p.is_absolute():
            # allow Typora题库/... or theme-relative
            cand = ROOT / p
            if not cand.exists():
                cand = TY / p
            p = cand
        if not p.exists():
            raise SystemExit(f"找不到: {p}")
        targets.append(p)
    else:
        if not args.theme:
            raise SystemExit("请指定 --path 或 --theme")
        theme = TY / args.theme
        if not theme.is_dir():
            raise SystemExit(f"主题不存在: {args.theme}")
        if args.name:
            targets.append(theme / args.name)
        elif args.glob:
            targets.extend(sorted(theme.glob(args.glob)))
        else:
            raise SystemExit("删除主题内文件时请加 --name 或 --glob")
    removed = 0
    for t in targets:
        if not t.exists():
            print("MISSING", t)
            continue
        if t.suffix.lower() != ".md":
            print("SKIP non-md", t)
            continue
        if args.dry_run:
            print("DRY remove", t.relative_to(ROOT) if t.is_relative_to(ROOT) else t)
        else:
            t.unlink()
            print("REMOVED", t.name)
        removed += 1
    print(f"{'将删除' if args.dry_run else '已删除'} {removed} 个文件")
    if removed and args.rebuild and not args.dry_run:
        return run_rebuild()
    if removed and not args.dry_run:
        print("下一步: python 重建背诵本.py   （或本次加 --rebuild）")
    return 0


def cmd_remove_theme(args: argparse.Namespace) -> int:
    theme = TY / args.theme
    if not theme.exists():
        raise SystemExit(f"主题不存在: {args.theme}")
    n = count_md(theme)
    if args.delete_files:
        if args.dry_run:
            print("DRY delete tree", theme, f"({n} md)")
        else:
            shutil.rmtree(theme)
            print("DELETED_THEME", args.theme)
    else:
        print(
            f"主题 {args.theme} 仍有 {n} 道题文件保留在磁盘。"
            f"若连文件一起删，请加 --delete-files"
        )
    # strip from WEEK_MAP if present
    if REBUILD.exists() and not args.dry_run:
        text = REBUILD.read_text(encoding="utf-8")
        text2 = re.sub(
            rf'\n\s*"{re.escape(args.theme)}":\s*"[^"]*",?',
            "\n",
            text,
        )
        if text2 != text:
            REBUILD.write_text(text2, encoding="utf-8")
            print("STRIPPED from 重建背诵本.py WEEK_MAP")
    if args.rebuild and not args.dry_run:
        return run_rebuild()
    print("下一步: python 重建背诵本.py")
    return 0


def run_rebuild() -> int:
    print("RUNNING", REBUILD.name)
    r = subprocess.run([sys.executable, str(REBUILD)], cwd=str(ROOT))
    return r.returncode


def build_parser() -> argparse.ArgumentParser:
    ap = argparse.ArgumentParser(
        description="管理 Typora题库 的导入 / 删除（改完记得重建背诵本）"
    )
    sub = ap.add_subparsers(dest="cmd", required=True)

    p = sub.add_parser("list", help="列出主题与题量")
    p.set_defaults(func=cmd_list)

    p = sub.add_parser("import", help="导入 .md 文件或文件夹到某个主题")
    p.add_argument("path", help="文件或文件夹路径")
    p.add_argument("--theme", required=True, help="目标主题文件夹名，如 10-Vue3")
    p.add_argument("--create-theme", action="store_true", help="主题不存在则创建")
    p.add_argument("--week", default=None, help='背诵本周标签，如 "补洞 · 我的专题"')
    p.add_argument("--force", action="store_true", help="覆盖同名文件")
    p.add_argument("--rebuild", action="store_true", help="导入后立刻重建背诵本")
    p.set_defaults(func=cmd_import)

    p = sub.add_parser("new", help="在主题下新建空白卡片模板")
    p.add_argument("--theme", required=True)
    p.add_argument("--name", required=True, help="文件名，如 99-我的新题.md")
    p.add_argument("--title", default=None)
    p.add_argument("--week", default=None)
    p.add_argument("--force", action="store_true")
    p.add_argument("--rebuild", action="store_true")
    p.set_defaults(func=cmd_new)

    p = sub.add_parser("remove", help="删除一张或多张题")
    p.add_argument("--path", help="文件路径（相对仓库根或 Typora题库）")
    p.add_argument("--theme", help="主题名")
    p.add_argument("--name", help="主题内文件名")
    p.add_argument("--glob", help='主题内通配，如 "*Pinia*"')
    p.add_argument("--dry-run", action="store_true")
    p.add_argument("--rebuild", action="store_true")
    p.set_defaults(func=cmd_remove)

    p = sub.add_parser("remove-theme", help="从重建配置去掉主题；可选删除文件夹")
    p.add_argument("theme")
    p.add_argument("--delete-files", action="store_true")
    p.add_argument("--dry-run", action="store_true")
    p.add_argument("--rebuild", action="store_true")
    p.set_defaults(func=cmd_remove_theme)

    return ap


def main() -> int:
    ap = build_parser()
    args = ap.parse_args()
    return args.func(args)


if __name__ == "__main__":
    raise SystemExit(main())
