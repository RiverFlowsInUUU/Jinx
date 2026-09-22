<div align="center">

# 🛑 Jinx 去广告规则 · 转换版

**iOS 拦得住的广告，mihomo / Surge 也拦得住**

*上游 Jinx 黑/白名单的格式翻译，规则一条不增不减*

[![Source](https://img.shields.io/badge/Source-Jinx%203.1.9-8250df?style=flat-square)](https://github.com/VME98/jinx-rules)
[![mihomo](https://img.shields.io/badge/mihomo-OpenClash-1f6feb?style=flat-square)](https://github.com/RiverFlowsInUUU/jinx-ads-rules)
[![Surge](https://img.shields.io/badge/Surge-RULE--SET-orange?style=flat-square)](https://github.com/RiverFlowsInUUU/jinx-ads-rules)
[![Rules](https://img.shields.io/badge/Ads-3889-0969da?style=flat-square)](https://github.com/RiverFlowsInUUU/jinx-ads-rules)
[![License](https://img.shields.io/badge/License-%E6%9C%AA%E5%A3%B0%E6%98%8E-critical?style=flat-square)](#-来源与许可)

</div>

## 📥 规则集

🔷 **mihomo / OpenClash**

完整版 · 3889 条

```
https://cdn.jsdelivr.net/gh/RiverFlowsInUUU/jinx-ads-rules@main/mihomo-ads.yaml
```

白名单守卫 · 43 条 · 与完整版配套

```
https://cdn.jsdelivr.net/gh/RiverFlowsInUUU/jinx-ads-rules@main/mihomo-white-guard.yaml
```

🔶 **Surge**

完整版 · 3889 条

```
https://cdn.jsdelivr.net/gh/RiverFlowsInUUU/jinx-ads-rules@main/surge-ads.list
```

白名单守卫 · 43 条 · 与完整版配套

```
https://cdn.jsdelivr.net/gh/RiverFlowsInUUU/jinx-ads-rules@main/surge-white-guard.list
```

守卫 = 上游 325 条白名单中会被黑名单命中的 42 条，加 1 条手工补充。

以上均为 jsDelivr；备选源 `raw.githubusercontent.com/RiverFlowsInUUU/jinx-ads-rules/main/<文件名>`。急用加 `?v=<日期>` 绕开 CDN 缓存。

### 🤝 搭配：AWAvenue-Ads-Rule

独立的第三方去广告规则集，与本文规则集无依赖，可叠加使用 —— Jinx 未收录的广告域由它补齐。

⚠️ 判定标准与 Jinx 不同：叠加后上游 Jinx 白名单中有 8 个域会被它拦掉（实测，随它每日更新的快照浮动）。

本体地址：

🔷 **mihomo / OpenClash** · `Clash-Classical`

```
https://cdn.jsdelivr.net/gh/TG-Twilight/AWAvenue-Ads-Rule@main/Filters/AWAvenue-Ads-Rule-Clash-Classical.yaml
```

🔶 **Surge** · `RULE-SET`

```
https://cdn.jsdelivr.net/gh/TG-Twilight/AWAvenue-Ads-Rule@main/Filters/AWAvenue-Ads-Rule-Surge-RULE-SET.list
```

由 [TG-Twilight/AWAvenue-Ads-Rule](https://github.com/TG-Twilight/AWAvenue-Ads-Rule) 维护（GPL-3.0）· 更多格式见[官方订阅生成器](https://awavenue.top/Sub.html)。

---

## 🔷 mihomo / OpenClash

```yaml
rule-providers:
  jinx-ads:
    type: http
    behavior: classical          # 不用 domain
    format: yaml                 # 文件是顶层 payload 列表
    url: "https://cdn.jsdelivr.net/gh/RiverFlowsInUUU/jinx-ads-rules@main/mihomo-ads.yaml"
    path: ./rule_provider/jinx-ads.yaml
    interval: 86400

  jinx-white-guard:
    type: http
    behavior: classical
    format: yaml
    url: "https://cdn.jsdelivr.net/gh/RiverFlowsInUUU/jinx-ads-rules@main/mihomo-white-guard.yaml"
    path: ./rule_provider/jinx-white-guard.yaml
    interval: 86400

rules:
  - RULE-SET,jinx-white-guard,DIRECT
  - RULE-SET,jinx-ads,REJECT
  # 其余规则接在后面
```

适用 mihomo · OpenClash · Stash · FlClash。`behavior: domain` 对普通域名的匹配范围取决于实现；`classical` 加显式 `DOMAIN-SUFFIX` 语义明确。

---

## 🔶 Surge

```
[Rule]
# 白名单（精确放行）
RULE-SET,https://cdn.jsdelivr.net/gh/RiverFlowsInUUU/jinx-ads-rules@main/surge-white-guard.list,DIRECT
# 广告拦截
RULE-SET,https://cdn.jsdelivr.net/gh/RiverFlowsInUUU/jinx-ads-rules@main/surge-ads.list,REJECT,pre-matching,extended-matching
# 其余规则接在后面
```

| 参数 | 作用 |
|:-----|:-----|
| `pre-matching` | REJECT 提前到 DNS / 连接建立阶段，最接近 Jinx 的系统级拦截 |
| `extended-matching` | 按 TLS SNI / HTTP Host 额外匹配，处理 App 直连 IP 的情况 |

`pre-matching` 仅对 REJECT 系策略生效。

---

## 📋 规则顺序

自上而下，先匹配先赢。

| # | 规则 | 去向 |
|:-:|:-----|:-----|
| 🛡️ | 白名单守卫 | `DIRECT` |
| 🚫 | 广告拦截 | `REJECT` |
| 🇨🇳 | 常规分流（`GEOSITE,cn` / `GEOIP,cn`） | `DIRECT` |

国内广告域名多数同时属于「中国大陆域名」。`GEOSITE,cn` 排在 `REJECT` 之前会先命中放行，广告规则不再有机会执行。

验证：打开一个带广告的 App，面板中出现 `jinx-ads` 命中即顺序正确；只看到 `cn` / `DIRECT` / `Final`，则把 `REJECT` 提前。

---

## 🔄 转换原理

| 上游写法 | 含义 | mihomo | Surge |
|:---------|:-----|:-------|:------|
| `bugly.qq.com` | 该域 + 全部子域 | `DOMAIN-SUFFIX` | `DOMAIN-SUFFIX` |
| `*.cupid.iqiyi.com` | 同上（等价） | `DOMAIN-SUFFIX` | `DOMAIN-SUFFIX` |
| `p*-ad.adkwai.com` | 中缀通配（单级） | `DOMAIN-REGEX` | `DOMAIN-WILDCARD` |
| 白名单 `qq.com` | 仅精确，不继承子域 | `DOMAIN` | `DOMAIN` |

- 两平台唯一差异是 149 条中缀通配 —— mihomo 不支持星号内嵌，改用 `DOMAIN-REGEX`
- `DOMAIN-SUFFIX` 覆盖整个子域树；误杀用白名单守卫放行
- 仅域名级拦截，同域内嵌广告需 MITM / URL 级规则
- 上游 `url_*` / `mitm_skip_domains` 依赖 MITM 上下文，未转换

---

## ⚙️ OpenClash：`绕过中国大陆 IP`

`china_ip_route`（默认常开）把中国大陆域名集写入 `fake-ip-filter`：这些域名解析到真实 IP，防火墙判定目标属大陆后直接放行，**连接不进入内核** —— 规则不生效，日志里也没有记录。国内 App 的广告 / 埋点 SDK 多挂在大厂域名下（`*.volces.com`、`*.bytedns.com`），天然落进该域名集。

```bash
uci set openclash.config.china_ip_route='0'
uci commit openclash
/etc/init.d/openclash restart
```

`fake-ip-filter` 里 NTP / STUN / 局域网等硬编码条目不受影响；域名访问多一跳内核，纯 IP 直连不受影响。回滚：`'0'` → `'1'`。

---

## 📁 文件结构

```
jinx-ads-rules/
├── 🔷 mihomo-*.yaml      # 2 份：完整版 / 白名单守卫
├── 🔶 surge-*.list       # 2 份，与 mihomo 一一对应
├── ✍️ custom-*.list      # 2 份人工维护源（--extra / --extra-white）
└── 🧪 skill/             # 转换脚本 + 方法论
```

`mihomo-*.yaml` 是顶层 `payload` 列表，`surge-*.list` 是 RULE-SET 文本，内容不可互换。`custom-*.list` 是唯一需要手工编辑的文件；生成产物重跑一次即被覆盖。

---

## 📚 来源与许可

| 项 | 值 |
|:---|:---|
| 上游 | [`VME98/jinx-rules`](https://github.com/VME98/jinx-rules) · 数据 `3.1.9` · `2026-09-15` |
| 上游许可 | 未声明（`license: null`） |
| 规则数据 | 版权归上游及其原始来源，不主张任何权利 |
| `skill/` | 转换脚本与方法论，不含上游数据，可自由取用、修改、再分发 |

上游作者或权利人如有异议，开 issue 即下架。

---

## 📖 更多文档

- 📘 [`skill/SKILL.md`](skill/SKILL.md) —— 匹配语义判定 · 通配映射 · 白名单瘦身 · 生成命令
- 🧪 [`skill/scripts/convert_ruleset.py`](skill/scripts/convert_ruleset.py) —— 4 个规则文件的生成脚本
- 🗓️ [`CHANGELOG.md`](CHANGELOG.md) —— 规则集变动记录

---

<div align="center">

数据来自 VME98/jinx-rules · 不主张任何许可

</div>
