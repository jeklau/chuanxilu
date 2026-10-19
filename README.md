# 传习录白话译注

王阳明《传习录》全本白话译注阅读站，共 343 条：

- **卷上** 129 条（徐爱录、陆澄录、薛侃录），附徐爱引言、徐爱跋
- **卷中** 71 条（答顾东桥、周道通、陆原静、欧阳崇一、罗整庵、聂文蔚诸书，训蒙大意，教约），附钱德洪序、答原静书后按语
- **卷下** 143 条（陈九川、黄直、黄修易、黄省曾、钱德洪、黄以方录），附钱德洪跋

条目编号依陈荣捷《王阳明传习录详注集评》。每条包括：校勘后的原文、白话、注释、今天怎么用、自测题、参看条目、与底本的校勘记录；86 条争议较大的条目附「反方怎么驳」。手机优先排版，支持深色模式、字号调节、全文搜索、间隔复习，部署后可离线阅读、添加到主屏幕。

## 部署到 Cloudflare Workers

`public/` 已经是构建好的成品，部署时不需要再构建。

### 方式一：在 Cloudflare 控制台连接这个仓库（推荐）

1. Cloudflare 控制台 → **Workers & Pages** → **Create** → **Import a repository**
2. 授权 GitHub，选择这个仓库
3. 构建设置：
   - Build command：留空
   - Deploy command：`npx wrangler deploy`
4. 保存并部署。以后每次 push 到 `main`，Cloudflare 会自动重新部署。

### 方式二：本地命令行

```bash
npm install
npx wrangler login
npm run deploy
```

部署完成后地址是 `https://chuanxilu.<你的子域>.workers.dev`。

### 绑定自己的域名

在 `wrangler.jsonc` 里加上（域名需已托管在同一个 Cloudflare 账号下）：

```jsonc
"routes": [{ "pattern": "cxl.example.com", "custom_domain": true }]
```

## 目录

```
public/            网站成品（部署的就是这个目录）
  index.html       阅读器 + 全部数据
  sw.js            离线缓存
  manifest.webmanifest, icon.*
data/
  juan1_raw.json   卷上底本原文（殆知阁 OCR 文本，按条切分）
  juan2_raw.json   卷中底本原文（已按陈荣捷编号拆分第 179/180 条）
  juan3_raw.json   卷下底本原文（按底本顺序，141 条）
  juan3_raw_n.json 卷下底本按陈荣捷编号重排（拆 228/229，补 316）
  b01–b06.json     卷上译注源文件
  b07–b12.json     卷下译注源文件（b12 含钱德洪跋）
  b13–b22.json     卷中译注源文件（b13 含钱德洪序，b18 含答原静书按语）
  all.json         合并后的数据（构建产物）
src/
  template.html    页面模板
  sw.js            Service Worker 模板
tools/
  check.py         把译注原文与底本逐字比对，列出所有改动
  build_data.py    合并条目、生成校勘记录
  build_site.py    把数据嵌入模板，输出 public/
wrangler.jsonc     Workers 配置（仅静态资源）
```

## 修改或加卷

```bash
npm run check      # 看每条与底本的差异
npm run build      # 重新生成 public/
```

条目字段：`n` 编号，`t` 标题，`yw` 原文，`bh` 白话，`zs` 注释 `[[词, 解释]]`，`gl` 参看条目编号，`q`/`a` 自测问答，`yong` 今天怎么用，`con` 反方驳论（可选）。

## 底本与说明

- 原文底本：殆知阁古籍库公版《传习录》（OCR 文本，错字较多，已依通行本校改：卷上 235 处、卷中 704 处、卷下 388 处，每处均在页面「校勘」中列出）
- 条目编号：依陈荣捷《王阳明传习录详注集评》
- 白话、注释、反方、自测题由 AI 撰写，并非出版译本，引用请核对纸本
- 阅读进度保存在浏览器本地，不上传，不跨设备同步
