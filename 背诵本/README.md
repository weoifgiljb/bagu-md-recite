# 背诵本（SQLite）

## 怎么用

1. 双击 启动背诵本.bat（本目录，或上级「八股预备」目录同名脚本）
2. 浏览器会打开 http://127.0.0.1:8765/index.html
3. 页眉显示「SQLite 已连接」即表示状态写入数据库

## 存哪里

- 数据库：同目录 
ecite.db
- 表：progress(question_id, status, notes, updated_at)
- status：
ew / learning / mastered / hard

## 说明

- 掌握度、四行笔记会写入 SQLite
- 若以前用过浏览器本地缓存，第一次连上库且库为空时会自动迁移
- 不要直接双击 index.html（那样写不进库，会回退 localStorage）
- 关掉启动窗口即停止服务
