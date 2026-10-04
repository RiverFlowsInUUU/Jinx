# 📘 Jinx 详情

📖 本文是 [README](../README.md) 之外的补充材料：不常用的操作、需要展开的解释、会随上游变动的数字。文中数字标注了取值日期。

## 📑 目录

- [📥 1 · 规则集与白名单](#-1-规则集与白名单)
- [🔗 2 · 订阅地址、缓存与生效判据](#-2-订阅地址缓存与生效判据)
- [🤝 3 · 搭配 AWAvenue-Ads-Rule](#-3-搭配-awavenue-ads-rule)
- [📋 4 · 规则顺序](#-4-规则顺序)
- [🔄 5 · 转换原理](#-5-转换原理)
- [🚧 6 · OpenClash：绕过中国大陆 IP](#-6-openclash绕过中国大陆-ip)
- [📁 7 · 文件结构](#-7-文件结构)
- [📚 8 · 来源与许可](#-8-来源与许可)
- [✅ 9 · 一致性保证与验收](#-9-一致性保证与验收)

---

## 📥 1 规则集与白名单

| 客户端 | 文件 | 格式 | 条数 | 用途 |
|:-------|:-----|:-----|-----:|:-----|
| mihomo / OpenClash | `mihomo-ads.yaml` | `classical` | 3889 | 黑名单 · 拦截 |
| mihomo / OpenClash | `mihomo-white-guard.yaml` | `classical` | 44 | 白名单 · 放行 |
| Surge | `surge-ads.list` | `RULE-SET` | 3889 | 黑名单 · 拦截 |
| Surge | `surge-white-guard.list` | `RULE-SET` | 44 | 白名单 · 放行 |
| Egern | `surge-ads.list` · `surge-white-guard.list` | `rule_set` | 3889 / 44 | 黑名单 / 白名单 · **直接复用** |
| sing-box | `sing-box-ads.json` | `source` | 3889 | 黑名单 · 拦截 |
| sing-box | `sing-box-white-guard.json` | `source` | 44 | 白名单 · 放行 |

🔵 **Egern 无独立产物**：它的规则集格式与 Surge 同源（`DOMAIN-SUFFIX` / `DOMAIN-WILDCARD` 逐字相同），直接引用 `surge-*.list` 即可 —— 引用位置有两处：`rules` 段的 `rule_set`（连接阶段）与 `forward` 段的 `proxy_rule_set`（DNS 阶段）。依据：姊妹仓 [Self-Configuration](https://github.com/RiverFlowsInUUU/Self-Configuration) 的四份现役 Egern profile 全部这样引用，并把这两份登记为「共用规则集」。

🧩 **白名单怎么来的**：上游白名单（325 条）中会被黑名单命中的 **42 条**，加 **2 条**手工补充（`*.tange365.com`，「小鲸看看」相机 App 的账户 / 设备 / 云存储域；`*.wechatos.net`，用户指定放行），共 44 条。

⚖️ 白名单的对照面是**上游黑名单** —— 生成时不把 `custom-*.list` 算进去，所以手工追加的域名**不会**因为「上游已放行」而被白名单豁免。跟上游白名单对着干等于静默误杀，这条前提见 [`skill/SKILL.md`](../skill/SKILL.md)。

---

## 🔗 2 订阅地址、缓存与生效判据

🔀 两个源内容完全一致，路径一一对应，**只换前缀**：

| 源 | 前缀 | 特点 |
|:---|:-----|:-----|
| Raw GitHub | `raw.githubusercontent.com/RiverFlowsInUUU/Jinx/main/` | 官方直读源，不经第三方 CDN；文件增删改名后与仓库一致、删文件无需 purge。**国内常被墙。** |
| jsDelivr | `cdn.jsdelivr.net/gh/RiverFlowsInUUU/Jinx@main/` | 国内直连更稳；多一层第三方缓存，删文件后不 purge 仍返回旧内容。 |

⏱️ **缓存与生效判据**（2026-09-22 实测）：

- ⏳ `raw` 自己也有边缘缓存 —— 推送后约 **3 分钟**才返回新内容，且 `?v=<日期>`、`Cache-Control: no-cache` 对它**都无效**。别拿 raw 当「已生效」的判据。
- 🧊 jsDelivr 缓存更厚。急用加 `?v=<日期>`，或走 purge 接口：
  `https://purge.jsdelivr.net/gh/RiverFlowsInUUU/Jinx@main/<文件>` —— 返回 `"status": "finished"` 即生效。
- 🔍 **判断「是否生效」的权威判据只有 GitHub Contents API**（直读 git 对象，不过 CDN）：
  `GET /repos/RiverFlowsInUUU/Jinx/contents/<路径>?ref=main` → base64 解码后比对本地 md5。
  中文路径要 `urllib.parse.quote`。raw / jsDelivr 的滞后**不等于**推送失败。

---

## 🤝 3 搭配 AWAvenue-Ads-Rule

➕ **AWAvenue 秋风广告规则** —— 独立的第三方去广告规则集，与本文规则集无依赖，可叠加使用，Jinx 未收录的广告域由它补齐。

⚠️ **判定标准与 Jinx 不同**：叠加后上游 Jinx 白名单中有 **8 个域**会被它拦掉（2026-09-22 实测，随它每日快照浮动）。这几个域需要放行的话，把 AWAvenue 的规则排到 Jinx 白名单**之后**。

📎 **只给 Raw 源**：它由对方托管，缓存我们 purge 不了 —— 列一个 jsDelivr 备用等于把别人的缓存层写进本文档，出问题也解释不清。

📌 **要 `RULE-SET`，不要裸域名版**：`Filters/` 下另有一份 `AWAvenue-Ads-Rule-Surge.list`，那是**裸域名**格式（`.8le8le.com` 这类带前导点，DOMAIN-SET 语义），与 `RULE-SET` 的消费方式不匹配。两份条数也不同：裸域名版 **961** 条，`RULE-SET` 版 **965** 条 —— 差额正好是它写不出的 4 条 `DOMAIN-KEYWORD`（`-ad.sm.cn`、`-ad.video.yximgs.com`、`-ad.wtzw.com`、`-be-pack-sign.pglstatp-toutiao.com`，子串匹配，无裸域名等价形式）。

🔢 条数以它文件头的 `#Total lines` 为准（2026-09-22 为 v1.7.8：`RULE-SET` 965 / 裸域名 961 / `Clash-Classical` 965）。上游每日更新，**别用自己数的行数去否定它的自报值**。

🔵 **sing-box 侧用官方现成的 `AWAvenue-Ads-Rule-Singbox.json`**（2026-09-28 实测）：

- 📐 它已是 rule-set 的 **source 格式**（`version: 3`，1.14.2 内核 `rule-set compile` 验证兼容），订阅即用，与「不用 `.srs`」的口径一致。
- 🔍 条数 965 与 `RULE-SET` 版同源：`domain` 949 + `domain_suffix` 12 + `domain_keyword` 4 —— 4 条关键词规则（`-ad.sm.cn` 等）在 sing-box 里有原生 `domain_keyword` 字段，无转换损失。
- 🚫 本仓不镜像这份文件：官方每日更新，快照必然滞后，且官方已是目标格式、镜像无加工价值 —— 与 Jinx 侧「格式转换镜像」的定位不同。订阅直接用官方 Raw 地址。

🔗 由 [TG-Twilight/AWAvenue-Ads-Rule](https://github.com/TG-Twilight/AWAvenue-Ads-Rule) 维护（GPL-3.0）· 更多格式见[官方订阅生成器](https://awavenue.top/Sub.html)。

---

## 📋 4 规则顺序

🔽 自上而下，先匹配先赢。

| 顺序 | 规则 | 去向 |
|:-:|:-----|:-----|
| 1 | 🛡️ 白名单 | `DIRECT` |
| 2 | 🚫 广告拦截 | `REJECT` |
| 3 | 🚦 常规分流（`GEOSITE,cn` / `GEOIP,cn`） | `DIRECT` |

⚠️ 国内广告域名多数同时属于「中国大陆域名」。`GEOSITE,cn` 排在 `REJECT` 之前会先命中放行，广告规则不再有机会执行。

✅ **验证**：打开一个带广告的 App，面板中出现 `jinx-ads` 命中即顺序正确；只看到 `cn` / `DIRECT` / `Final`，则把 `REJECT` 提前。

---

## 🔄 5 转换原理

| 上游写法 | 含义 | mihomo | Surge | Egern | sing-box |
|:---------|:-----|:-------|:------|:------|:---------|
| `bugly.qq.com` | 该域 + 全部子域 | `DOMAIN-SUFFIX` | `DOMAIN-SUFFIX` | 同 Surge | `domain_suffix` |
| `*.cupid.iqiyi.com` | 同上（等价） | `DOMAIN-SUFFIX` | `DOMAIN-SUFFIX` | 同 Surge | `domain_suffix` |
| `p*-ad.adkwai.com` | 中缀通配（单级） | `DOMAIN-REGEX` | `DOMAIN-WILDCARD` | 同 Surge | `domain_regex` |
| 上游白名单 `qq.com` | 仅精确，不继承子域 | `DOMAIN` | `DOMAIN` | 同 Surge | `domain` |

- 🎯 **各端唯一差异在 149 条中缀通配的写法** —— Surge 与 Egern 都用 `DOMAIN-WILDCARD`；mihomo 不支持星号内嵌，改写成 `DOMAIN-REGEX`；sing-box 落在 `domain_regex`（同为 Go RE2 正则，转换式与 mihomo 一致）。域名后缀与精确匹配两类，四端语义完全对齐。
- 🌳 `DOMAIN-SUFFIX` / `domain_suffix` 覆盖整个子域树；误杀用白名单放行。
- 🧱 仅域名级拦截，同域内嵌广告需 MITM / URL 级规则。
- ⏭️ 上游 `url_*` / `mitm_skip_domains` 依赖 MITM 上下文，未转换。

🔬 **sing-box 侧的语义实证**（内核 1.14.2 · 2026-09-28）：

- 📐 `domain_suffix: ["example.com"]`（不带点）命中自身 + 全部子域，**域段级边界**（`aexample.com` 不误命中）—— 实证 `sagernet/sing` 的 `common/domain/matcher.go`：trie 按「`.` 段边界 + 叶子」判定，与 mihomo `DOMAIN-SUFFIX` 等价；前导点写法 `.example.com` 才是「仅子域、不含自身」，本仓不用。
- 🧊 文件是 rule-set 的 **source 格式**（JSON，`"version": 5`），不是二进制 `.srs` —— 远程规则集 `format: "source"` 直接消费，订阅即用无需本地编译；官方文档明确 `.json` 扩展名下 `format` 可省略，本仓配置示例仍显式写出。
- 🔍 `sing-box rule-set compile` 可把 JSON 编译成 `.srs`（本仓不用，仅作格式校验）；编译时 trie 会把 **17 条重复条目折叠**（上游同时存在 `*.x.com` 与 `x.com`，转换后同值），与 mihomo / Surge 侧保留重复行同源 —— 重复匹配无副作用，三平台条目口径保持一致。compile → decompile 回读：`domain_suffix` 3740 → 3723（去重后唯一值）、`domain_regex` 149 / `domain` 41 逐条一致。

---

## 🚧 6 OpenClash：绕过中国大陆 IP

📌 `china_ip_route`（默认常开）把中国大陆域名集写入 `fake-ip-filter`：这些域名解析到真实 IP，防火墙判定目标属大陆后直接放行，**连接不进入内核** —— 规则不生效，日志里也没有记录。国内 App 的广告 / 埋点 SDK 多挂在大厂域名下（`*.volces.com`、`*.bytedns.com`），天然落进该域名集。

关闭：

```bash
uci set openclash.config.china_ip_route='0'
uci commit openclash
/etc/init.d/openclash restart
```

📎 `fake-ip-filter` 里 NTP / STUN / 局域网等硬编码条目不受影响；域名访问多一跳内核，纯 IP 直连不受影响。回滚：`'0'` → `'1'`。

---

## 📁 7 文件结构

```
Jinx/
├── 🔷 mihomo-*.yaml    # 2 份：黑名单 / 白名单
├── 🔶 surge-*.list     # 2 份，与 mihomo 一一对应
├── 🔵 sing-box-*.json  # 2 份，与 mihomo 一一对应（rule-set source 格式）
├── 📝 custom-*.list    # 2 份人工维护源（--extra / --extra-white）
├── 🧪 skill/           # 转换脚本 + 方法论 + 验收闸门
│   ├── 📄 scripts/     # convert_ruleset.py —— 六份产物的唯一生成入口
│   └── ✅ tests/       # verify_jinx_src.py（9 段断言）· selftest_negative.py（负样本）
├── 🔁 .github/         # CI：每次提交自动跑上述两个脚本
├── 📐 .gitattributes   # 全仓文本 eol=lf（跨平台产物逐字节可复现）
└── 📁 DetailsReadme/   # 本文档
```

📌 `mihomo-*.yaml` 是顶层 `payload` 列表，`surge-*.list` 是 RULE-SET 文本，`sing-box-*.json` 是 rule-set source 格式，**内容不可互换**。`custom-*.list` 是唯一需要手工编辑的文件；生成产物重跑一次即被覆盖。

---

## ✅ 9 一致性保证与验收

🧱 本仓对外只承诺一件事：**六份文件内容等价、规则一条不增不减**。它由 `.github/workflows/ci.yml` 在每次 push / PR 自动校验，闸门是 [`skill/tests/verify_jinx_src.py`](../skill/tests/verify_jinx_src.py)（9 段 · 50 项断言）：

| 段 | 守什么 |
|:-:|:-------|
| 1 | 六份产物存在且非空 |
| 2 | 三格式条数一致（ads 三份互等 / white-guard 三份互等） |
| 3 | **跨格式逐条语义等价** —— 归一化后比对，不是只比条数 |
| 4 | 文件头 `# entries` 自述 == 实际条数 |
| 5 | README / DetailsReadme 的条数声明 == 文件实际 |
| 6 | **产物 == 源头重跑的结果**（防手改产物、防改了源头忘了重跑） |
| 7 | `custom-*.list` 的表头声明与实际条数一致，且每条都真的落进产物 |
| 8 | 文案规范：emoji 只在行首结构位 + 密度下限 |
| 9 | 行尾符与 BOM |

🔢 退出码沿用姊妹仓的四态协议：`0` 过 / `1` 判负 / `2` 环境不达标 / `3` SKIP。**SKIP 用独立码 3，不借 0 蒙混** —— 姊妹仓记录过一次事故：SKIP 与「环境不达标」并成同码，导致汇总脚本把环境故障吞成 SKIP、以 exit 0 假绿。

🧷 第 6 段需要上游源文件（`jinx-rules/`），CI 会先下载再跑，故 CI 上该段**真正执行**；本地裸跑显示 SKIP 属正常。

⚠️ 闸门自身也可能退化。`selftest_negative.py` 专治这个：它在临时副本仓里制造 6 种典型错误（手改产物 / 只改表头 / 跨格式差异 / 文档漂移 / 源头改了没重跑 / emoji 违规），要求闸门**逐一判负**，有漏报即判负。一个只会全绿的闸门与没有闸门等价 —— 这是本仓踩过的「永远绿的空操作」教训。

📐 编写期该自测当场抓出两个真 bug，留痕备查：① 第 6 段比对时 `--src` 写法差异（ads 线用 `jinx-rules`、white-guard 线用 `./jinx-rules`，**因为它原样进表头**）会被误报成内容差异；② emoji 判定把 `U+2B00-2BFF` 整段当箭头排除，而 `U+2B50`（五角星形符号）正住在那段里 —— 导致句中 emoji 静默漏报。

📏 **行尾统一（2026-10-04 修复）**：产物此前在仓库内**行尾分裂** —— mihomo / Surge 四份是 CRLF、sing-box 两份是 LF。根因是 `convert_ruleset.py` 用 `write_text(text)` 写出，而 Python 的通用换行转换会把 `\n` 按平台写成 `os.linesep`：**Windows 出 CRLF、Linux 出 LF，同一脚本跨平台产出不同字节**。这导致 CI 在 Linux 上重跑生成必得 LF、与仓库内的 CRLF 不符，第 6 段当场判负。

处置两条腿，缺一不可：① 脚本改为 `write_text(..., newline='')` 显式钉死 LF（根治产出）；② 新增 `.gitattributes` 声明全仓文本 `eol=lf`（根治检出与提交）。六份产物已按新脚本重跑，**仅行尾变化、内容零改动**（逐字节归一化比对验证）。

📌 规则集按行解析、客户端都会 trim 行尾，故 CRLF 与 LF 对功能等价 —— 归一化只为「跨平台产物逐字节可复现」这一工程目标，不改任何语义。

---

## 📚 8 来源与许可

| 项 | 值 |
|:---|:---|
| 📦 上游 | [`VME98/jinx-rules`](https://github.com/VME98/jinx-rules) · 数据 `3.1.9` · `2026-09-15` |
| ⚖️ 上游许可 | 未声明（`license: null`） |
| 📄 规则数据 | 版权归上游及其原始来源，不主张任何权利 |
| 🧪 `skill/` | 转换脚本与方法论，不含上游数据，可自由取用、修改、再分发 |

📮 上游作者或权利人如有异议，开 issue 即下架。

---

[🏠 回到 README](../README.md)
