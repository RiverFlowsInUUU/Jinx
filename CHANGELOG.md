# 🗓️ 更新日志

规则集本身的显著变动，按日期倒序。日期为 UTC+8。

---

## 2026-09-22

**变更**

- 🏷️ **仓库名大小写规范化：`jinx-ads-rules` → `Jinx`** —— 与姊妹仓 `Surge` / `Egern` 的命名风格统一，也与上游项目名（`VME98/jinx-rules` 的 **Jinx**）一致。仓内 19 处引用已更新（README 订阅地址 / skill / 转换脚本）。
  - ⚠️ **旧地址实测全部仍可用**：`raw.githubusercontent.com` 与 jsDelivr 的旧名均 **HTTP 200**、`github.com` 旧名 **HTTP 301** → 新名 ⇒ **已订阅的地址无需改动**。
  - 📌 **文件名与 provider 名保持原样**：`surge-ads.list` / `surge-white-guard.list`、mihomo 侧 provider 名 `jinx-ads` / `jinx-white-guard` 属标识符，未动；上游 `VME98/jinx-rules` 未动。

- 🔧 mihomo 侧文件名 `.list` → `.yaml`，内容改为顶层 `payload` 列表。`.list` 是 Surge / Quantumult 的惯例，mihomo 的 `format` 默认就是 `yaml` —— 沿用 `.list` 会让抄配置的人漏写 `format`（按 yaml 解析直接报错），或被迫写一条多余的 `format: text`。**mihomo 旧地址失效**，Surge 侧文件名不变。
- 🔢 黑名单 3891 → **3889** 条（见下「移除」）。
- 🏷️ 术语调整：「完整版」→「**黑名单**」，「白名单守卫」→「**白名单**」。差集版删除后「完整」已失去对照物 —— 它只是相对差集才显得"完整"，不如按语义直呼。**文件名与订阅地址一个字未改**（`mihomo-ads.yaml` / `surge-ads.list` / `*-white-guard.*` 照旧），已订阅的不受影响。

**移除**

- 🧹 删除差集版（`mihomo-ads-delta.yaml` · `surge-ads-delta.list`）。三条实测否掉了它：① 收益只有「列表少 53 行」（约 1.4% 体积），而规则重复**本身没有副作用** —— 同一域名被两套规则命中，结果都是 REJECT；② 代价是把那 53 条的覆盖面**外包给对方的 16 条「伞」规则**，对方一改这边就静默漏拦；③ 对误杀**零改善** —— 黑名单与差集版对上游白名单的命中数同为 42 条。现只保留黑名单，要叠加第三方列表就直接叠。
- 🧹 `custom-ads.list` 移除 2 条：`msg.qy.net` · `rdelivery.qq.com` —— 两者都躺在上游 `whitelist.txt` 里，上游明确放行。保留 `rmonitor.qq.com`（既不在上游黑名单、也不在其白名单，是干净追加）。

**修复**

- 🐛 补齐 `--extra` 的收录前提：白名单的对照面是**上游黑名单**（`--guard-against-*` 不含 `custom-*.list`），所以追加进来的域名**不会**因为「上游已放行」而被白名单豁免 —— 跟上游白名单对着干 = 静默误杀。这条前提已写进 `custom-ads.list` 表头与 `skill/SKILL.md`，并按它移除了上面 2 个冲突条目。

## 2026-09-21

**变更**

- 🛡️ 白名单 42 → 43 条：新增 `*.tange365.com` —— 相机 App「小鲸看看」的业务域（账户 / 设备 / 云存储），必须直连。

## 2026-09-19

**修复**

- 🐛 普通域名由 `DOMAIN`（精确匹配）改为 `DOMAIN-SUFFIX`。Jinx 的匹配语义是「该域 + 全部子域」，初版按精确转换 —— 列表里写 `bugly.qq.com`，拦不住 `ios.bugly.qq.com`。同一份日志 30 条被拦域名的覆盖率 93% → 100%。

**新增**

- ✨ 新增 3 条上游未收录的广告域：`msg.qy.net` · `rmonitor.qq.com` · `rdelivery.qq.com`，由 `custom-ads.list` 并入。

**移除**

- 🧹 删除早期 `*-domain.list` / `*-domainset.txt` 变体，收敛为两平台各 3 份文件。

## 2026-09-18

**新增**

- 🎉 首次发布：mihomo 与 Surge 各 3 份规则集 —— 黑名单 / 差集版 / 白名单。
