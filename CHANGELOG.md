# 🗓️ 更新日志

规则集本身的显著变动，按日期倒序。日期为 UTC+8。

---

## 2026-10-10（六）· 规则：白名单新增 `*.za.group`

> 📌 本日第一条。上游数据仍固定在 `3.1.9` 快照，未随本次改动漂移。

**变更**

- 🛡️ **白名单 44 → 45 条：新增 `*.za.group`** —— 众安银行 App（ZA Bank）业务域，2026-10-10 实测 + 用户指定放行，语义为 `za.group` 及其全部子域（如 `bankappgw.za.group` / `bank.za.group`），三平台落点分别为 `DOMAIN-SUFFIX,za.group`（mihomo / Surge）与 `domain_suffix: ["za.group"]`（sing-box）。经 `custom-direct.list` 的 `--extra-white` 通道并入，追加在 guard 过滤之后、不参与碰撞裁剪。
  - 🔍 **现象**：大陆使用懒人版时 App 的 `bankappgw.za.group:443` 落进兜底规则走境外代理，登录 / 刷新 / 查余额一直转圈；图片与静态资源正常（`cdn.zaticdn.com` 上游已在直连集）。
  - 🧩 **根因**：上游直连集（Loyalsoldier `direct.txt` 与 Jinx 白名单）均未收录 `za.group`；同族的 `zainvest.group` / `zafinsvc.com` / `zajourney.com` / `zaticdn.com` 上游都已放行，**只有 `za.group` 一族漏网**。实测大陆可直连、未被墙，故在本仓手工补直连，等上游收录后再删本条。
  - 📐 三份产物同一次重跑生成，条数 45 / 45 / 45 一致；`sing-box` 侧字段构成 `domain=41 domain_suffix=4`（原 3 项 + 本次 1 项）。
  - ✅ **验收（对 diff）**：与改动前对拍，**只出现三处允许的变化** —— 表头 `# entries: 44 → 45`、`# extra-white: custom-direct.list(2) → (3)`、末尾按顺序多出 1 条 `DOMAIN-SUFFIX,za.group`；其余正文**逐行不变**（既有 44 条逐字节相同；sing-box JSON 仅 `domain_suffix` 数组末尾追加 1 项）。README 与 `DetailsReadme` 的条数声明同步 44 → 45，`skill/SKILL.md` 预期读数与 `selftest_negative.py` 的条数锚点一并更新。
  - 📌 **上游快照未动**：本次重跑固定在上游 `3.1.9`（commit `3fd15f94`）—— 改前已先验证「用该版本重跑，六份产物与仓库既有文件逐字节一致」，故本次 diff 不含任何上游漂移（上游现已是 `3.2.1`）。

---

## 2026-10-04（四）· 改名：`*-white-guard.*` → `*-direct.*`

> 📌 本日第四条。**规则内容零改动** —— 三份产物逐字节比对，与新名前完全一致。

**变更**

- 🏷️ **白名单产物改名：`mihomo-white-guard.yaml` → `mihomo-direct.yaml`、`surge-white-guard.list` → `surge-direct.list`、`sing-box-white-guard.json` → `sing-box-direct.json`。** 与源头 `custom-direct.list` 及「白名单 = 直连」的语义对齐 —— 历史名 `white-guard` 是更早一次术语调整（「白名单守卫」→「白名单」）未收尾的遗留。
  - ⚠️ **旧订阅地址失效**：三个旧名文件已删除，旧地址将 404。**已订阅旧地址的需改用新地址。** —— 这是本次改动的已知代价，经确认后执行。
  - 🔧 示例里的 **provider / tag 名**一并由 `jinx-white-guard` 改为 `jinx-direct`（文件名与标识符对齐）。
  - ✅ **内容零改动**：新旧产物**逐字节相同**（1599 / 1326 / 1459 字节，三份全等）—— 纯改名。
  - 📐 产物名由 `convert_ruleset.py --tag <名>` 决定，故**改的是生成参数**（`--tag white-guard` → `--tag direct`）而非手改文件名，`verify_jinx_src.py` 的 `REGEN` / `PRODUCTS` 表随之同步 —— 保证「产物 == 源头重跑结果」这条断言仍然成立。
  - 📝 全仓共 52 处引用随之更新（生成参数 / README / DetailsReadme / SKILL / 断言 / 负样本 / `custom-direct.list` 表头）；**CHANGELOG 的 6 处旧名保留不动** —— 那里记的是"当时叫什么"，改了等于篡改历史。

