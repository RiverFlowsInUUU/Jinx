<div align="center">

# 🛑 Jinx 去广告规则

**iOS 拦得住的广告，mihomo 和 Surge 也拦得住**

上游 Jinx 黑/白名单的格式转换 · 规则一条不增不减

[![Source](https://img.shields.io/badge/Source-Jinx%203.1.9-8250df?style=flat-square)](https://github.com/VME98/jinx-rules)
[![mihomo](https://img.shields.io/badge/mihomo-OpenClash-1f6feb?style=flat-square)](https://github.com/RiverFlowsInUUU/Jinx)
[![Surge](https://img.shields.io/badge/Surge-RULE--SET-orange?style=flat-square)](https://github.com/RiverFlowsInUUU/Jinx)
[![Rules](https://img.shields.io/badge/Ads-3889-0969da?style=flat-square)](https://github.com/RiverFlowsInUUU/Jinx)
[![License](https://img.shields.io/badge/License-%E6%9C%AA%E5%A3%B0%E6%98%8E-critical?style=flat-square)](#-来源与许可)

</div>

## 📥 订阅

📦 四份文件，两个源，内容完全一致；末两行是第三方的秋风广告规则，可叠加。

| 客户端 | 文件 | 条数 | 用途 |
|:-------|:-----|-----:|:-----|
| mihomo / OpenClash | `mihomo-ads.yaml` | 3889 | 拦截 |
| mihomo / OpenClash | `mihomo-white-guard.yaml` | 43 | 放行 |
| Surge | `surge-ads.list` | 3889 | 拦截 |
| Surge | `surge-white-guard.list` | 43 | 放行 |
| mihomo / OpenClash | `AWAvenue-Ads-Rule-Clash-Classical.yaml` | 965 | 拦截 · 秋风 |
| Surge | `AWAvenue-Ads-Rule-Surge-RULE-SET.list` | 965 | 拦截 · 秋风 |

⭐ **Raw GitHub** · 首选

```
https://raw.githubusercontent.com/RiverFlowsInUUU/Jinx/main/mihomo-ads.yaml
https://raw.githubusercontent.com/RiverFlowsInUUU/Jinx/main/mihomo-white-guard.yaml
https://raw.githubusercontent.com/RiverFlowsInUUU/Jinx/main/surge-ads.list
https://raw.githubusercontent.com/RiverFlowsInUUU/Jinx/main/surge-white-guard.list
```

🔁 **jsDelivr** · 备用

```
https://cdn.jsdelivr.net/gh/RiverFlowsInUUU/Jinx@main/mihomo-ads.yaml
https://cdn.jsdelivr.net/gh/RiverFlowsInUUU/Jinx@main/mihomo-white-guard.yaml
https://cdn.jsdelivr.net/gh/RiverFlowsInUUU/Jinx@main/surge-ads.list
https://cdn.jsdelivr.net/gh/RiverFlowsInUUU/Jinx@main/surge-white-guard.list
```

🔀 换备用源：把 `raw.githubusercontent.com/RiverFlowsInUUU/Jinx/main/` 换成 `cdn.jsdelivr.net/gh/RiverFlowsInUUU/Jinx@main/`。

🤝 **AWAvenue 秋风广告规则** · 第三方 · 可叠加 · 仅给 Raw 源

⚠️ 判定标准与 Jinx 不同 —— 会拦掉 Jinx 白名单里的 8 个域。由对方托管，缓存不归我们管，故不列备用源。

```
https://raw.githubusercontent.com/TG-Twilight/AWAvenue-Ads-Rule/main/Filters/AWAvenue-Ads-Rule-Clash-Classical.yaml
https://raw.githubusercontent.com/TG-Twilight/AWAvenue-Ads-Rule/main/Filters/AWAvenue-Ads-Rule-Surge-RULE-SET.list
```

## 🔌 接入

🔷 **mihomo / OpenClash**

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

🔶 **Surge**

```
[Rule]
# 白名单（精确放行）
RULE-SET,https://raw.githubusercontent.com/RiverFlowsInUUU/Jinx/main/surge-white-guard.list,DIRECT
# 广告拦截
RULE-SET,https://raw.githubusercontent.com/RiverFlowsInUUU/Jinx/main/surge-ads.list,REJECT,pre-matching,extended-matching
# 其余规则接在后面
```

💡 `pre-matching` 把 REJECT 提前到 DNS / 连接建立阶段，`extended-matching` 按 TLS SNI / HTTP Host 额外匹配，处理 App 直连 IP 的情况 —— 两者都只对 REJECT 系策略生效。

📌 叠加秋风规则时，把它排在 Jinx **之后**。

## 📋 规则顺序

🔽 自上而下，先匹配先赢。

| 顺序 | 规则 | 去向 |
|:-:|:-----|:-----|
| 1 | 🛡️ 白名单 | `DIRECT` |
| 2 | 🚫 广告拦截 | `REJECT` |
| 3 | 🚦 常规分流（`GEOSITE,cn` / `GEOIP,cn`） | `DIRECT` |

⚠️ 国内广告域名多数同时属于「中国大陆域名」—— `GEOSITE,cn` 若排到 `REJECT` 之前会先命中放行，广告规则再没有机会执行。

## 🚧 OpenClash

📌 `绕过中国大陆 IP`（`china_ip_route`）默认常开。开着时目标属大陆的连接直接放行、**不进入内核**，规则不生效，日志里也没有记录。用本规则集要关掉它：

```bash
uci set openclash.config.china_ip_route='0'
uci commit openclash
/etc/init.d/openclash restart
```

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
