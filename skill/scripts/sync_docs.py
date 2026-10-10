#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""按真实读数同步文档里的全部声明（README / DetailsReadme / SKILL.md）。

## 为什么需要它

合并上游时最容易漏、且漏了**不会立刻报错**的环节，是「文档读数」：

  - 产物条数变了，但 README 徽章 / 订阅表 / 能力矩阵 / 详情表 / SKILL 预期读数
    是分散的 13 处独立文本，靠人逐处手改；
  - 上游版本号与快照日期还有 4 处（README 徽章、README 表格、README 页脚、
    Details 页脚），改漏了读者看到的还是旧版本 —— 而这**根本不影响闸门**，
    因为闸门那时只校验条数、不校验版本号。

本脚本把这件事变成一条命令：读产物 + 上游 `version.json` + `custom-*.list`，
推导出全部读数，再按锚点推平文档。**读数只有一个来源**，文档只是它的投影。

## 用法

    python skill/scripts/sync_docs.py           # dry-run：只打印将要改什么
    python skill/scripts/sync_docs.py --write   # 实际写入

跑完必须再跑闸门（`skill/tests/verify_jinx_src.py`）确认没有残余漂移。

## 与闸门的分工

  - 本脚本**写**：把文档推到真值。
  - 闸门**判**：断言文档声明 == 产物实际，不通过即判负。