**纪律入册**

- `skill/SKILL.md`「对外交付」新增一条：**改一个产物的文件名 = 一次改全套，且属破坏性改动**（订阅地址变更）。含代价先想清楚（旧地址 404；无法确认引用方已迁移时宁可保留旧文件标注废弃）、先改 `--tag` 而非 `git mv`、改完必做逐字节比对、五层必查清单、CHANGELOG 一律不改。

---

## 2026-10-04（三）· 修复：行尾跨平台不一致（CI 首跑即抓出）

> 📌 本日第三条。**规则内容零改动** —— 六份产物只有行尾变化（CRLF → LF），逐字节归一化比对已证「仅行尾不同、内容一致」。

**修复**

- 🐛 **`convert_ruleset.py` 写出行尾随平台而变，产物跨平台不可复现** —— 脚本原用 `write_text(text)`，而 Python 的通用换行转换会把 `\n` 按平台写成 `os.linesep`：**Windows 出 CRLF、Linux 出 LF**。后果是仓库内**行尾分裂**（mihomo / Surge 四份产物为 CRLF、sing-box 两份为 LF），且 CI 在 Linux 上重跑生成必得 LF、与仓库内容不符。
  - 修法两条腿：① 写出改为 `write_text(text, encoding='utf-8', newline='')` 显式钉死 LF；② 新增 `.gitattributes`（`* text=auto eol=lf`）管住检出与提交。**缺一不可** —— 只改脚本则仓库内容仍是 CRLF、CI 仍判负；只归一化文件则下次在 Windows 重跑又写回 CRLF。
  - ✅ 六份产物按新脚本重跑，验证方式为「与改动前逐字节归一化行尾后比对」，结果全部为「仅行尾不同、内容一致」。
  - 📌 规则集按行解析、客户端都会 trim 行尾，CRLF 与 LF 对功能等价；本次只为「跨平台产物逐字节可复现」这一工程目标。

**留痕：这次缺陷是 CI 第一次运行当场抓出来的**

- 🔍 推上 CI 后首次运行**判负 6 项** —— 本地全绿、CI 全红，根因正是平台差异（本机 Windows 的 `write_text` 出 CRLF，与仓库内容"碰巧"一致；Linux 出 LF 才暴露真相）。这恰好印证了本仓这条断言的价值：**「产物 == 源头重跑结果」必须跨平台验证**，只在本机跑等于没跑。
- ⚠️ **同时更正一条此前的错误判断**：上一节曾写「仓库内实际存的是 LF，只是 `core.autocrlf=true` 把它检出成 CRLF」。用 `git cat-file -p HEAD:<file>` 直读 blob 核实后确认：**仓库内就是 CRLF**，`core.autocrlf` 不是原因。教训是 —— 判断「仓库里到底存了什么」必须直读 git 对象，**不能看工作区**（工作区会被 autocrlf 改写）。
- 📐 本次同步更新 `skill/SKILL.md` 踩坑记录与 `DetailsReadme` 第 9 节，把平台行尾陷阱的判据与两条腿修法写入，供日后复用。

---

> 📌 本日第二条。规则数据一个字节未改 —— 只加校验。白名单的改动见下方（一）节。

**新增**

