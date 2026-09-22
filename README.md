<div align="center">

# 🛑 Jinx 去广告规则 · 转换版

**让 iOS 拦得住的广告，在 mihomo / Surge 上也拦得住**

*不是原创规则 —— 上游 Jinx 黑/白名单的语法翻译件，不增删一条规则*

[![Source](https://img.shields.io/badge/Source-Jinx%203.1.9-8250df?style=flat-square)](https://github.com/VME98/jinx-rules)
[![mihomo](https://img.shields.io/badge/mihomo-OpenClash-1f6feb?style=flat-square)](https://github.com/RiverFlowsInUUU/jinx-ads-rules)
[![Surge](https://img.shields.io/badge/Surge-RULE--SET-orange?style=flat-square)](https://github.com/RiverFlowsInUUU/jinx-ads-rules)
[![Rules](https://img.shields.io/badge/Ads-3891%20%7C%203838-0969da?style=flat-square)](https://github.com/RiverFlowsInUUU/jinx-ads-rules)
[![License](https://img.shields.io/badge/License-%E6%9C%AA%E5%A3%B0%E6%98%8E-critical?style=flat-square)](#-来源与许可)

</div>

## 📥 两份文件

🔷 **mihomo / OpenClash** · 配 `behavior: classical` + `format: yaml`

```
https://cdn.jsdelivr.net/gh/RiverFlowsInUUU/jinx-ads-rules@main/mihomo-ads.yaml
```

🔶 **Surge** · `RULE-SET` 直接引用

```
https://cdn.jsdelivr.net/gh/RiverFlowsInUUU/jinx-ads-rules@main/surge-ads.list
```

顺序是**生死线**：白名单 → REJECT → 你原有的分流规则。

> 🩹 mihomo 侧已于 2026-09-22 从 `.list` 改为 **`.yaml`**，旧地址失效，见 [§版本修正](#-版本修正)。
>
> 📚 前缀二选一：`cdn.jsdelivr.net/gh/RiverFlowsInUUU/jinx-ads-rules@main/`（推荐）或 `raw.githubusercontent.com/RiverFlowsInUUU/jinx-ads-rules/main/`。急用加 `?v=<日期>` 绕开 CDN 缓存。

---

## 🎯 该选哪个

判据只有一条：**你客户端里有没有同时跑 `AWAvenue-Ads-Rule`？**

| 情况 | mihomo | Surge |
|:-----|:-------|:------|
| 没有 / 不确定 | `mihomo-ads.yaml` ⭐ | `surge-ads.list` ⭐ |
| 有 AWAvenue | `mihomo-ads-delta.yaml` | `surge-ads-delta.list` |

- 📉 差集只少 **53 条** —— 除非确定 AWAvenue 在跑，否则直接用完整版
- 🛡️ 白名单守卫（43 条）建议加 —— 上游 325 条里只有 **42 条**真会被这套黑名单误杀
- ⚠️ `custom-*.list` 是**源文件不是规则集**，不要直接引用

---

## 🔷 mihomo / OpenClash

```yaml
rule-providers:
  jinx-ads:
    type: http
    behavior: classical          # ⚠️ 必须 classical，不要用 domain
    format: yaml                 # 文件是顶层 payload 列表；写 text 会解析失败
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
  - RULE-SET,jinx-white-guard,DIRECT   # ① 白名单必须在 REJECT 之前
  - RULE-SET,jinx-ads,REJECT           # ② 广告拦截
  # - GEOSITE,cn,DIRECT ...            # ③ 你原有的规则接在后面
```

适用 mihomo · OpenClash · Stash · FlClash。

---

## 🔶 Surge

```
[Rule]
# ① 白名单（精确放行）
RULE-SET,https://cdn.jsdelivr.net/gh/RiverFlowsInUUU/jinx-ads-rules@main/surge-white-guard.list,DIRECT
# ② 广告拦截
RULE-SET,https://cdn.jsdelivr.net/gh/RiverFlowsInUUU/jinx-ads-rules@main/surge-ads.list,REJECT,pre-matching,extended-matching
# ③ 你自己的规则接在后面
```

| 参数 | 作用 |
|:-----|:-----|
| `pre-matching` | REJECT 提前到 DNS / 连接阶段生效，最接近 Jinx 的系统级体验 |
| `extended-matching` | 按 TLS SNI / HTTP Host 兜底匹配，专治 App 直连 IP |

> ⚠️ `pre-matching` **只能跟 REJECT 系策略用** —— 白名单那行不要写。

---

## 📋 规则顺序

自上而下、先匹配先赢。你机器上 99% 的国内广告域名，同时也属于「中国大陆域名」。

```
❌ 顺序错                             ✅ 顺序对
GEOSITE,cn,DIRECT     ← 先命中放行    RULE-SET,jinx-white-guard,DIRECT
RULE-SET,jinx-ads,REJECT ← 轮不到     RULE-SET,jinx-ads,REJECT
                                      GEOSITE,cn,DIRECT
```

土办法验证：开一个本来有广告的 App，看面板规则命中 —— 看到 `jinx-ads` 命中即顺序对。

---

## 🚨 OpenClash：一个开关让规则静默失效

规则接好了，日志里也看得到 `match RuleSet(jinx-ads) using REJECT`，但部分广告照旧 —— 漏掉的那些域名日志里**一条记录都没有**。

根因是 `绕过中国大陆 IP`（`china_ip_route`，默认常开）：它把「中国大陆域名集」塞进 `fake-ip-filter`，这些域名 DNS 返回真实 IP，防火墙判定目标属大陆直接 return，**连接根本没进内核**。国内 App 的广告 SDK 多挂在大厂域名下（`*.volces.com`、`*.bytedns.com`），天然落进这个集合。

```bash
uci set openclash.config.china_ip_route='0'
uci commit openclash
/etc/init.d/openclash restart
```

- ✅ NTP / STUN / 局域网等硬编码条目不受影响
- ⚖️ 副作用：域名访问多一跳内核，纯 IP 直连不受影响
- ↩️ 回滚：把 `'0'` 改回 `'1'` + commit + restart

---

## 🔄 转换原理

| 上游写法 | 含义 | mihomo | Surge |
|:---------|:-----|:-------|:------|
| `bugly.qq.com` | 该域 + **全部子域** | `DOMAIN-SUFFIX` | `DOMAIN-SUFFIX` |
| `p*-ad.adkwai.com` | 中缀通配 | `DOMAIN-REGEX` | `DOMAIN-WILDCARD` |
| 白名单 `qq.com` | **仅精确**，不继承子域 | `DOMAIN` | `DOMAIN` |

- 🔍 两平台唯一差异是 149 条中缀通配 —— mihomo 不支持星号内嵌，改用 `DOMAIN-REGEX`
- 🚫 `url_*` / `mitm_skip_domains` 依赖 MITM 上下文，未转换

---

## 📁 文件结构

```
jinx-ads-rules/
├── 🔷 mihomo-*.yaml      # 3 份：完整版 3891 / 差集版 3838 / 白名单守卫 43
├── 🔶 surge-*.list       # 3 份，与 mihomo 一一对应
├── ✍️ custom-*.list      # 2 份人工维护源（--extra / --extra-white）
└── 🧪 skill/             # 转换脚本 + 完整方法论
```

> 📐 **后缀即格式**：`mihomo-*.yaml` 是顶层 `payload` 列表，`surge-*.list` 是 RULE-SET 文本，内容**不可互换**。
>
> ✍️ `custom-*.list` 是唯一需要人手改的文件；生成产物重跑一次即被完全覆盖，**不要手改**。

---

## ⚠️ 已知坑

| | 坑 | 说明 |
|:-:|:---|:-----|
| 🥇 | 顺序 | 白名单 → REJECT → `GEOSITE,cn`。「配了但广告还在」的头号原因 |
| 🪃 | OpenClash 前置开关 | 见上节 —— 静默失效，日志看不出异常 |
| 🌐 | 超广通配 | `ad.*`、`pangolin*` 这类一条覆盖几百条的规则 |
| 🧱 | 只做域名级拦截 | 同域内嵌广告需 MITM / URL 级规则 |
| 🎯 | `DOMAIN-SUFFIX` 面大 | 为复刻 Jinx 行为；误杀用白名单加回，别改回精确 |

---

## 🩹 版本修正

| 日期 | 修正 |
|:-----|:-----|
| 2026-09-22 | mihomo 侧 `.list` → **`.yaml`**，内容改为顶层 `payload` 列表。**旧地址已失效** |
| 2026-09-19 | 普通域名从 `DOMAIN` 改回 `DOMAIN-SUFFIX`（Jinx 是后缀匹配），拦截覆盖率 93% → 100% |

---

## 📄 来源与许可

| 项 | 说明 |
|:---|:-----|
| 上游 | [`VME98/jinx-rules`](https://github.com/VME98/jinx-rules) · `3.1.9` · `2026-09-15` |
| 上游许可 | **`license: null`** —— 未声明任何 License |
| 本仓库 | **同样不主张任何许可**。这是对公开数据的格式翻译，不是我的作品 |
| 下架承诺 | 上游作者若认为不妥，开 issue 或联系我，**立刻删除本仓库** |

- 📌 建议直接引用**上游原始地址**；本仓库只是替你省掉「转换」这一步
- 🔧 `skill/` 下的脚本与方法论**不含任何上游数据**，可自由取用、修改、再分发

---

## 📖 更多

- 📘 [`skill/SKILL.md`](skill/SKILL.md) —— 完整方法论：语义判定、通配映射、差集逻辑、白名单瘦身、踩坑记录
- 🧪 [`skill/scripts/convert_ruleset.py`](skill/scripts/convert_ruleset.py) —— 6 个规则文件全部由它产出，可复现重跑

---

<div align="center">

🛑 数据来自 VME98/jinx-rules · 本仓库不主张任何许可

</div>
