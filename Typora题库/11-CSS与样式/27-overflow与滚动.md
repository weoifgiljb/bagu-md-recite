# 题 27：overflow、滚动条与滚动性能？

## 面试官可能怎么问

- overflow:hidden 副作用？
- 滚动链 / 穿透？
- 平滑滚动？

## 口述结构（90 秒）

1. `visible/hidden/auto/scroll`（及较新的 `clip`）管裁剪与是否出现滚动条
2. 出滚动条：内容溢出 + 该方向允许滚（`auto`/`scroll`）
3. 弹层打开要锁背景滚动；用 `overscroll-behavior` 防滚动穿透
4. 长列表虚拟滚动；`scroll` 回调里少强制 layout；平滑滚用 CSS/`scrollTo`

## 参考答案

### 1. overflow 取值与副作用

```css
.box { overflow: hidden; }           /* 裁切，不滚动 */
.box { overflow: auto; }             /* 需要时才出滚动条 */
.box { overflow-x: auto; overflow-y: hidden; }
.box { overflow: clip; }             /* 裁切且不建滚动容器，影响传播与 sticky 更「干净」 */
```

`overflow: hidden` 常见副作用：
1. 裁掉 `box-shadow`、子元素 `position:absolute` 溢出部分。  
2. 祖先 `hidden/auto/scroll` 常导致后代 `position: sticky` 失效。  
3. 可能意外创建 BFC（老题常考）。  
4. 焦点元素在裁切外时，无障碍体验差。

步骤：先问「要不要滚」→ 要滚用 `auto`；只要裁切且无滚动，再考虑 `hidden`/`clip`。

### 2. 弹层锁滚动 + 防穿透

```css
/* 打开 Modal 时 */
body.is-locked { overflow: hidden; }

.modal__panel {
  max-height: min(80vh, 640px);
  overflow: auto;
  overscroll-behavior: contain; /* 滚到头不要把滚动传给背后页面 */
}
```

```js
function lockScroll(lock) {
  document.body.classList.toggle("is-locked", lock);
}
```

iOS 上仅 `overflow:hidden` 有时不够，可能还要记 `scrollY` 并给 body 加 `position:fixed; top: -scrollY`（讲出思路即可）。

### 3. 平滑滚动

```css
html { scroll-behavior: smooth; } /* 锚点跳转 */
@media (prefers-reduced-motion: reduce) {
  html { scroll-behavior: auto; }
}
```

```js
el.scrollTo({ top: 0, behavior: "smooth" });
```

### 4. 滚动性能注意点

```js
let ticking = false;
scroller.addEventListener("scroll", () => {
  if (ticking) return;
  ticking = true;
  requestAnimationFrame(() => {
    // 读 scrollTop、改 transform；避免每帧 el.offsetHeight
    ticking = false;
  });
}, { passive: true });
```

- 长列表：虚拟列表，别一次性插上万 DOM。  
- 少在 scroll 里读布局属性再改样式（强制同步 layout）。  
- 自定义滚动条：`::-webkit-scrollbar`（WebKit）/ `scrollbar-width`（标准）。

业务例子：对话框 `body` 锁滚，面板内部 `overflow:auto` + `overscroll-behavior:contain`；文档页锚点 `scroll-behavior:smooth`。

## 可能追问

- sticky 被谁破坏？→ 任意 `overflow` 非 visible 的祖先都可能成为 sticky 的包含块边界。
- 滚动链？→ 子滚到底后继续滚手势传到父/页面；用 `overscroll-behavior` 切断。
- `scrollbar-gutter: stable`？→ 预留滚动条槽，避免出现/消失时布局抖动。

## 我的笔记

- 定义：
- 原理：
- 业务例子：
- 可能追问：
