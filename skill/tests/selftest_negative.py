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
    p = w / 'README.md'
    t = p.read_text(encoding='utf-8')
    t = t.replace('| `surge-white-guard.list` | 44 |', '| `surge-white-guard.list` | 50 |')
    p.write_text(t, encoding='utf-8')


@case('源头改了没重跑：custom-direct.list 追加一条', '源头 custom')
def _(w):
    p = w / 'custom-direct.list'
    p.write_text(p.read_text(encoding='utf-8') + '*.selftest-not-real.net\n',
                 encoding='utf-8')


@case('文案违规：emoji 落在句中', '文案规范')
def _(w):
    p = w / 'README.md'
    t = p.read_text(encoding='utf-8')
    # ⭐ 是 U+2B50 —— 与箭头（U+2192 / U+2B05）同段，专门用来防「整段排除」的漏报
    t = t.replace('⭐ **Raw GitHub** · 首选', '上面用的是 ⭐ 首选 Raw')
    p.write_text(t, encoding='utf-8')


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
