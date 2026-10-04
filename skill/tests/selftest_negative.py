#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""verify_jinx_src.py 的负样本自测 —— 证明闸门真能抓错，不是空转。

**为什么必须有这个文件**：一个只会全绿的闸门与没有闸门等价。本仓
`skill/SKILL.md` 记录过一次真实事故：某个检查「两半都恒空/恒 0」，
长期以绿形态存在，实际什么都没验 —— 被称为「永远绿的空操作」。
本脚本就是防这类退化的：它在临时副本仓里逐一制造典型错误，
要求 `verify_jinx_src.py` **判负**且命中预期分段。任何一种错误没被抓到，
本脚本即判负 —— 提示闸门出现了漏报。

退出码：0=全部抓到 / 1=有漏报（闸门不可信）。

用法:
  python skill/tests/selftest_negative.py
"""
import io
import json
import shutil
import subprocess
import sys
import tempfile
from pathlib import Path

for _s in ('stdout', 'stderr'):
    _f = getattr(sys, _s, None)
    if _f is not None and hasattr(_f, 'reconfigure'):
        try:
            _f.reconfigure(encoding='utf-8', errors='replace')
        except (ValueError, OSError):
            pass

ROOT = Path(__file__).resolve().parents[2]
TARGET = ROOT / 'skill' / 'tests' / 'verify_jinx_src.py'

CASES = []


def case(label, expect):
    """注册一个负样本：label 说明制造的错误，expect 是应命中的分段关键词。"""
    def deco(fn):
        CASES.append((label, expect, fn))
        return fn
    return deco


@case('手改产物：白名单 mihomo 删掉一条', '条数一致')
def _(w):
    p = w / 'mihomo-white-guard.yaml'
    lines = p.read_text(encoding='utf-8').splitlines()
    idx = next(i for i, l in enumerate(lines) if l.strip().startswith('- '))
    lines.pop(idx)
    p.write_text('\n'.join(lines) + '\n', encoding='utf-8')


@case('手改产物：只把表头自述条数改掉', '文件头 # entries')
def _(w):
    p = w / 'surge-white-guard.list'
    t = p.read_text(encoding='utf-8').replace('# entries: ', '# entries: 99 # ')
    lines = [l for l in t.splitlines()]
    for i, l in enumerate(lines):
        if l.startswith('# entries:'):
            lines[i] = '# entries: 99'
    p.write_text('\n'.join(lines) + '\n', encoding='utf-8')


@case('手改产物：sing-box 少一条（跨格式差异）', '跨格式语义等价')
def _(w):
    p = w / 'sing-box-white-guard.json'
    d = json.loads(p.read_text(encoding='utf-8'))
    for rule in d['rules']:
        for v in rule.values():
            if v:
                v.pop()
                break
        break
    p.write_text(json.dumps(d, ensure_ascii=False, indent=2) + '\n', encoding='utf-8')


@case('文档漂移：README 订阅表条数写错', '文档条数声明')
def _(w):
    """把订阅表里某个文件的条数改错。

    兼容两种合法表格形态（见 verify_jinx_src.py 第 5 段）：
      A 独立单元格： | `f` | 44 |
      B 内嵌链接：   [`f`](URL) `44`
    两种都试，确保本负样本在版式演进后依然有效。
    实测教训（2026-10-04）：只匹配形态 A 时，README 改成形态 B 后本负样本
    静默失效（改不动文件 → 断言自然不报错 → 被误读成「漏报」）。
    """
    p = w / 'README.md'
    t = p.read_text(encoding='utf-8')
    for old, new in [
        ('[`surge-white-guard.list`](https://raw.githubusercontent.com/'
         'RiverFlowsInUUU/Jinx/main/surge-white-guard.list) `44`',
         '[`surge-white-guard.list`](https://raw.githubusercontent.com/'
         'RiverFlowsInUUU/Jinx/main/surge-white-guard.list) `50`'),
        ('| `surge-white-guard.list` | 44 |', '| `surge-white-guard.list` | 50 |'),
    ]:
        if old in t:
            t = t.replace(old, new)
            break
    else:
        raise AssertionError('负样本失效：README 订阅表两种形态都没匹配到')
    p.write_text(t, encoding='utf-8')


@case('源头改了没重跑：custom-direct.list 追加一条', '源头 custom')
def _(w):
    p = w / 'custom-direct.list'
    p.write_text(p.read_text(encoding='utf-8') + '*.selftest-not-real.net\n',
                 encoding='utf-8')


@case('文案违规：emoji 落在句中', '文案规范')
def _(w):
    """在正文句子中间塞一个 emoji。

    用 ⭐（U+2B50）—— 它与箭头（→ U+2192、⬅ U+2B05）同处一位区段，
    专门守「把整段当箭头排除」这类漏报（2026-10-04 真实踩过）。

    ⚠️ 锚点必须选**当前 README 里真实存在**的行。实测教训：本负样本原锚在
    `⭐ **Raw GitHub** · 首选` 上，该行随裸 URL 块一起被删除后，负样本静默
    失效（`replace` 无命中 → 文件没被改 → 断言不报错 → 被误读成「漏报」）。
    故此处改为**动态选择**：取第一个非空、非标题、不含 emoji 的正文行来注入。
    """
    p = w / 'README.md'
    lines = p.read_text(encoding='utf-8').split('\n')
    for i, l in enumerate(lines):
        s = l.strip()
        if not s or s.startswith(('#', '|', '>', '```', '<', '- ', '*')):
            continue
        if v := __import__('re').search(
                '[\U0001F300-\U0001FAFF\U00002600-\U000027BF\U00002B00-\U00002BFF]', s):
            continue
        lines[i] = '上面用的是 ⭐ 首选 Raw，' + s
        break
    else:
        raise AssertionError('负样本失效：README 里找不到可注入的正文行')
    p.write_text('\n'.join(lines), encoding='utf-8')


@case('平台清单缺一端：仓库简介漏 sing-box（第 10 段）', '平台清单齐备')
def _(w):
    """把建仓脚本里的简介默认值还原成漏 sing-box 的旧值。

    这是**真实发生过的缺陷**：2026-09-28 加入 sing-box 后，README / 接入节 /
    徽章都更新了，但仓库简介（GitHub 页面顶部、列表、搜索结果都显示它）漏了
    整整一周无人发现 —— 因为它存在建仓脚本的 `--description` 默认值里，
    平时没人会打开那个文件看。
    """
    p = w / 'skill' / 'scripts' / 'upload_to_github.py'
    t = p.read_text(encoding='utf-8')
    # ⚠️ 锚点会随平台增删而过期 —— 这里断言必须命中，否则抛错而非静默通过
    #    （实测：加入 Egern 后本锚点曾失效并被自测当场抓出）。
    old = 'mihomo / Surge / Egern / sing-box'
    assert old in t, '负样本失效：简介默认值里已无预期文本（平台清单可能又变了）'
    p.write_text(t.replace(old, 'mihomo / Surge / Egern', 1), encoding='utf-8')


@case('平台清单缺一端：转换原理表头去掉 sing-box 列（第 10 段）', '平台清单齐备')
def _(w):
    """表格表头少一个平台列 —— 属「清单类位置」的平台缺失。

    ⚠️ 本条守的是第 10 段的**判据强度**：早期实现只判「全文出现过平台名」，
    这种删表格列的做法照样全绿（别处仍有 sing-box 字样）。现已锚定到
    结构性位置（徽章行 / 订阅表行 / 折叠块标头 / 表头 / 简介默认值）。
    """
    p = w / 'DetailsReadme' / 'DetailsReadme.md'
    t = p.read_text(encoding='utf-8')
    old = '| 上游写法 | 含义 | mihomo | Surge | Egern | sing-box |'
    assert old in t, '负样本失效：转换原理表头已改版（平台列可能又变了）'
    p.write_text(t.replace(old, '| 上游写法 | 含义 | mihomo | Surge | Egern |', 1),
                 encoding='utf-8')


def main():
    if not TARGET.is_file():
        print(f'❌ 前置不达标：找不到 {TARGET}')
        return 2
    print(f'被检脚本: {TARGET}')
    print(f'负样本数: {len(CASES)}\n')

    caught = missed = 0
    for label, expect, sabotage in CASES:
        with tempfile.TemporaryDirectory() as tmp:
            work = Path(tmp) / 'repo'
            shutil.copytree(ROOT, work,
                            ignore=shutil.ignore_patterns('.git', 'jinx-rules',
                                                          '__pycache__', '_regen'))
            sabotage(work)
            proc = subprocess.run(
                [sys.executable, str(TARGET), '--root', str(work)],
                capture_output=True, text=True, encoding='utf-8', errors='replace')
            out = proc.stdout or ''
            ok = proc.returncode == 1 and expect in out
            if ok:
                caught += 1
                hits = [l.strip() for l in out.splitlines() if l.strip().startswith('❌')]
                print(f'  ✅ {label}')
                print(f'      exit=1，命中「{expect}」｜{hits[0] if hits else ""}')
            else:
                missed += 1
                print(f'  ❌ {label}')
                print(f'      **漏报**：预期 exit=1 且命中「{expect}」，实际 exit={proc.returncode}')
                tail = (out or proc.stderr or '').strip().splitlines()[-6:]
                for l in tail:
                    print(f'      | {l}')

    print(f'\n负样本结果: {caught} 抓到, {missed} 漏报')
    if missed:
        print('⚠️  存在漏报 —— 闸门的判据有盲区，不可信。请修 verify_jinx_src.py。')
        return 1
    print('✅ 全部典型错误都能被判负 —— 闸门不是空转。')
    return 0


if __name__ == '__main__':
    sys.exit(main())
