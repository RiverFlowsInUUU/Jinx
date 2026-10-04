<div align="center">

# 🛑 Jinx 去广告规则

**iOS 拦得住的广告，mihomo / Surge / sing-box 也拦得住**

上游 Jinx 黑/白名单的格式转换 · 规则一条不增不减

[![Source](https://img.shields.io/badge/Source-Jinx%203.1.9-8250df?style=flat-square)](https://github.com/VME98/jinx-rules)
[![License](https://img.shields.io/badge/License-%E6%9C%AA%E5%A3%B0%E6%98%8E-critical?style=flat-square)](#-来源与许可)

[![mihomo](https://img.shields.io/badge/mihomo-OpenClash-1f6feb?style=flat-square)](#-接入)
[![Surge](https://img.shields.io/badge/Surge-RULE--SET-orange?style=flat-square)](#-接入)
[![sing-box](https://img.shields.io/badge/sing--box-source%20JSON-blue?style=flat-square)](#-接入)

[![Ads](https://img.shields.io/badge/%E6%8B%A6%E6%88%AA-3889%20%E6%9D%A1-0969da?style=flat-square)](#-订阅)
[![White](https://img.shields.io/badge/%E6%94%BE%E8%A1%8C-44%20%E6%9D%A1-2da44e?style=flat-square)](#-订阅)
[![AWAvenue](https://img.shields.io/badge/%E7%A7%8B%E9%A3%8E-965%20%E6%9D%A1-f9c513?style=flat-square)](#-订阅)

</div>

## 🧭 目录

- [📥 订阅](#-订阅)
  - [🧱 Jinx 规则集](#-jinx-规则集)
  - [🤝 AWAvenue 秋风广告规则](#-awavenue-秋风广告规则)
- [🔌 接入](#-接入)
- [📋 规则顺序](#-规则顺序)
- [🚧 OpenClash](#-openclash)
- [📖 文档](#-文档)
- [📚 来源与许可](#-来源与许可)

## 📥 订阅

### 🧱 Jinx 规则集

📦 六份文件 × 两个源，内容完全一致，订阅任选其一。

| 客户端 | 文件 | 条数 | 用途 |
|:-------|:-----|-----:|:-----|
| mihomo / OpenClash | `mihomo-ads.yaml` | 3889 | 拦截 |
| mihomo / OpenClash | `mihomo-white-guard.yaml` | 44 | 放行 |
| Surge | `surge-ads.list` | 3889 | 拦截 |
| Surge | `surge-white-guard.list` | 44 | 放行 |
| sing-box | `sing-box-ads.json` | 3889 | 拦截 |
| sing-box | `sing-box-white-guard.json` | 44 | 放行 |

⭐ **Raw GitHub** · 首选

```
https://raw.githubusercontent.com/RiverFlowsInUUU/Jinx/main/mihomo-ads.yaml
https://raw.githubusercontent.com/RiverFlowsInUUU/Jinx/main/mihomo-white-guard.yaml
https://raw.githubusercontent.com/RiverFlowsInUUU/Jinx/main/surge-ads.list
https://raw.githubusercontent.com/RiverFlowsInUUU/Jinx/main/surge-white-guard.list
https://raw.githubusercontent.com/RiverFlowsInUUU/Jinx/main/sing-box-ads.json
https://raw.githubusercontent.com/RiverFlowsInUUU/Jinx/main/sing-box-white-guard.json
```

🔁 **jsDelivr** · 备用

```
https://cdn.jsdelivr.net/gh/RiverFlowsInUUU/Jinx@main/mihomo-ads.yaml
https://cdn.jsdelivr.net/gh/RiverFlowsInUUU/Jinx@main/mihomo-white-guard.yaml
https://cdn.jsdelivr.net/gh/RiverFlowsInUUU/Jinx@main/surge-ads.list
https://cdn.jsdelivr.net/gh/RiverFlowsInUUU/Jinx@main/surge-white-guard.list
https://cdn.jsdelivr.net/gh/RiverFlowsInUUU/Jinx@main/sing-box-ads.json
https://cdn.jsdelivr.net/gh/RiverFlowsInUUU/Jinx@main/sing-box-white-guard.json
```

🔀 换备用源：把 `raw.githubusercontent.com/RiverFlowsInUUU/Jinx/main/` 换成 `cdn.jsdelivr.net/gh/RiverFlowsInUUU/Jinx@main/`。

### 🤝 AWAvenue 秋风广告规则

🍂 第三方规则，官方直链，可叠加；上游每日更新，条数以官方文件头为准。

| 客户端 | 文件 | 条数 | 用途 |
|:-------|:-----|-----:|:-----|
| mihomo / OpenClash | `AWAvenue-Ads-Rule-Clash-Classical.yaml` | 965 | 拦截 |
| Surge | `AWAvenue-Ads-Rule-Surge-RULE-SET.list` | 965 | 拦截 |
| sing-box | `AWAvenue-Ads-Rule-Singbox.json` | 965 | 拦截 |

```
https://raw.githubusercontent.com/TG-Twilight/AWAvenue-Ads-Rule/main/Filters/AWAvenue-Ads-Rule-Clash-Classical.yaml
https://raw.githubusercontent.com/TG-Twilight/AWAvenue-Ads-Rule/main/Filters/AWAvenue-Ads-Rule-Surge-RULE-SET.list
https://raw.githubusercontent.com/TG-Twilight/AWAvenue-Ads-Rule/main/Filters/AWAvenue-Ads-Rule-Singbox.json
```

> [!WARNING]
> 判定标准与 Jinx 不同 —— 会拦掉 Jinx 白名单里的 8 个域。叠加时把秋风排在 Jinx **之后**。

💡 sing-box 版是官方自己的 rule-set source 格式，`format: "source"` 直接挂，无需本地编译；条数与字段构成见 [`DetailsReadme/DetailsReadme.md`](DetailsReadme/DetailsReadme.md) 第 3 章。

## 🔌 接入

🔽 点开对应客户端展开配置；白名单规则在前、拦截在后，其余规则接在后面。

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

  jinx-white-guard:
    type: http
    behavior: classical
    format: yaml
    url: "https://raw.githubusercontent.com/RiverFlowsInUUU/Jinx/main/mihomo-white-guard.yaml"
    path: ./rule_provider/jinx-white-guard.yaml
    interval: 86400

rules:
  - RULE-SET,jinx-white-guard,DIRECT
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
RULE-SET,https://raw.githubusercontent.com/RiverFlowsInUUU/Jinx/main/surge-white-guard.list,DIRECT
# 广告拦截
RULE-SET,https://raw.githubusercontent.com/RiverFlowsInUUU/Jinx/main/surge-ads.list,REJECT,pre-matching,extended-matching
# 其余规则接在后面
```

💡 `pre-matching` 把 REJECT 提前到 DNS / 连接建立阶段，`extended-matching` 按 TLS SNI / HTTP Host 额外匹配，处理 App 直连 IP 的情况 —— 两者都只对 REJECT 系策略生效，白名单行不加。

</details>

<details>
<summary>🔷 <b>sing-box</b> · rule_set（1.14.2 实测）</summary>

```json
{
  "route": {
    "rule_set": [
      {
        "type": "remote",
        "tag": "jinx-white-guard",
        "format": "source",
        "url": "https://raw.githubusercontent.com/RiverFlowsInUUU/Jinx/main/sing-box-white-guard.json",
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
      { "rule_set": ["jinx-white-guard"], "outbound": "direct" },
      { "rule_set": ["jinx-ads"], "action": "reject" }
    ]
  }
}
```

💡 `format: "source"` 是 JSON 源格式，不用二进制 `.srs`，订阅即用。

💡 `outbound` 的 `direct` 指配置里直连出站的 tag，按自己的配置改。

💡 `update_interval` 缺省就是 `1d`；1.14 起 `download_detour` 已废弃（1.16 移除），不要再用。

</details>

## 📋 规则顺序

🔽 自上而下，先匹配先赢。

| 顺序 | 规则 | 去向 |
|:-:|:-----|:-----|
| 1 | 🛡️ 白名单 | `DIRECT` |
| 2 | 🚫 广告拦截 | `REJECT` |
| 3 | 🚦 常规分流（`GEOSITE,cn` / `GEOIP,cn`） | `DIRECT` |

> [!WARNING]
> 国内广告域名多数同时属于「中国大陆域名」—— `GEOSITE,cn` 若排到 `REJECT` 之前会先命中放行，广告规则再没有机会执行。

## 🚧 OpenClash

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

## 📖 文档

| 文档 | 内容 |
|:-----|:-----|
| 📘 [`DetailsReadme/DetailsReadme.md`](DetailsReadme/DetailsReadme.md) | 白名单来源 · 两个源的缓存与生效判据 · 秋风对比 · 转换原理 · OpenClash 细节 |
| 🧪 [`skill/SKILL.md`](skill/SKILL.md) | 匹配语义判定 · 通配映射 · 白名单瘦身 · 生成命令 |
| 🗓️ [`CHANGELOG.md`](CHANGELOG.md) | 规则变动记录 |

## 📚 来源与许可

📄 上游 [`VME98/jinx-rules`](https://github.com/VME98/jinx-rules)（数据 `3.1.9` · `2026-09-15`，未声明许可）。规则数据版权归上游及其原始来源，本仓不主张任何权利；`skill/` 下的脚本与方法论不含上游数据，可自由取用。上游权利人如有异议，开 issue 即下架。

---

<div align="center">

📊 数据来自 VME98/jinx-rules

</div>
