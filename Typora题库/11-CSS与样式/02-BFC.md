# 题 2：什么是 BFC？能解决什么问题？

## 面试官可能怎么问

- 怎么触发 BFC？
- 清浮动、margin 重叠怎么用 BFC？
- 触发之后具体改哪一层、写什么属性？

## 口述结构（90 秒）

1. BFC = 块级格式化上下文：一块独立布局区域，内部怎么排，尽量不把麻烦「漏」到外面
2. 先认症状（高度塌了 / margin 叠了 / 两栏被浮动挤乱），再在**合适的那一层**触发 BFC
3. 触发常用：`display: flow-root`（优先）、`overflow: auto/hidden`、`float`、`position: absolute/fixed`、flex/grid 子项等
4. 讲清「改父还是改子」：清浮动改**父**；隔开 margin 常改**中间包一层**或改用 padding/gap

## 参考答案

### 1. 它是什么

BFC（Block Formatting Context）是浏览器排布块级盒子时的一套独立规则。同一个 BFC 里的块按规则排；不同 BFC 之间更「绝缘」。面试别背定义，要会：**什么场景开 BFC、开在谁身上、写哪句 CSS**。

### 2. 怎么触发（记常用即可）

| 写法 | 何时用 | 副作用 |
| --- | --- | --- |
| `display: flow-root` | **首选**专为开 BFC | 几乎无额外裁剪 |
| `overflow: hidden/auto` | 老项目常见 | 可能裁阴影、绝对定位、sticky 失效 |
| `float: left/right` | 自己在讲浮动时顺带 | 父级又可能塌，一般不当「解决方案」 |
| `position: absolute/fixed` | 弹层等 | 脱离普通流 |
| 父是 flex/grid | 子项本身是 BFC | 布局已在用 Flex/Grid 时自然具备 |

### 3. 遇见问题 → 怎么办（步骤）

**场景 A：父级高度塌陷（子元素全 float）**

1. 现象：卡片里头像 `float:left`，父盒子高度变 0，背景/边框包不住。  
2. 原因：浮动子元素不撑开普通父级高度。  
3. 处理：**给父级**开 BFC，不要只给浮动的子元素加莫名其妙属性。  
```css
.card { display: flow-root; }   /* 推荐 */
/* 或老写法 */
.card { overflow: hidden; }
/* 或 clearfix 伪元素，本质也是隔开浮动 */
.card::after { content: ""; display: table; clear: both; }
```
4. 验收：父级高度包住浮动内容；后面的兄弟不再钻到浮动旁边去（除非你想环绕）。

**场景 B：垂直 margin 重叠（合并）**

1. 现象：标题 `margin-bottom: 24px`，段落 `margin-top: 16px`，实际空隙不是 40 而是 24。  
2. 原因：相邻块级盒在同一 BFC 里，垂直 margin 会合并。  
3. 处理任选其一（讲清取舍）：  
   - **包一层并开 BFC**：让两边不在「直接相邻」关系里  
```css
.section { display: flow-root; padding: 16px 0; } /* 用 padding 代替一侧 margin 更稳 */
```
   - **改结构间距**：父子之间用父的 `padding`，兄弟之间用父的 `gap`（flex/grid）  
   - 少用「给父 overflow:hidden 硬隔」除非你接受裁剪副作用  
4. 验收：量一下间距是否等于你期望的设计值。

**场景 C：两栏自适应（左 float，右被挡住）**

1. 现象：左边浮动侧栏，右边正文跑到侧栏下面或叠住。  
2. 处理：给**右边主栏**开 BFC（或直接 Flex/Grid，现代优先）。  
```css
.aside { float: left; width: 200px; }
.main { display: flow-root; } /* 或 overflow: auto */
```
3. 现代写法更推荐：  
```css
.row { display: flex; gap: 16px; }
.aside { flex: 0 0 200px; }
.main { flex: 1; min-width: 0; }
```
面试可以说：BFC 是原理题答案；新项目布局优先 Flex/Grid。

### 4. 决策口诀（面试收尾）

- **先定位改谁**：塌高度 → 改父；隔 margin → 改包裹层或改用 padding/gap；挡浮动 → 改被挡的那一列。  
- **再选触发方式**：能 `flow-root` 不用 `hidden` 乱裁。  
- **新布局能 Flex/Grid 就别靠 float + BFC 拼。**

## 可能追问

- 和 IFC 区别？→ IFC 是行内格式化上下文，关心行盒、垂直对齐、行高。  
- `overflow: hidden` 副作用？→ 裁切阴影/绝对定位子元素；可能影响 `position: sticky`。  
- `flow-root` 和 clearfix？→ 都能清浮动；`flow-root` 语义就是建 BFC，更干净。

## 我的笔记

- 定义：
- 原理：
- 业务例子：
- 可能追问：
