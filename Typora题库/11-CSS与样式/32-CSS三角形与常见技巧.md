# 题 32：纯 CSS 画三角形？还有哪些常考技巧？

## 面试官可能怎么问

- 三角形原理？
- 梯形/气泡小三角？
- 其他常考手写？

## 口述结构（90 秒）

1. 宽高设 0，用透明 `border`，只给一边（或邻边）上色，交汇成三角
2. 气泡：矩形盒子 + `::after`/`::before` 三角贴边；注意层级与边框色
3. 其它常考：条纹渐变、滚动吸附、纯 CSS 开关（了解）、`clip-path`
4. 生产更多用 SVG/图标；面试考的是你懂 border 盒模型

## 参考答案

### 1. 三角形原理（步骤）

1. 元素 `width:0; height:0`，内容区消失。  
2. 四边 `border` 仍在，每边是一个梯形/三角区域。  
3. 三边透明、一边着色 → 只看见一个三角。

```css
.tri-up {
  width: 0;
  height: 0;
  border-left: 8px solid transparent;
  border-right: 8px solid transparent;
  border-bottom: 12px solid #333; /* 底边有色 → 尖朝上 */
}

.tri-down {
  width: 0; height: 0;
  border-left: 8px solid transparent;
  border-right: 8px solid transparent;
  border-top: 12px solid #333;
}

.tri-right {
  width: 0; height: 0;
  border-top: 8px solid transparent;
  border-bottom: 8px solid transparent;
  border-left: 12px solid #333;
}
```

口诀：**哪边有颜色，三角的「底」在哪边；尖指向对侧。**

### 2. 气泡小三角 / 梯形

```css
.bubble {
  position: relative;
  display: inline-block;
  padding: 8px 12px;
  background: #333;
  color: #fff;
  border-radius: 6px;
}
.bubble::after {
  content: "";
  position: absolute;
  left: 16px;
  bottom: -6px;
  width: 0; height: 0;
  border-left: 6px solid transparent;
  border-right: 6px solid transparent;
  border-top: 6px solid #333; /* 与背景同色 */
}
```

带边框的气泡：做**两个**三角（伪元素一大一小），大的用边框色、小的用背景色叠上去，露出一圈描边。

**梯形**：相邻两边 border 着色、另两边透明，或 `clip-path: polygon(...)`。

```css
.trap {
  width: 120px;
  height: 0;
  border-bottom: 40px solid #1677ff;
  border-left: 20px solid transparent;
  border-right: 20px solid transparent;
}
```

### 3. 其他常考手写（了解级）

```css
/* 条纹背景 */
.stripes {
  background: repeating-linear-gradient(
    45deg, #eee 0 8px, #fff 8px 16px
  );
}

/* 滚动吸附 */
.scroller {
  overflow-x: auto;
  scroll-snap-type: x mandatory;
}
.scroller > .page { scroll-snap-align: start; }

/* 现代形状：比 border 三角好维护 */
.tri2 {
  width: 40px; height: 40px;
  background: #333;
  clip-path: polygon(50% 0, 0 100%, 100% 100%);
}
```

checkbox hack 做纯 CSS Tab/手风琴：能讲原理即可，生产优先用按钮 + JS/详情元素。

业务例子：Tooltip/气泡箭头面试手写 border 三角；真实项目用 SVG 或组件库 Popover。

## 可能追问

- 等边三角？→ 用边长关系算 border 宽，或 `clip-path`/`rotate` 更直观。
- 为什么生产少用 border 三角？→ 改大小/描边/阴影麻烦，SVG/`clip-path` 更清晰。
- 空心三角？→ 双伪元素叠加，或 SVG stroke。

## 我的笔记

- 定义：
- 原理：
- 业务例子：
- 可能追问：