- ✅ **`skill/tests/verify_jinx_src.py` —— 一致性断言（9 段 · 50 项）** —— 本仓的立身之本是「六份文件内容等价、规则一条不增不减」，此前**只靠人工对拍**，一次误改即静默破坏且无人察觉。现固化为断言：产物存在性 · 三格式条数一致 · **跨格式逐条语义等价**（归一化比对，非仅比条数）· 表头 `# entries` 自述 · 文档条数声明（README / DetailsReadme）· **产物 == 源头重跑结果**（逐字节，防手改产物与「改了源头忘了重跑」）· `custom-*.list` 落盘 · 文案规范（emoji 行首 + 密度）· 行尾与 BOM。
  - 🔢 退出码沿用全仓四态：`0` 过 / `1` 判负 / `2` 环境不达标 / `3` SKIP。**SKIP 走独立码 3，不借 0 蒙混**（姊妹仓曾因 SKIP 与「环境不达标」同码，把环境故障吞成 SKIP → exit 0 假绿）。
  - 📌 第 6 段需上游源文件，CI 先下载再跑；本地裸跑显示 SKIP 属正常。
  - 📌 该脚本名此前已被 `skill/SKILL.md` 第 280 行引用为「emoji 断言的第 8 段」，但**文件从未存在**（`git log --diff-filter=A` 零命中）—— 本次一并兑现该引用。

- 🧪 **`skill/tests/selftest_negative.py` —— 负样本自测（防闸门空转）** —— 在临时副本仓里制造 6 种典型错误（手改产物 / 只改表头 / 跨格式差异 / 文档漂移 / 源头改了没重跑 / emoji 违规），要求断言脚本逐一判负；**有漏报即判负**。依据是本 skill 记录过的「两半都恒空 = 永远绿的空操作」教训：一个只会全绿的闸门与没有闸门等价。

- 🔁 **`.github/workflows/ci.yml` —— 首次引入 CI** —— push / PR 触发：取上游源文件 → 跑 9 段断言 → 跑负样本自测。取源文件一步**失败即整步失败**（`curl -f`），避免源文件静默缺失导致第 6 段长期 SKIP、CI 退化成空操作。

- 🏷️ README 加 CI 徽章；文档索引补「验收闸门」；DetailsReadme 新增第 9 节「一致性保证与验收」（九段清单、退出码协议、已知行尾不统一）。

**修复**

- 🐛 **`DetailsReadme` 白名单条数漏改**：`mihomo-white-guard.yaml` 一行仍写 `43`（本日第一条改动时只同步了 Surge / sing-box 两行，漏了这一行）。**由新写的断言当场抓出** —— 这正是它存在的意义。
- 📐 **`skill/SKILL.md` 预期读数过期**：「完整生成」节的预期读数写着 `white-guard 43` / `domain_suffix=2`，已随本次白名单改动更新为 `44` / `3`，并注明该行随源头漂、写完必跑闸门核对。

**留痕（编写断言时踩的坑，两条都会给出错误结论）**

- 🐛 **第 6 段比对曾被 `--src` 写法差异误报**：`--src` 会**原样进产物表头**，而 ads 线线上是 `# source: jinx-rules`（无 `./`）、white-guard 线是 `# source: ./jinx-rules`（有 `./`）—— 两条命令写法本就不同，不是笔误。断言脚本因此按产品线分别固化参数，并在 diff 详情里显式提示「仅表头注释行差异」。
- 🐛 **emoji 判定曾漏报句中 emoji**：初版把 `U+2B00-2BFF` 整段当箭头排除（为让 `→` U+2192 不算 emoji），但 `⭐`(U+2B50) 正住在那段里 → `上面用的是 ⭐ 首选 Raw` 这类违规**静默逃过检查**。改为逐码位排除箭头。该漏报由负样本自测当场抓到，并留下一个用 `⭐` 造的负样本长期守它。
- 🐛 **emoji 判定曾给合规内容假红**：`⚖️` = U+2696 + U+FE0F，若把 FE0F 当独立 emoji 匹配，第二轮命中时前缀非结构字符 → 本仓 7 处 `⚖️ / ⏱️ / ⚠️` 行首引导符全被误报。改为 FE0F 随基字符整体消费。

