# 🗓️ 更新日志

规则集本身的显著变动，按日期倒序。日期为 UTC+8。

---

## 2026-09-22

**变更**

- 🔧 mihomo 侧文件名 `.list` → `.yaml`，内容改为顶层 `payload` 列表。`.list` 是 Surge / Quantumult 的惯例，mihomo 的 `format` 默认就是 `yaml` —— 沿用 `.list` 会让抄配置的人漏写 `format`（按 yaml 解析直接报错），或被迫写一条多余的 `format: text`。**mihomo 旧地址失效**，Surge 侧文件名不变。

## 2026-09-21

**变更**

- 🛡️ 白名单守卫 42 → 43 条：新增 `*.tange365.com` —— 相机 App「小鲸看看」的业务域（账户 / 设备 / 云存储），必须直连。

## 2026-09-19

**修复**

- 🐛 普通域名由 `DOMAIN`（精确匹配）改为 `DOMAIN-SUFFIX`。Jinx 的匹配语义是「该域 + 全部子域」，初版按精确转换 —— 列表里写 `bugly.qq.com`，拦不住 `ios.bugly.qq.com`。同一份日志 30 条被拦域名的覆盖率 93% → 100%。

**新增**

- ✨ 新增 3 条上游未收录的广告域：`msg.qy.net` · `rmonitor.qq.com` · `rdelivery.qq.com`，由 `custom-ads.list` 并入。

**移除**

- 🧹 删除早期 `*-domain.list` / `*-domainset.txt` 变体，收敛为两平台各 3 份文件。

## 2026-09-18

**新增**

- 🎉 首次发布：mihomo 与 Surge 各 3 份规则集 —— 完整版 / 差集版 / 白名单守卫。
