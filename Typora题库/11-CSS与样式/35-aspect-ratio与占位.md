# 题 35：宽高比与图片占位怎么做？

## 面试官可能怎么问

- 以前 padding-top 黑客？
- aspect-ratio？
- 防 CLS？

## 口述结构（90 秒）

1. **旧方案**：父级 `height:0` + `padding-top: 百分比`（百分比相对**宽度**）撑出比例盒，子绝对定位填满
2. **新方案**：`aspect-ratio: 16 / 9`（或 `1 / 1`），语义清晰
3. **防 CLS**：图片在 HTML 写 `width`/`height`，或 CSS 固定比例占位；骨架屏同尺寸；避免加载后高度从 0 跳开
4. 配 `object-fit: cover/contain` 裁切或留白

## 参考答案

### 1. 以前的 padding-top「黑客」（回答该问）

原理：垂直方向 `padding-%` 参照的是**包含块宽度**，所以 `padding-top: 56.25%` ≈ 16:9。

```css
.box {
  position: relative;
  height: 0;
  padding-top: 56.25%; /* 9/16 = 0.5625 */
  background: #eee;
}
.box > * {
  position: absolute;
  inset: 0;
  width: 100%;
  height: 100%;
  object-fit: cover;
}
```

缺点：高度被 padding「占用」，真实内容要绝对定位；和普通流混用容易绕晕。旧项目兼容才保留。

### 2. 现代：`aspect-ratio`（回答该问）

```css
.video {
  aspect-ratio: 16 / 9;
  width: 100%;
  background: #eee;
}
.video img,
.video video {
  width: 100%;
  height: 100%;
  object-fit: cover;
  display: block;
}
```

正方形头像：`aspect-ratio: 1;`。  
也可 `aspect-ratio: 4 / 3;`。若同时设了明确 width+height，比例与二者冲突时按规范协调（常见是宽度定了再由 ratio 推高度）。

### 3. 防 CLS（Cumulative Layout Shift）（回答该问）

步骤：

1. **服务端/模板已知固有尺寸**：`<img width="800" height="450" src="..." alt="">`（浏览器据此算比例占位）。
2. **或 CSS 占位**：父级 `aspect-ratio` / 固定高度，图片 `width:100%; height:100%; object-fit:cover`。
3. **骨架屏**：同宽高比灰块，图片 `onload` 后淡入，避免「先 0 高再撑开」。
4. **懒加载**：`loading="lazy"` 仍要保留尺寸或比例，否则进视口才撑开也会抖。
5. **字体**：次要 CLS 来源；关键标题可 `font-display` + 接近的 fallback 度量。

```html
<div class="media" style="aspect-ratio:16/9">
  <img src="cover.jpg" width="1600" height="900" alt="封面" loading="lazy" />
</div>
```

```css
.media img {
  width: 100%;
  height: 100%;
  object-fit: cover;
}
```

### 4. 业务例子

- 视频课封面、Banner、商品主图统一 16:9 / 1:1，列表不会一张张「蹦高度」。
- 管理后台上传预览区先画比例框再塞图。

## 可能追问

- 和 `object-fit`？→ ratio 负责盒子形状，fit 负责图怎么装进盒子（cover 裁切 / contain 完整）。
- 浏览器支持？→ 现代浏览器 OK；极旧 WebView 回退 padding 黑科技。
- 只有宽度变、高度写死？→ 不如 ratio；写死高度在窄屏会变形或裁切失控。

## 我的笔记

- 定义：
- 原理：
- 业务例子：
- 可能追问：