---

## 2026-10-04（二）· 工程：一致性闸门与 CI

> 📌 本日第二条。**规则数据一个字节未改** —— 只加校验。
**新增**

## 2026-10-04（一）· 规则：白名单新增 `*.wechatos.net`

> 📌 本日三条记录中的第一条。本日共三次改动，为同一天内的先后顺序，非版本号。

**变更**

- 🛡️ **白名单 43 → 44 条：新增 `*.wechatos.net`** —— 用户指定放行，语义为 `wechatos.net` 及其全部子域（如 `api.wechatos.net` / `cdn.wechatos.net`），三平台落点分别为 `DOMAIN-SUFFIX,wechatos.net`（mihomo / Surge）与 `domain_suffix: ["wechatos.net"]`（sing-box）。经 `custom-direct.list` 的 `--extra-white` 通道并入，追加在 guard 过滤之后、不参与碰撞裁剪。
  - 📌 **语义口径留痕**：「前缀是 wechatos.net 的所有域名」有歧义，两种解法范围不同 —— 本次取**后缀语义**（`DOMAIN-SUFFIX`，放行该域 + 全部子域）；另一种「任何以 `wechatos.net` 开头的域名」（如 `wechatos.net.abc.com`）需 `DOMAIN-KEYWORD,wechatos.net`，范围更宽，**本次不采用**。日后若要改判，按此口径重议。
  - 📐 三份产物同一次重跑生成，条数 44 / 44 / 44 一致；`sing-box` 侧字段构成 `domain=41 domain_suffix=3`（原 2 项 + 本次 1 项）。
  - ✅ **验收（对 diff）**：与改动前对拍，**只出现三处允许的变化** —— 表头 `# entries: 43 → 44`、`# extra-white: custom-direct.list(1) → (2)`、末尾按顺序多出 1 条 `DOMAIN-SUFFIX,wechatos.net`；其余正文**逐行不变**（sing-box JSON 无表头，仅 `domain_suffix` 数组末尾追加 1 项，既有 41 + 2 项逐项一致）。README 与 `DetailsReadme` 的条数声明同步 43 → 44。

---

## 2026-09-28

**变更**

- 🔵 **新增 sing-box 支持：`sing-box-ads.json`（3889 条）· `sing-box-white-guard.json`（43 条）** —— rule-set 的 **source 格式**（JSON），不是二进制 `.srs`：远程规则集 `format: "source"` 直接消费，订阅即用。格式依据官方文档（内核 **1.14.2** 实测）：顶层 `{"version": 5, "rules": [...]}`，5 是 1.14.0 引入的当前版本；`.json` 扩展名即 source 格式的约定后缀（`format` 在该扩展名下可省略，示例仍显式写出）。条数与 mihomo / Surge 完全一致，同一次重跑生成。
  - 📐 **字段映射**：黑名单条目（域 + 全部子域）→ `domain_suffix`（3740），149 条中缀通配 → `domain_regex`（Go RE2，与 mihomo `DOMAIN-REGEX` 转换式相同）；白名单精确条目 → `domain`（41），强制放行条目 → `domain_suffix`（2）。
  - 🔬 **`domain_suffix` 语义实证**（`sagernet/sing` 的 `common/domain/matcher.go`）：不带点写法命中自身 + 全部子域、域段级边界（`aexample.com` 不误命中）—— 与 mihomo `DOMAIN-SUFFIX` 等价；前导点 `.example.com` 才是「仅子域」，本仓不用。
  - ✅ **1.14.2 内核全链路验证**：两份 JSON `rule-set compile` 通过；本地挂载与远程（`type: remote` + `format: "source"`）两种接入 `sing-box check` 通过；compile → decompile 回读逐条一致（唯一差 17 条重复折叠，见下）。
  - 📌 17 条「重复」来自上游同时存在 `*.x.com` 与 `x.com`（转换后同值），mihomo / Surge 侧同样保留这 17 行 —— 重复匹配无副作用，三平台口径一致；compile 成 `.srs` 时 trie 会折叠它们，属语义无损。
  - 📌 接入示例里 `outbound: "direct"` 按用户自己的直连出站 tag 改；`update_interval` 缺省即 `1d`；1.14 起 `download_detour` 已废弃（1.16 移除），示例不再使用。

