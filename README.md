<div align="center">

# 🛑 Jinx 去广告规则

**iOS 拦得住的广告，mihomo / Surge / Egern / sing-box 也拦得住**

上游 Jinx 黑/白名单的格式转换 · 规则一条不增不减

[![Source](https://img.shields.io/badge/Source-Jinx%203.1.9-8250df?style=flat-square)](https://github.com/VME98/jinx-rules)
[![License](https://img.shields.io/badge/License-%E6%9C%AA%E5%A3%B0%E6%98%8E-critical?style=flat-square)](#-来源与许可)

[![mihomo](https://img.shields.io/badge/mihomo-OpenClash-1f6feb?style=flat-square)](#-接入)
[![Surge](https://img.shields.io/badge/Surge-RULE--SET-orange?style=flat-square)](#-接入)
[![Egern](https://img.shields.io/badge/Egern-%E5%A4%8D%E7%94%A8%20Surge%20%E6%A0%BC%E5%BC%8F-8957e5?style=flat-square)](#-接入)
[![sing-box](https://img.shields.io/badge/sing--box-source%20JSON-blue?style=flat-square)](#-接入)
[![CI](https://github.com/RiverFlowsInUUU/Jinx/actions/workflows/ci.yml/badge.svg)](https://github.com/RiverFlowsInUUU/Jinx/actions/workflows/ci.yml)

[![Ads](https://img.shields.io/badge/%E6%8B%A6%E6%88%AA-3889%20%E6%9D%A1-0969da?style=flat-square)](#-订阅)
[![White](https://img.shields.io/badge/%E6%94%BE%E8%A1%8C-44%20%E6%9D%A1-2da44e?style=flat-square)](#-订阅)
[![AWAvenue](https://img.shields.io/badge/%E7%A7%8B%E9%A3%8E-965%20%E6%9D%A1-f9c513?style=flat-square)](#-订阅)

</div>

> 🤖 **AI agent 请从这里开始** → [`skill/SKILL.md`](skill/SKILL.md)：改完必跑的那一条命令，和六条不要越的线。

## 🧭 目录

- [📥 订阅](#-订阅)
  - [🧱 Jinx 规则集](#-jinx-规则集)
  - [🤝 AWAvenue 秋风广告规则](#-awavenue-秋风广告规则)
- [🧬 一条不差 · 四端同源](#-一条不差--四端同源)
- [🔌 接入](#-接入)
- [📋 规则顺序](#-规则顺序)
- [🚧 OpenClash](#-openclash)
- [📖 文档](#-文档)
- [📚 来源与许可](#-来源与许可)

## 📥 订阅

### 🧱 Jinx 规则集

🔗 文件名即订阅地址 —— 右键「复制链接地址」即可取用。

| <div align="center">客户端</div> | <div align="center">🚫 拦截规则集</div> | <div align="center">✅ 放行规则集</div> |
|:--|:--|:--|
| **mihomo** / OpenClash | [`mihomo-ads.yaml`](https://raw.githubusercontent.com/RiverFlowsInUUU/Jinx/main/mihomo-ads.yaml) `3889` | [`mihomo-direct.yaml`](https://raw.githubusercontent.com/RiverFlowsInUUU/Jinx/main/mihomo-direct.yaml) `44` |
| **Surge** / **Egern** | [`surge-ads.list`](https://raw.githubusercontent.com/RiverFlowsInUUU/Jinx/main/surge-ads.list) `3889` | [`surge-direct.list`](https://raw.githubusercontent.com/RiverFlowsInUUU/Jinx/main/surge-direct.list) `44` |
| **sing-box** | [`sing-box-ads.json`](https://raw.githubusercontent.com/RiverFlowsInUUU/Jinx/main/sing-box-ads.json) `3889` | [`sing-box-direct.json`](https://raw.githubusercontent.com/RiverFlowsInUUU/Jinx/main/sing-box-direct.json) `44` |

📌 表内链接指向 **Raw GitHub**（首选源）。要换成 jsDelivr 备用源，把
`raw.githubusercontent.com/RiverFlowsInUUU/Jinx/main/` 换成 `cdn.jsdelivr.net/gh/RiverFlowsInUUU/Jinx@main/` 即可。

### 🤝 AWAvenue 秋风广告规则

🍂 第三方规则，官方直链，可叠加；上游每日更新，条数以官方文件头为准。

| <div align="center">客户端</div> | <div align="center">🚫 拦截规则集</div> |
|:--|:--|
| **mihomo** / OpenClash | [`AWAvenue-Ads-Rule-Clash-Classical.yaml`](https://raw.githubusercontent.com/TG-Twilight/AWAvenue-Ads-Rule/main/Filters/AWAvenue-Ads-Rule-Clash-Classical.yaml) `965` |
| **Surge** | [`AWAvenue-Ads-Rule-Surge-RULE-SET.list`](https://raw.githubusercontent.com/TG-Twilight/AWAvenue-Ads-Rule/main/Filters/AWAvenue-Ads-Rule-Surge-RULE-SET.list) `965` |
| **sing-box** | [`AWAvenue-Ads-Rule-Singbox.json`](https://raw.githubusercontent.com/TG-Twilight/AWAvenue-Ads-Rule/main/Filters/AWAvenue-Ads-Rule-Singbox.json) `965` |

> [!WARNING]
> 判定标准与 Jinx 不同 —— 会拦掉 Jinx 白名单里的 8 个域。叠加时把秋风排在 Jinx **之后**。

💡 sing-box 版是官方自己的 rule-set source 格式，`format: "source"` 直接挂，无需本地编译；条数与字段构成见 [`DetailsReadme/DetailsReadme.md`](DetailsReadme/DetailsReadme.md) 第 3 章。

---

## 🧬 一条不差 · 四端同源

🔬 不是"抄了一份列表"，是**同一批规则换个写法的镜像** —— 各端逐条等价，由 CI 每次提交对拍。

| <div align="center">维度</div> | <div align="center">Jinx 规则集</div> | <div align="center">说明</div> |
|:--|:--|:--|
| 🚫 拦截 | **3889 条** | 3740 条域名后缀 + 149 条中缀通配 |
| ✅ 放行 | **44 条** | 41 条精确 + 3 条后缀（含 2 条手工补充） |
| 🧩 各端一致 | **逐条等价** | mihomo / Surge / Egern / sing-box 归一化后零差异 |
| 🎯 增删 | **一条不增不减** | 只做格式转换，不改上游判定 |
| 🔄 可复现 | **逐字节一致** | 产物 == 源头重跑结果，CI 对拍 |
| 📌 上游快照 | `3.1.9` · `2026-09-15` | 上游更新后需重跑生成 |

🚫 **只做减法不做加法**：本仓不替你判断"哪些广告该拦"，上游收录什么就转什么。唯一例外是 `custom-*.list` 里人工补充的域名，每一条都写明依据。

---

## 🔌 接入

🎯 贴进去就能用；白名单规则在前、拦截在后，其余规则接在后面。

<details open>
<summary>🔷 <b>mihomo / OpenClash</b> · rule-providers</summary>

```yaml
rule-providers:
  jinx-ads:
    type: http
    behavior: classical          # 不用 domain
    format: yaml                 # 文件是顶层 payload 列表
    url: "https://raw.githubusercontent.com/RiverFlowsInUUU/Jinx/main/mihomo-ads.yaml"
    path: ./rule_provider/jinx-ads.yaml
    interval: 86400

  jinx-direct:
    type: http
    behavior: classical
    format: yaml
    url: "https://raw.githubusercontent.com/RiverFlowsInUUU/Jinx/main/mihomo-direct.yaml"
    path: ./rule_provider/jinx-direct.yaml
    interval: 86400

rules:
  - RULE-SET,jinx-direct,DIRECT
  - RULE-SET,jinx-ads,REJECT
  # 其余规则接在后面
```

💡 `behavior: classical` 不能改成 `domain` —— 文件是逐条规则，不是域名集合。

💡 `format: yaml` 与 `.yaml` 后缀配套（mihomo 的缺省格式，显式写出防抄错）。

</details>

<details>
<summary>🔶 <b>Surge</b> · RULE-SET</summary>

```
[Rule]
# 白名单（精确放行）
RULE-SET,https://raw.githubusercontent.com/RiverFlowsInUUU/Jinx/main/surge-direct.list,DIRECT
# 广告拦截
RULE-SET,https://raw.githubusercontent.com/RiverFlowsInUUU/Jinx/main/surge-ads.list,REJECT,pre-matching,extended-matching
# 其余规则接在后面
```

💡 `pre-matching` 把 REJECT 提前到 DNS / 连接建立阶段，`extended-matching` 按 TLS SNI / HTTP Host 额外匹配，处理 App 直连 IP 的情况 —— 两者都只对 REJECT 系策略生效，白名单行不加。

</details>

<details>
<summary>🟣 <b>Egern</b> · 直接复用 Surge 那份 <code>.list</code></summary>

✨ **不用另找文件** —— Egern 的规则集格式与 Surge 同源，`surge-direct.list` 与 `surge-ads.list` 原样可用。

```yaml
# ① 连接阶段：走规则匹配（白名单在前、拦截在后）
rules:
- rule_set:
    name: Jinx-CN
    match: https://raw.githubusercontent.com/RiverFlowsInUUU/Jinx/main/surge-direct.list
    policy: DIRECT
    update_interval: 604800
- rule_set:
    name: Jinx-Ads
    match: https://raw.githubusercontent.com/RiverFlowsInUUU/Jinx/main/surge-ads.list
    policy: AD
    update_interval: 604800
    # 其余规则接在后面
```

```yaml
# ② DNS 阶段：防泄露的一环（可选，但推荐 —— 广告域在解析阶段就拒答）
forward:
- proxy_rule_set:
    match: https://raw.githubusercontent.com/RiverFlowsInUUU/Jinx/main/surge-direct.list
    value: Domestic-DNS
- proxy_rule_set:
    match: https://raw.githubusercontent.com/RiverFlowsInUUU/Jinx/main/surge-ads.list
    value: reject
- domain_wildcard: '*'          # 兜底必须指向「代理没起来时也能用」的加密组
  value: Domestic-DNS
```

💡 `update_interval: 604800` 是一周（秒）—— Egern 官方**未文档化**该键缺省值，**不写就是行为不可知**，建议显式钉死。

💡 `policy` / `value` 里的组名（`AD` / `Direct` / `Domestic-DNS`）按你自己的配置改；上面用的是常见写法。

💡 两处引用**同一份文件**即可：`rules` 段管连接，`forward` 段管 DNS。这份文件是**纯域名、零 IP 条目**，不会因 IP 类规则触发额外解析。

</details>

<details>
<summary>🔷 <b>sing-box</b> · rule_set（1.14.2 实测）</summary>

```json
{
  "route": {
    "rule_set": [
      {
        "type": "remote",
        "tag": "jinx-direct",
        "format": "source",
        "url": "https://raw.githubusercontent.com/RiverFlowsInUUU/Jinx/main/sing-box-direct.json",
        "update_interval": "1d"
      },
      {
        "type": "remote",
        "tag": "jinx-ads",
        "format": "source",
        "url": "https://raw.githubusercontent.com/RiverFlowsInUUU/Jinx/main/sing-box-ads.json",
        "update_interval": "1d"
      }
    ],
    "rules": [
      { "rule_set": ["jinx-direct"], "outbound": "direct" },
      { "rule_set": ["jinx-ads"], "action": "reject" }
    ]
  }
}
```

💡 `format: "source"` 是 JSON 源格式，不用二进制 `.srs`，订阅即用。

💡 `outbound` 的 `direct` 指配置里直连出站的 tag，按自己的配置改。

💡 `update_interval` 缺省就是 `1d`；1.14 起 `download_detour` 已废弃（1.16 移除），不要再用。

</details>

---

## 📋 规则顺序

🔽 自上而下，先匹配先赢 —— 顺序错了，规则等于没加。

| <div align="center">顺序</div> | <div align="center">规则</div> | <div align="center">去向</div> |
|:-:|:-----|:-----|
| 1 | ✅ 白名单 | `DIRECT` |
| 2 | 🚫 广告拦截 | `REJECT` |
| 3 | 🚦 常规分流（`GEOSITE,cn` / `GEOIP,cn`） | `DIRECT` |

> [!WARNING]
> 国内广告域名多数同时属于「中国大陆域名」—— `GEOSITE,cn` 若排到 `REJECT` 之前会先命中放行，广告规则再没有机会执行。

---

## 🚧 OpenClash

🔧 一个开关决定规则生不生效 —— 装完先看这一节。

> [!IMPORTANT]
> `绕过中国大陆 IP`（`china_ip_route`）默认常开：目标属大陆的连接直接放行、**不进入内核**，规则不生效、日志无记录。用本规则集必须关掉它。

<details>
<summary>🔧 关闭命令（SSH）</summary>

```bash
uci set openclash.config.china_ip_route='0'
uci commit openclash
/etc/init.d/openclash restart
```

</details>

🔁 回滚：把 `'0'` 改回 `'1'` 再重启即可。

---

## 📖 文档

📚 按需查阅 —— 常用操作在首页，原理与推导在下沉文档。

| <div align="center">文档</div> | <div align="center">内容</div> |
|:-----|:-----|
| 📘 [`DetailsReadme/DetailsReadme.md`](DetailsReadme/DetailsReadme.md) | 白名单来源 · 两个源的缓存与生效判据 · 秋风对比 · 转换原理 · OpenClash 细节 |
| 🧪 [`skill/SKILL.md`](skill/SKILL.md) | 匹配语义判定 · 通配映射 · 白名单瘦身 · 生成命令 · 验收闸门 |
| 📅 [`CHANGELOG.md`](CHANGELOG.md) | 规则变动记录 |

🧷 六份文件同一次生成、内容等价，由 CI 每次提交自动校验（三格式逐条比对 + 条数声明 + 产物可复现），读数字不符会直接标红。

---

## 📚 来源与许可

| <div align="center">项</div> | <div align="center">说明</div> |
|:--|:--|
| 📄 上游 | [`VME98/jinx-rules`](https://github.com/VME98/jinx-rules) · 数据 `3.1.9` · `2026-09-15` |
| 📜 许可 | 上游未声明（`license: null`），本仓亦不主张 |
| 🧬 规则数据 | 版权归上游及其原始来源 |
| 🧪 `skill/` | 转换脚本与方法论，不含上游数据，可自由取用 |

📮 上游权利人如有异议，开 issue 即下架。

---

<div align="center">

📊 数据来自 VME98/jinx-rules

</div>
