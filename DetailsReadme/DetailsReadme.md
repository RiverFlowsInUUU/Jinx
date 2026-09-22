# Jinx 详情

[README](../README.md) 之外的补充材料：不常用的操作、需要展开的解释、会随上游变动的数字。文中数字标注了取值日期。

## 目录

- [📥 1 · 规则集与白名单](#-1-规则集与白名单)
- [🔗 2 · 订阅地址、缓存与生效判据](#-2-订阅地址缓存与生效判据)
- [🤝 3 · 搭配 AWAvenue-Ads-Rule](#-3-搭配-awavenue-ads-rule)
- [📋 4 · 规则顺序](#-4-规则顺序)
- [🔄 5 · 转换原理](#-5-转换原理)
- [⚙️ 6 · OpenClash：绕过中国大陆 IP](#-6-openclash绕过中国大陆-ip)
- [📁 7 · 文件结构](#-7-文件结构)
- [📚 8 · 来源与许可](#-8-来源与许可)

---

## 📥 1 规则集与白名单

| 客户端 | 文件 | 格式 | 条数 | 用途 |
|:-------|:-----|:-----|-----:|:-----|
| mihomo / OpenClash | `mihomo-ads.yaml` | `classical` | 3889 | 黑名单 · 拦截 |
| mihomo / OpenClash | `mihomo-white-guard.yaml` | `classical` | 43 | 白名单 · 放行 |
| Surge | `surge-ads.list` | `RULE-SET` | 3889 | 黑名单 · 拦截 |
| Surge | `surge-white-guard.list` | `RULE-SET` | 43 | 白名单 · 放行 |

**白名单怎么来的**：上游白名单（325 条）中会被黑名单命中的 **42 条**，加 **1 条**手工补充（`*.tange365.com`，「小鲸看看」相机 App 的账户 / 设备 / 云存储域），共 43 条。

白名单的对照面是**上游黑名单** —— 生成时不把 `custom-*.list` 算进去，所以手工追加的域名**不会**因为「上游已放行」而被白名单豁免。跟上游白名单对着干等于静默误杀，这条前提见 [`skill/SKILL.md`](../skill/SKILL.md)。

---

## 🔗 2 订阅地址、缓存与生效判据

两个源内容完全一致，路径一一对应，**只换前缀**：

| 源 | 前缀 | 特点 |
|:---|:-----|:-----|
| Raw GitHub | `raw.githubusercontent.com/RiverFlowsInUUU/Jinx/main/` | 官方直读源，不经第三方 CDN；文件增删改名后与仓库一致、删文件无需 purge。**国内常被墙。** |
| jsDelivr | `cdn.jsdelivr.net/gh/RiverFlowsInUUU/Jinx@main/` | 国内直连更稳；多一层第三方缓存，删文件后不 purge 仍返回旧内容。 |

**缓存与生效判据**（2026-09-22 实测）：

- `raw` 自己也有边缘缓存 —— 推送后约 **3 分钟**才返回新内容，且 `?v=<日期>`、`Cache-Control: no-cache` 对它**都无效**。别拿 raw 当「已生效」的判据。
- jsDelivr 缓存更厚。急用加 `?v=<日期>`，或走 purge 接口：
  `https://purge.jsdelivr.net/gh/RiverFlowsInUUU/Jinx@main/<文件>` —— 返回 `"status": "finished"` 即生效。
- **判断「是否生效」的权威判据只有 GitHub Contents API**（直读 git 对象，不过 CDN）：
  `GET /repos/RiverFlowsInUUU/Jinx/contents/<路径>?ref=main` → base64 解码后比对本地 md5。
  中文路径要 `urllib.parse.quote`。raw / jsDelivr 的滞后**不等于**推送失败。

---

## 🤝 3 搭配 AWAvenue-Ads-Rule

**AWAvenue 秋风广告规则** —— 独立的第三方去广告规则集，与本文规则集无依赖，可叠加使用，Jinx 未收录的广告域由它补齐。

**判定标准与 Jinx 不同**：叠加后上游 Jinx 白名单中有 **8 个域**会被它拦掉（2026-09-22 实测，随它每日快照浮动）。这几个域需要放行的话，把 AWAvenue 的规则排到 Jinx 白名单**之后**。

**只给 Raw 源**：它由对方托管，缓存我们 purge 不了 —— 列一个 jsDelivr 备用等于把别人的缓存层写进本文档，出问题也解释不清。

**要 `RULE-SET`，不要裸域名版**：`Filters/` 下另有一份 `AWAvenue-Ads-Rule-Surge.list`，那是**裸域名**格式（`.8le8le.com` 这类带前导点，DOMAIN-SET 语义），与 `RULE-SET` 的消费方式不匹配。两份条数也不同：裸域名版 **961** 条，`RULE-SET` 版 **965** 条 —— 差额正好是它写不出的 4 条 `DOMAIN-KEYWORD`（`-ad.sm.cn`、`-ad.video.yximgs.com`、`-ad.wtzw.com`、`-be-pack-sign.pglstatp-toutiao.com`，子串匹配，无裸域名等价形式）。

条数以它文件头的 `#Total lines` 为准（2026-09-22 为 v1.7.8：`RULE-SET` 965 / 裸域名 961 / `Clash-Classical` 965）。上游每日更新，**别用自己数的行数去否定它的自报值**。

由 [TG-Twilight/AWAvenue-Ads-Rule](https://github.com/TG-Twilight/AWAvenue-Ads-Rule) 维护（GPL-3.0）· 更多格式见[官方订阅生成器](https://awavenue.top/Sub.html)。

---

## 📋 4 规则顺序

自上而下，先匹配先赢。

| 顺序 | 规则 | 去向 |
|:-:|:-----|:-----|
| 1 | 白名单 | `DIRECT` |
| 2 | 广告拦截 | `REJECT` |
| 3 | 常规分流（`GEOSITE,cn` / `GEOIP,cn`） | `DIRECT` |

国内广告域名多数同时属于「中国大陆域名」。`GEOSITE,cn` 排在 `REJECT` 之前会先命中放行，广告规则不再有机会执行。

**验证**：打开一个带广告的 App，面板中出现 `jinx-ads` 命中即顺序正确；只看到 `cn` / `DIRECT` / `Final`，则把 `REJECT` 提前。

---

## 🔄 5 转换原理

| 上游写法 | 含义 | mihomo | Surge |
|:---------|:-----|:-------|:------|
| `bugly.qq.com` | 该域 + 全部子域 | `DOMAIN-SUFFIX` | `DOMAIN-SUFFIX` |
| `*.cupid.iqiyi.com` | 同上（等价） | `DOMAIN-SUFFIX` | `DOMAIN-SUFFIX` |
| `p*-ad.adkwai.com` | 中缀通配（单级） | `DOMAIN-REGEX` | `DOMAIN-WILDCARD` |
| 上游白名单 `qq.com` | 仅精确，不继承子域 | `DOMAIN` | `DOMAIN` |

- 两平台唯一差异是 **149 条中缀通配** —— mihomo 不支持星号内嵌，改用 `DOMAIN-REGEX`。
- `DOMAIN-SUFFIX` 覆盖整个子域树；误杀用白名单放行。
- 仅域名级拦截，同域内嵌广告需 MITM / URL 级规则。
- 上游 `url_*` / `mitm_skip_domains` 依赖 MITM 上下文，未转换。

---

## ⚙️ 6 OpenClash：绕过中国大陆 IP

`china_ip_route`（默认常开）把中国大陆域名集写入 `fake-ip-filter`：这些域名解析到真实 IP，防火墙判定目标属大陆后直接放行，**连接不进入内核** —— 规则不生效，日志里也没有记录。国内 App 的广告 / 埋点 SDK 多挂在大厂域名下（`*.volces.com`、`*.bytedns.com`），天然落进该域名集。

关闭：

```bash
uci set openclash.config.china_ip_route='0'
uci commit openclash
/etc/init.d/openclash restart
```

`fake-ip-filter` 里 NTP / STUN / 局域网等硬编码条目不受影响；域名访问多一跳内核，纯 IP 直连不受影响。回滚：`'0'` → `'1'`。

---

## 📁 7 文件结构

```
Jinx/
├── mihomo-*.yaml      # 2 份：黑名单 / 白名单
├── surge-*.list       # 2 份，与 mihomo 一一对应
├── custom-*.list      # 2 份人工维护源（--extra / --extra-white）
├── skill/             # 转换脚本 + 方法论
└── DetailsReadme/     # 本文档
```

`mihomo-*.yaml` 是顶层 `payload` 列表，`surge-*.list` 是 RULE-SET 文本，**内容不可互换**。`custom-*.list` 是唯一需要手工编辑的文件；生成产物重跑一次即被覆盖。

---

## 📚 8 来源与许可

| 项 | 值 |
|:---|:---|
| 上游 | [`VME98/jinx-rules`](https://github.com/VME98/jinx-rules) · 数据 `3.1.9` · `2026-09-15` |
| 上游许可 | 未声明（`license: null`） |
| 规则数据 | 版权归上游及其原始来源，不主张任何权利 |
| `skill/` | 转换脚本与方法论，不含上游数据，可自由取用、修改、再分发 |

上游作者或权利人如有异议，开 issue 即下架。

---

[← 回到 README](../README.md)
