# 题 28：图片被撑破布局怎么处理？object-fit？

## 面试官可能怎么问

- img 默认是什么元素？
- cover 和 contain？
- 背景图 vs img？

## 口述结构（90 秒）

1. `img` 是**替换元素**，有固有宽高；默认 `inline`，可被内容撑破容器
2. 流体：`max-width:100%; height:auto`；定框裁切：`object-fit` + `object-position`
3. `cover` 铺满裁切；`contain` 完整可见可能留白
4. 内容图用 `<img>`（SEO/无障碍）；装饰用 CSS `background`；防 CLS 用宽高或 `aspect-ratio`

## 参考答案

### 1. img 默认与「撑破」

- 默认显示：`inline` 替换元素，有 intrinsic size。  
- 撑破常见原因：大图宽高未限制；父级是 flex 子项未 `min-width:0`；写了固定 `height` 又没配 fit。

```css
/* 响应式底线 */
img {
  max-width: 100%;
  height: auto;
  display: block; /* 顺带去掉基线空隙，见题 23 */
}

/* flex 子项防撑破 */
.media { min-width: 0; }
```

### 2. object-fit：cover vs contain

先给图片一个**明确的盒子**（宽高或 aspect-ratio），再谈 fit：

```css
.avatar {
  width: 64px;
  height: 64px;
  border-radius: 50%;
  overflow: hidden;
}
.avatar img {
  width: 100%;
  height: 100%;
  object-fit: cover;       /* 铺满，多余裁掉 */
  object-position: center; /* 裁哪边 */
}

.thumb {
  width: 100%;
  aspect-ratio: 16 / 9;
}
.thumb img {
  width: 100%;
  height: 100%;
  object-fit: contain;     /* 完整显示，可能两侧空 */
  background: #f5f5f5;
}
```

| 值 | 效果 | 场景 |
| --- | --- | --- |
| `cover` | 铺满裁切 | 头像、卡片封面 |
| `contain` | 完整可见 | 商品透明底、logo |
| `fill` | 拉伸变形 | 一般避免 |
| `none` | 原尺寸 | 少用 |
| `scale-down` | 相当于 none/contain 更小者 | 避免放大模糊 |

### 3. 背景图 vs `<img>`

```css
.hero {
  background: url(hero.webp) center / cover no-repeat;
  min-height: 240px;
}
```

```html
<img src="product.webp" alt="红色跑鞋侧面" width="800" height="600" loading="lazy" />
```

| | `<img>` | `background-image` |
| --- | --- | --- |
| 语义 / SEO / alt | 有 | 无（装饰） |
| object-fit | 有 | 用 `background-size: cover/contain` |
| 懒加载 / 优先级 | `loading`/`fetchpriority` | 靠自己控 |

防 CLS：

```html
<img src="a.webp" alt="" width="400" height="300" />
```
或 CSS：`aspect-ratio: 4/3;` 先占位。

业务例子：头像圆 `cover`；商品图列表定高 `cover`；Logo 完整显示用 `contain`。

## 可能追问

- `aspect-ratio`？→ 先占位防跳动，再配合 fit。
- 和 `srcset`/`picture`？→ 不同分辨率/艺术裁切；fit 管「盒内怎么铺」。
- 替换元素还有谁？→ `video`、`iframe`、表单控件等，部分也支持 `object-fit`。

## 我的笔记

- 定义：
- 原理：
- 业务例子：
- 可能追问：