- 🧪 `convert_ruleset.py` 同步扩展：黑/白名单两条命令现在各产出 **3 个文件**（mihomo / Surge / sing-box），sing-box 侧元数据只打印到 stdout（source JSON 不支持注释、strict 解析不允许多余字段）。重跑验收：既有 4 个产物 **逐字节不变**（`cmp` 验证），仅新增 2 个 JSON。

- 🤝 **秋风（AWAvenue）订阅清单补齐 sing-box 行** —— 官方本就有现成的 `AWAvenue-Ads-Rule-Singbox.json`（rule-set source 格式，`version: 3`，1.14.2 内核 compile 验证兼容），README 订阅表与地址块各加一行官方直链，三平台对齐。965 条与 `RULE-SET` 版同源（`domain` 949 + `domain_suffix` 12 + `domain_keyword` 4，关键词规则有原生字段、无转换损失）。**本仓不镜像这份文件**：官方每日更新、快照必滞后，且官方已是目标格式、镜像无加工价值 —— 与 Jinx 侧「格式转换镜像」的定位不同（口径入 DetailsReadme 第 3 章）。

- 🎨 **README 整体重排（183 → 253 行）：目录导航 + 自家/第三方分表 + 接入折叠 + 原生 alert** —— 用户原话「逻辑和可视化美观化都是一坨」。四处改动：
  - 🧭 顶部加**目录**（8 条内链，锚点按 github-slugger 规则对拍验证全命中，标题 emoji 无 FE0F）；slogan 补上 sing-box（原「mihomo 和 Surge 也拦得住」漏了新平台）；徽章重排三行（项目 / 平台 / 数据），数据徽章拆「拦截 3889 · 放行 43 · 秋风 965」各配中文色标。
  - 🧱 **订阅节拆两个 `###` 子节**：自家 6 份（两源地址块）与秋风 3 份（官方直链单源）分表 —— 原先 9 行混排一张表，第三方行「官方直链、无备用源」与自家「两源可选」的事实混在一起说不清。
  - 🔌 **接入节三个客户端各收进 `<details>` 折叠块**（mihomo 默认展开）：原先 ~60 行配置怼在正文里，sing-box 一段还连着 4 个 💡📌 堆成整段；折叠后每块内说明**一行一条**。配置一字未改。
  - ⚠️ **两处硬警告升级为 GitHub 原生 alert**（`> [!WARNING]` / `> [!IMPORTANT]`）：GEOSITE,cn 顺序坑、OpenClash `china_ip_route`；uci 命令收进 `<details>`，留一行回滚在外。「叠加秋风排 Jinx 之后」并入秋风节的 WARNING，不再两处重复。
  - ✅ 按既有口径自检：emoji 45 个（≥20）、行首规则（HTML 标签内 / 单元格起始豁免）、标题无 FE0F、目录锚点全命中、条数声明与文件一致。版式规范已同步 `skill/SKILL.md`「对外交付」。

## 2026-09-22

**变更**

- ✂️ **README 去掉一处「我们的选择」辩解** —— AWAvenue 那行原写「…会拦掉 Jinx 白名单里的 8 个域。**由对方托管，缓存不归我们管，故不列备用源。**」后半句是在解释**我们为什么只给 Raw 源**，属决策叙述，不是产品信息 —— 标题行「仅给 Raw 源」已把事实说清。已删，保留前半句（与白名单冲突是使用者要知道的）。
  - 📌 口径入 [`skill/SKILL.md`](skill/SKILL.md) 的分层原则：**README 只写产品当前状态**，不写归类自述 / 决策辩解 / 评审对话。
  - ✅ 地址字符串与条数一字未改，10 个地址照旧。