两者共用同一套推导逻辑（本文件下方的 `derive`），所以不存在「脚本改完、
闸门仍判负」的错位。刻意不做成「闸门自动改文件」—— 判据自己改被检对象，
就不再是判据。
"""

import argparse
import json
import pathlib
import re
import sys


# ─────────────────────────────────────────────────────────────────────
# 读数推导：唯一的真值来源
# ─────────────────────────────────────────────────────────────────────

def _entries(path):
    """读一份列表文件的有效条目（去空行、去注释、去行尾空白）。"""
    out = []
    for line in path.read_text(encoding='utf-8').splitlines():
        s = line.strip()
        if s and not s.startswith('#'):
            out.append(s)
    return out


def _count_product(path):
    """数一份产物的条目数（三种格式各自的正文形态）。"""
    if path.suffix == '.json':
        data = json.loads(path.read_text(encoding='utf-8'))
        total = 0
        for rule in data.get('rules', []):
            for key in ('domain', 'domain_suffix', 'domain_regex'):
                total += len(rule.get(key) or [])
        return total
    if path.suffix == '.list':
        return len(_entries(path))
    # mihomo yaml：正文是 `  - 'GOAL,value'`
    return sum(1 for line in path.read_text(encoding='utf-8').splitlines()
               if line.startswith('  - '))


def _singbox_fields(path, keys):
    data = json.loads(path.read_text(encoding='utf-8'))
    rule = data['rules'][0]
    return {k: len(rule.get(k) or []) for k in keys}


def derive(root):
    """从仓根推导全部读数。缺上游源时抛 SystemExit 提示先取源。"""
    src = root / 'jinx-rules'
    vpath = src / 'version.json'
    if not vpath.is_file():
        sys.exit('❌ 缺 jinx-rules/version.json —— 先取上游源文件。\n'
                 '   见 SKILL.md「上游滚动时的标准流程」。')

    ver = json.loads(vpath.read_text(encoding='utf-8'))
    upstream = {
        'version': ver['version'],
        'date': ver['lastUpdate'][:10],
    }
    # 上游各源文件的实际条数（version.json 里也有一份计数，两者互为佐证）
    upstream['blk_fixed'] = len(_entries(src / 'blacklist.txt'))
    upstream['blk_wild'] = len(_entries(src / 'blacklist_wildcard.txt'))
    upstream['wl_fixed'] = len(_entries(src / 'whitelist.txt'))
    upstream['wl_wild'] = len(_entries(src / 'whitelist_wildcard.txt'))
    upstream['wl_total'] = upstream['wl_fixed'] + upstream['wl_wild']

    # guard 之后真正留存的白名单条数（会被黑名单误杀的那部分）
    sys.path.insert(0, str(root / 'skill' / 'scripts'))
    from convert_ruleset import build_blacklist_matcher  # noqa: E402
    collides = build_blacklist_matcher(
        [str(src / 'blacklist.txt')], [str(src / 'blacklist_wildcard.txt')])
    wl_all = _entries(src / 'whitelist.txt') + _entries(src / 'whitelist_wildcard.txt')
    upstream['wl_kept'] = sum(1 for e in wl_all if collides(e))

    # 产物条数
    products = {}
    for fam in ('ads', 'direct'):
        products[fam] = {
            'mihomo': _count_product(root / f'mihomo-{fam}.yaml'),
            'surge': _count_product(root / f'surge-{fam}.list'),
            'singbox': _count_product(root / f'sing-box-{fam}.json'),
        }
    ads_fields = _singbox_fields(root / 'sing-box-ads.json',
                                 ('domain', 'domain_suffix', 'domain_regex'))
    direct_fields = _singbox_fields(root / 'sing-box-direct.json',
                                    ('domain', 'domain_suffix'))

    custom = {
        'ads': _entries(root / 'custom-ads.list'),
        'direct': _entries(root / 'custom-direct.list'),
    }

    # ── 护栏：产物必须与上游 HEAD 同步，否则拒绝同步文档版本号 ────────────
    #
    # 这是本脚本最重要的一条断言。没有它就会出现「半同步」：产物还是旧上游
    # 生成的，文档却把版本号改成新上游 —— 文档对读者撒了一个静默的谎，而且
    # **条数断言全部会通过**（条数与产物自洽），没有任何门禁能发现。
    # 2026-10-10 定下规矩：只用上游最新版合并，不许拿旧版本产物去对文档。
    expect_ads = upstream['blk_fixed'] + upstream['blk_wild'] + len(custom['ads'])
    expect_direct = upstream['wl_kept'] + len(custom['direct'])
    if products['ads']['mihomo'] != expect_ads or products['direct']['mihomo'] != expect_direct:
        sys.exit(
            '❌ 产物与当前上游不同步，拒绝同步文档 —— 先重跑生成链。\n'
            f"   上游 {upstream['version']}（{upstream['date']}）应有："
            f'ads {expect_ads} / direct {expect_direct}\n'
            f"   仓内产物实际：ads {products['ads']['mihomo']} / "
            f"direct {products['direct']['mihomo']}\n"
            '   做法：按 SKILL.md「上游滚动时的标准流程」重跑两条生成命令，再回来同步文档。\n'
            '   （若上游其实没动、只是本地 jinx-rules/ 过期，同样先重取上游源。）')

    # 自洽检查：推导过程本身不许出现矛盾
    if len(set(products['ads'].values())) != 1 or len(set(products['direct'].values())) != 1:
        sys.exit(f'❌ 三格式条数不一致：{products} —— 先修产物，再谈同步文档。')
    if products['ads']['mihomo'] != sum(ads_fields.values()):
        sys.exit(f'❌ ads 条数与 sing-box 字段构成不符：'
                 f"{products['ads']['mihomo']} vs {ads_fields}")
    if products['direct']['mihomo'] != sum(direct_fields.values()):
        sys.exit(f'❌ direct 条数与 sing-box 字段构成不符：'
                 f"{products['direct']['mihomo']} vs {direct_fields}")
    if upstream['wl_kept'] + len(custom['direct']) != products['direct']['mihomo']:
        sys.exit(f"❌ 白名单推导式不闭合：上游留存 {upstream['wl_kept']} + "
                 f"手工 {len(custom['direct'])} != direct 产物 "
                 f"{products['direct']['mihomo']}")

    return {'upstream': upstream, 'products': products,
            'ads_fields': ads_fields, 'direct_fields': direct_fields,
            'custom': custom}


# ─────────────────────────────────────────────────────────────────────
# 锚点改写：每一处读数的定位与替换
# ─────────────────────────────────────────────────────────────────────

def _sub(text, label, pattern, repl, changes):
    """替换并把「改了/没改」记进 changes。找不到锚点时报错，不静默跳过。"""
    new, n = re.subn(pattern, repl, text)
    if n == 0:
        changes.append(('MISS', label, '锚点未命中 —— 文档版式变了，请同步更新本脚本'))
        return text
    if new != text:
        changes.append(('CHG', label, f'{n} 处'))
    return new


PRODUCT_FILES = {
    'ads': (('mihomo-ads.yaml', 'mihomo'),
            ('surge-ads.list', 'surge'),
            ('sing-box-ads.json', 'singbox')),
    'direct': (('mihomo-direct.yaml', 'mihomo'),
               ('surge-direct.list', 'surge'),
               ('sing-box-direct.json', 'singbox')),
}


def sync_readme(text, d, changes):
    u, p = d['upstream'], d['products']
    af, df = d['ads_fields'], d['direct_fields']

    text = _sub(text, 'README Source 徽章',
                r'(badge/Source-Jinx%20)([0-9][0-9.]*)',
                lambda m: m.group(1) + u['version'], changes)
    text = _sub(text, 'README 拦截徽章',
                r'(%E6%8B%A6%E6%88%AA-)(\d+)(%20%E6%9D%A1)',
                lambda m: m.group(1) + str(p['ads']['mihomo']) + m.group(3), changes)
    text = _sub(text, 'README 放行徽章',
                r'(%E6%94%BE%E8%A1%8C-)(\d+)(%20%E6%9D%A1)',
                lambda m: m.group(1) + str(p['direct']['mihomo']) + m.group(3), changes)

    for fam, files in PRODUCT_FILES.items():
        for fn, plat in files:
            text = _sub(
                text, f'README 订阅表 {fn}',
                r'(\[`' + re.escape(fn) + r'`\]\([^)]+\)\s*`?)(\d+)(`?)',
                lambda m, v=d['products'][fam][plat]: m.group(1) + str(v) + m.group(3),
                changes)

    text = _sub(
        text, 'README 矩阵拦截行',
        r'(\| 🚫 拦截 \| \*\*)(\d+)( 条\*\* \| )(\d+)( 条域名后缀 \+ )(\d+)( 条中缀通配 \|)',
        lambda m: (m.group(1) + str(p['ads']['mihomo']) + m.group(3)
                   + str(af['domain_suffix']) + m.group(5)
                   + str(af['domain_regex']) + m.group(7)), changes)
    text = _sub(
        text, 'README 矩阵放行行',
        r'(\| ✅ 放行 \| \*\*)(\d+)( 条\*\* \| )(\d+)( 条精确 \+ )(\d+)( 条后缀（含 )(\d+)( 条手工补充） \|)',
        lambda m: (m.group(1) + str(p['direct']['mihomo']) + m.group(3)
                   + str(df['domain']) + m.group(5)
                   + str(df['domain_suffix']) + m.group(7)
                   + str(len(d['custom']['direct'])) + m.group(9)), changes)
    text = _sub(
        text, 'README 上游快照行',
        r'(\| 📌 上游快照 \| `)([0-9][0-9.]*)(` · `)(\d{4}-\d{2}-\d{2})(` \|)',
        lambda m: m.group(1) + u['version'] + m.group(3) + u['date'] + m.group(5),
        changes)
    text = _sub(
        text, 'README 页脚上游行',
        r'(\| 📄 上游 \| \[`VME98/jinx-rules`\]\([^)]+\) · 数据 `)([0-9][0-9.]*)(` · `)(\d{4}-\d{2}-\d{2})(` \|)',
        lambda m: m.group(1) + u['version'] + m.group(3) + u['date'] + m.group(5),
        changes)
    return text


def sync_details(text, d, changes):
    u, p = d['upstream'], d['products']
    for fam, files in PRODUCT_FILES.items():
        for fn, plat in files:
            text = _sub(
                text, f'Details 表 {fn}',
                r'(\| `' + re.escape(fn) + r'` \|[^|]*\|\s*)(\d+)(\s*\|)',
                lambda m, v=d['products'][fam][plat]: m.group(1) + str(v) + m.group(3),
                changes)
    text = _sub(
        text, 'Details 白名单推导句',
        r'(上游白名单（)(\d+)( 条）中会被黑名单命中的 \*\*)(\d+)( 条\*\*，加 \*\*)(\d+)( 条\*\*手工补充（[^）]*），共 )(\d+)( 条。)',
        lambda m: (m.group(1) + str(u['wl_total']) + m.group(3)
                   + str(u['wl_kept']) + m.group(5)
                   + str(len(d['custom']['direct'])) + m.group(7)
                   + str(p['direct']['mihomo']) + m.group(9)), changes)
    # 括注里逐条列出的手工域名也要与源头条数一致 —— 条数对了、名单漏一个
    # 同样是对读者的误导（读者会据此以为只放了这几条）。
    m = re.search(r'加 \*\*(\d+) 条\*\*手工补充（([^）]*)）', text)
    if m:
        listed = re.findall(r'`\*\.?([^`]+)`', m.group(2))
        want = len(d['custom']['direct'])
        if int(m.group(1)) != want or len(listed) != want:
            changes.append(('MISS', 'Details 手工域名名单',
                            f'括注里只有 {len(listed)} 个域名，源头有 {want} 个 —— '
                            f'请在 sync_details 的名单处补齐（含每条的依据说明）'))
    text = _sub(
        text, 'Details 页脚上游行',
        r'(\| 📦 上游 \| \[`VME98/jinx-rules`\]\([^)]+\) · 数据 `)([0-9][0-9.]*)(` · `)(\d{4}-\d{2}-\d{2})(` \|)',
        lambda m: m.group(1) + u['version'] + m.group(3) + u['date'] + m.group(5),
        changes)
    return text


def sync_skill(text, d, changes):
    u, p = d['upstream'], d['products']
    af, df = d['ads_fields'], d['direct_fields']
    names = '、'.join(f'`*.{e.lstrip("*.")}`' if e.startswith('*.') else f'`{e}`'
                     for e in d['custom']['direct'])
    line = (f'预期读数：`ads {p["ads"]["mihomo"]}` / `direct {p["direct"]["mihomo"]}`'
            f'（上游白名单 {u["wl_total"]} 条 → guard 裁到 {u["wl_kept"]}，'
            f'再 +{len(d["custom"]["direct"])} extra-white：{names}）；'
            f'sing-box 侧 `ads: domain_suffix={af["domain_suffix"]} '
            f'domain_regex={af["domain_regex"]}` / '
            f'`direct: domain={df["domain"]} domain_suffix={df["domain_suffix"]}`。')
    text = _sub(text, 'SKILL 预期读数行', r'预期读数：`ads \d+`[^\n]*', line, changes)
    return text


TARGETS = {
    'README.md': sync_readme,
    'DetailsReadme/DetailsReadme.md': sync_details,
    'skill/SKILL.md': sync_skill,
}


def main():
    ap = argparse.ArgumentParser(description='按真实读数同步文档声明')
    ap.add_argument('--root', default=None, help='仓根（默认：本脚本上溯两级）')
    ap.add_argument('--write', action='store_true', help='实际写入（默认只演练）')
    args = ap.parse_args()

    # Windows 控制台默认 GBK，输出 emoji 会 UnicodeEncodeError 中断整个同步
    # （实测：写到一半崩掉，文件处于「部分同步」状态）。统一钉 utf-8，
    # 无法编码的字符降级为替代符而不是抛异常。
    for stream in (sys.stdout, sys.stderr):
        try:
            stream.reconfigure(encoding='utf-8', errors='replace')
        except (AttributeError, ValueError):
            pass

    root = (pathlib.Path(args.root).resolve() if args.root
            else pathlib.Path(__file__).resolve().parents[2])
    d = derive(root)

    print(f'上游快照 {d["upstream"]["version"]} · {d["upstream"]["date"]}'
          f'（黑名单 {d["upstream"]["blk_fixed"]}+{d["upstream"]["blk_wild"]}，'
          f'白名单 {d["upstream"]["wl_total"]} → guard 留存 {d["upstream"]["wl_kept"]}）')
    print(f'产物 ads {d["products"]["ads"]["mihomo"]} / '
          f'direct {d["products"]["direct"]["mihomo"]}')
    print()

    total_changed = 0
    missing = []
    for rel, fn in TARGETS.items():
        path = root / rel
        if not path.is_file():
            print(f'❌ {rel} 不存在')
            return 2
        old = path.read_text(encoding='utf-8')
        changes = []
        new = fn(old, d, changes)
        for kind, label, detail in changes:
            if kind == 'MISS':
                missing.append(f'{rel} :: {label}')
                print(f'  ⚠️  {rel} :: {label} —— {detail}')
            elif kind == 'CHG':
                total_changed += 1
                print(f'  ✏️  {rel} :: {label} —— {detail}')
        if new != old and args.write:
            # newline='' 显式钉 LF：与 .gitattributes / convert_ruleset.py 一致，
            # 否则 Windows 上 write_text 会按 os.linesep 写 CRLF（历史踩坑）。
            path.write_text(new, encoding='utf-8', newline='')
            print(f'  💾 {rel} 已写入')

    print()
    if missing:
        print(f'⚠️  {len(missing)} 处锚点未命中 —— 文档版式可能变了，'
              f'请同步更新 sync_docs.py 的锚点：')
        for m in missing:
            print(f'     - {m}')
        return 1
    if not args.write:
        print(f'（演练模式）将有 {total_changed} 处改写。加 --write 落盘。')
    else:
        print(f'✅ 同步完成，{total_changed} 处改写。'
              f'接着跑：python skill/tests/verify_jinx_src.py')
    return 0


if __name__ == '__main__':
    sys.exit(main())
