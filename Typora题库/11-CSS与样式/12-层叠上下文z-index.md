# 题 12：层叠上下文和 z-index 是什么关系？弹层被挡住怎么查？

## 面试官可能怎么问

- `z-index` 什么时候生效？
- 哪些情况会创建新的层叠上下文？
- 为什么子元素 `z-index:9999` 还是被盖住？
- `transform`/`opacity`/`filter` 对 fixed 弹层有什么影响？
- 你怎么系统性排查？

## 口述结构（90 秒）

1. `z-index` 只在**同一层叠上下文**里比大小；先比上下文，再比上下文内
2. 定位元素（及 flex/grid 子项等）才谈传统 z-index；很多属性会**新建上下文**
3. 经典坑：父级 `transform`/`opacity<1` 后，子级再高也翻不出父级那一层
4. 弹层：Teleport 到 `body` + 统一层级规范（遮罩 < 面板 < toast）
5. 排查：从被挡元素往上找「谁建了上下文」

## 参考答案

### 1. 核心模型

- 文档根是一个层叠上下文。  
- 某个元素创建新上下文后，它的子孙 **先在内部排好**，再作为整体与外部比较。  
- 所以：**不是谁数字大谁就在最上**，而是「你在哪个盒子的楼层里」。

### 2. 常见创建层叠上下文的情况（记高频）

- 根元素  
- `position` 为 `relative/absolute/fixed/sticky` 且 `z-index` 非 `auto`  
- `opacity` 小于 1  
- `transform` / `filter` / `perspective` / `will-change` 为上述等  
- `isolation: isolate`  
- 部分 `flex`/`grid` 子项 `z-index` 非 `auto`  

```css
.card {
  position: relative;
  z-index: 1;          /* 建上下文 */
  transform: translateZ(0); /* 也常建上下文 */
}
```

### 3. 层级约定（业务）

```text
页面内容 < 下拉/ sticky 表头 < 抽屉/模态遮罩 < 模态面板 < Toast/Notification
```

用设计 token：`--z-dropdown: 1000; --z-modal: 2000; --z-toast: 3000;`

### 4. 遇到问题怎么办（逐步排查）

**现象：Modal 里按钮菜单被页面表头盖住，或 `z-index:9999` 无效**

1. **看 DOM 挂载点**：弹层是否在带 `transform` 的布局父级内（侧栏动画、zoom 页面）。  
2. **DevTools**：选中弹层，看 Computed 的 `z-index`、`position`、祖先是否有 `transform/filter/opacity`。  
3. **对比兄弟上下文**：父 A `z-index:1` 与父 B `z-index:2`，A 里孩子写 9999 也赢不了 B。  
4. **修法优先级**：  
   - 弹层 `Teleport`/`createPortal` 到 `body`  
   - 去掉祖先不必要的 `transform`（动画改到内层）  
   - 提高「整层」父级的 z-index，而不是只抬孙子  
   - 统一遮罩与面板同一门户，避免遮罩在下、面板还在旧父级  

```html
<!-- Vue -->
<Teleport to="body">
  <div class="modal" style="z-index: var(--z-modal)">...</div>
</Teleport>
```

```css
/* 危险：父级一开动画，fixed 子级 containing block 也可能变 */
.page { transform: translateX(0); }
.bad-fixed { position: fixed; inset: 0; } /* 可能相对 .page */
```

5. **验收**：滚动页面、打开侧栏动画时弹层仍盖住全屏；多弹层按规范叠放。

**业务例子**：带 `backdrop-filter`/`transform` 的筛选条里写 `position:fixed` 的下拉，会被后渲染的实验台盖住——下拉挂到 body 或去掉父级滤镜。

### 5. 和 fixed 的关系（常一起考）

- 通常 `fixed` 相对视口。  
- 祖先有 `transform`/`filter`/`perspective` 等时，fixed 可能改相对该祖先——弹层「定不准」。  
- 解法同样：门户到 `body`，或避免祖先那些属性。

## 可能追问

- `z-index:auto`？→ 不新建（就这段常见规则而言），按绘制顺序参与。  
- 负 z-index？→ 可能跑到背景后面，注意被父背景盖住。  
- `isolation: isolate`？→ 显式新建上下文，做混合模式/叠层时好控。

## 我的笔记

- 定义：
- 原理：
- 业务例子：
- 可能追问：