- 🎨 **emoji 密度补足：铺回行首，不进正文** —— 上一版每份文档只有标题挂 emoji、正文几乎全裸，用户反馈「emoji 不如之前丰富……现在好少」。本轮把 emoji 铺回**行首**：段落引导符（📦 ⭐ 🔁 🔀 🤝 ⚠️ 💡 📌 🔽 📄 📊）、表格单元格起始（规则顺序表 🛡️ / 🚫 / 🚦，文档表 📘 / 🧪 / 🗓️，来源表 📦 / ⚖️ / 📄 / 🧪）、无序列表项（⏳ 🧊 🔍 🎯 🌳 🧱 ⏭️ ✅）、文件结构树的各条目（🔷 / 🔶 / 📝 / 🧪 / 📁）以及详情文档的标题与目录。README **8 → 28** 个，`DetailsReadme` **16 → 56** 个。
  - 📌 **用户口径：emoji 只能出现在行首，不得落在句中**（原话「不得出现在句中，只能句首」）。故正文里不再有「上面用的是 ⭐ 首选 Raw」这类夹在句子中间的写法。
  - 🔍 已把这条口径固化成断言：校验脚本按「emoji 之前只许出现结构字符（标题 / 列表 / 引用标记、表格竖线、`[`、树形框线、缩进）」判定，并设密度下限（README ≥ 20 / `DetailsReadme` ≥ 40）—— 防止下次又被"克制"回去。校验器自测 12 例全对，含 3 个负样本（句中 / 行尾 / 箭头不算 emoji）。
  - 📎 表格单元格里的 emoji 属「单元格起始」，不算句中；标题 emoji 仍只用单码位（见下条 FE0F 坑）。

- 🎨 **标题补回 emoji；秋风规则并进「订阅」清单末尾** —— 上一版为追求克制把标题 emoji 全去掉，本轮补回：**每个标题带一个 emoji** 作视觉锚点（层级仍交给 `##` 与留白，`---` 分隔线继续不用）。同时把第三方 **AWAvenue 秋风广告规则**从独立的 `## 🤝 搭配 AWAvenue-Ads-Rule` 小节移进 `## 📥 订阅`：表格加两行与 Jinx 四份并列（用途列标「拦截 · 秋风」），地址块排在自家两源之后，落在**规则集清单的最下面**。
  - 📌 用户口径：第三方规则属规则集清单的一部分，「应该放到规则集的最下面，而不是 README 的最下边」。
  - ⚠️ **emoji 会改变锚点**：`## 📥 订阅` 的锚点是 `#-订阅`（emoji 被 slug 删掉后余下前导横线），`## 📥 1 规则集与白名单` 是 `#-1-规则集与白名单`。README 徽章里的 `](#-来源与许可)` 与 DetailsReadme 目录 8 条内链已同步，改标题时必须一起改。
  - 🐛 **踩坑：标题 emoji 不能带变体选择符（U+FE0F）** —— `⚙️` / `🛠️` 实际是「基字符 + FE0F」两个码位，而 FE0F 属 Mn 类、会被 slug **保留**，于是 `## ⚙️ OpenClash` 的真实锚点是 `#️-openclash`（`#` 后面跟一个看不见的字符），手写的 `#-openclash` **点不动**。已换成不含变体符的 `🔧` / `🚧`。**校验器第一版也栽在同一个坑里**：它用 `[^\w]` 做字符类，把 FE0F 当非单词字符删掉，于是给了假通过 —— 现已改为对齐 github-slugger 的保留集（L / M / N / Pc / Zs + `-`），并用 `github-slugger` 本体交叉验证（0 未命中）。

- 🧹 **README 精简重做（219 → 145 行），解释性内容整体下沉到 `DetailsReadme/DetailsReadme.md`** —— 原 README 8 个平级小节、每节一个 emoji 标题 + 一条 `---` 分隔线，地址、参数、原理、许可平铺在一起，读起来是「一大堆堆叠」。重做后**标题去掉全部 emoji、不再用 `---` 分隔线**（层级交给 `##` 和留白），小节按使用动线重排：订阅 → 接入 → 规则顺序 → OpenClash → 搭配 AWAvenue → 文档 → 来源与许可。
  - 📦 **新增 [`DetailsReadme/DetailsReadme.md`](DetailsReadme/DetailsReadme.md)**（8 章 145 行）：白名单推导、两个源的前缀与缓存判据（`?v=` 对 raw 无效 · 权威判据是 Contents API · purge 接口）、AWAvenue 的 `RULE-SET` vs 裸域名版（965 / 961 与 4 条 `DOMAIN-KEYWORD` 差额）、规则顺序验证法、转换原理表、OpenClash `china_ip_route` 的机理与回滚、文件结构、来源与许可。
  - 📌 **只搬不删**：所有实质信息一条未丢；地址字符串与条数一字未改，10 个地址照旧，已订阅的地址无需改动。README 里只剩操作信息与结论。

- 📊 **README「📥 规则集」改为表格呈现** —— 原来 4 份文件 × 2 个源 = 8 个 fenced 地址块平铺 70 余行，标题、条数、说明夹在块与块之间，找一份文件要翻半天。改为 **一张总览表**（客户端 / 文件 / 格式 / 条数 / 用途）+ **每个源一个地址块**（⭐ 首选 Raw 一块 4 行、🔁 备用 jsDelivr 一块 4 行）—— 块数 8 → 2。`### 🤝 搭配：AWAvenue-Ads-Rule` 同构处理：表格（客户端 / 格式 / 条数 / 说明）+ 单块 Raw 两行。
  - 📐 `skill/SKILL.md` 的地址版式规范同步改写为「**一张总览表 + 每个源一块 fenced 地址块**」，并把本次返工的理由写进文档（4 份 × 2 源 = 8 块时标题、条数、说明夹在块与块之间，读者找不到头），避免下次又拆成 8 块。
  - 📌 **纯版式重排，地址字符串与条数一字未改** —— 地址总数仍为 10 个（自家 8 + AWAvenue 2），已订阅的地址无需改动。AWAvenue 条数经复核确为其文件头自报值（v1.7.8：`RULE-SET` 965 / 裸域名版 961）。

- 🔗 **规则集地址改以 Raw GitHub 为首选源，CDN 降为备用源**：README 原先六处地址只给 jsDelivr，raw 仅在小字里带一句。改为**每个文件各给一块可复制地址** —— 自家 4 份文件「⭐ 首选 Raw GitHub / 🔁 备用 jsDelivr CDN」两块；**AWAvenue 两处只给 Raw**（第三方规则，由对方托管，其缓存我们 purge 不了，多列一个备用源等于把对方的缓存层写进本文档）。`## 🔷 mihomo / OpenClash` 与 `## 🔶 Surge` 的配置片段同步以 raw 为主，备用源的换法写在片段下方的说明行里；`skill/SKILL.md` 的「引用优先 …」条目与「对外交付 · 双地址」一并翻正（并注明第三方规则集只给 raw）。
  - 📌 **只调整推荐次序与呈现方式，地址字符串本身未变** —— 已订阅的地址一律无需改动。本轮列出的 10 个地址（自家 8 + AWAvenue 2）实测全部 **HTTP 200**。
  - 📌 依据：raw 是官方直读源，不经第三方 CDN，文件增删改名后与仓库一致、无需 purge；jsDelivr 多一层第三方缓存（删文件后不 purge 仍返回旧内容），但国内直连更稳 —— 保留为备用，不再当默认。
  - ⚠️ 实测补充：raw **不是**"推送即生效" —— 本轮推送后 raw 仍返回旧版，约 **3 分钟**才同步，`?v=<日期>` 对它无效。判断是否生效只能看 GitHub Contents API；这一条已写进 README 与 `skill/SKILL.md`。

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
