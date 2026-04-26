#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
IBK Geni-Code 보안 보고서용 흐름도 생성 스크립트
- D1: 기존 프로그램 반영 체계 흐름도
- D2: 통제 Before/After 비교도 (Geni-Code 사용 시 사각지대)

영일피혁 경영보고서 스타일(Navy/Gold/Cyan) 적용.
"""

import os
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import matplotlib.font_manager as fm
from matplotlib.patches import FancyBboxPatch, FancyArrowPatch, Rectangle
from matplotlib.lines import Line2D

FONT_PATH = "C:/Windows/Fonts/malgun.ttf"
FONT_BOLD_PATH = "C:/Windows/Fonts/malgunbd.ttf"
OUT_DIR = os.path.dirname(os.path.abspath(__file__))

font_prop = fm.FontProperties(fname=FONT_PATH)
font_bold = fm.FontProperties(fname=FONT_BOLD_PATH)
fm.fontManager.addfont(FONT_PATH)
fm.fontManager.addfont(FONT_BOLD_PATH)
plt.rcParams['font.family'] = font_prop.get_name()
plt.rcParams['axes.unicode_minus'] = False

HEX_NAVY = '#002040'
HEX_BLUE = '#005288'
HEX_ACCENT = '#0091C8'
HEX_GOLD = '#B49632'
HEX_RED = '#C83232'
HEX_GRAY = '#646464'
HEX_LIGHT = '#F5F7FA'
HEX_WARN_BG = '#FFF5F5'


def _box(ax, x, y, w, h, text, fill=HEX_NAVY, fg='white', fs=9, bold=True):
    box = FancyBboxPatch((x, y), w, h,
                         boxstyle="round,pad=0.02,rounding_size=0.08",
                         linewidth=1.0, edgecolor=fill, facecolor=fill)
    ax.add_patch(box)
    ax.text(x + w/2, y + h/2, text,
            ha='center', va='center', color=fg, fontsize=fs,
            fontproperties=(font_bold if bold else font_prop))


def _ghost_box(ax, x, y, w, h, text, edge=HEX_GRAY, fg=HEX_GRAY, fs=8, bg='white'):
    box = FancyBboxPatch((x, y), w, h,
                         boxstyle="round,pad=0.02,rounding_size=0.08",
                         linewidth=1.0, edgecolor=edge, facecolor=bg,
                         linestyle='--')
    ax.add_patch(box)
    ax.text(x + w/2, y + h/2, text,
            ha='center', va='center', color=fg, fontsize=fs,
            fontproperties=font_prop)


def _arrow(ax, x1, y1, x2, y2, color=HEX_NAVY, lw=1.5, style='->'):
    a = FancyArrowPatch((x1, y1), (x2, y2),
                        arrowstyle=style, color=color,
                        mutation_scale=14, linewidth=lw)
    ax.add_patch(a)


def _label(ax, x, y, text, fs=8, color=HEX_GRAY, bold=False, ha='center'):
    ax.text(x, y, text, ha=ha, va='center',
            fontsize=fs, color=color,
            fontproperties=(font_bold if bold else font_prop))


# ──────────────────────────────────────────────────────────────
# D1: 기존 프로그램 반영 체계 흐름도
# ──────────────────────────────────────────────────────────────
def diagram_current_flow(path):
    fig, ax = plt.subplots(figsize=(11, 4.8))
    ax.set_xlim(0, 11)
    ax.set_ylim(0, 4.8)
    ax.axis('off')

    # Title
    _label(ax, 5.5, 4.5, '[현행] 프로그램 작성·반영 체계', fs=13, color=HEX_NAVY, bold=True)

    # Stage boxes (top row)
    stages = [
        (0.5, 'Dev (개발서버)', '작성·단위테스트'),
        (3.2, 'QA 서버', '통합·기능 검증'),
        (5.9, '운영 서버', '실배포'),
    ]
    for x, title, sub in stages:
        _box(ax, x, 2.6, 2.3, 0.9, title, fill=HEX_NAVY, fg='white', fs=11)
        _label(ax, x + 1.15, 2.35, sub, fs=8, color=HEX_GRAY)

    # Arrows between stages
    _arrow(ax, 2.8, 3.05, 3.2, 3.05, color=HEX_NAVY, lw=2.0)
    _arrow(ax, 5.5, 3.05, 5.9, 3.05, color=HEX_NAVY, lw=2.0)

    # Final deployment target (right-end)
    _box(ax, 8.6, 2.6, 2.1, 0.9, '업무 시스템', fill=HEX_BLUE, fg='white', fs=11)
    _label(ax, 9.65, 2.35, '계정계·스마트뱅킹·여신지원 등', fs=7, color=HEX_GRAY)
    _arrow(ax, 8.2, 3.05, 8.6, 3.05, color=HEX_NAVY, lw=2.0)

    # Control gates (below arrows)
    gate_y = 1.4
    _box(ax, 0.5, gate_y, 2.3, 0.6, '신규: 부장 결재 / 변경: 팀장 결재',
         fill=HEX_GOLD, fg='white', fs=8)
    _box(ax, 3.2, gate_y, 2.3, 0.6, '변경관리 시스템 등록',
         fill=HEX_GOLD, fg='white', fs=9)
    _box(ax, 5.9, gate_y, 2.3, 0.6, '형상관리·배포 통제',
         fill=HEX_GOLD, fg='white', fs=9)

    # Upward connectors (gate → stage)
    for x in [1.65, 4.35, 7.05]:
        _arrow(ax, x, 2.0, x, 2.6, color=HEX_GOLD, lw=1.2, style='-')

    # Creator note (far left)
    _label(ax, 0.5, 0.6,
           '작성 주체와 무관: 사람 / IBK Geni-Code / AIDD(외부 AI 솔루션) 모두 동일 경로',
           fs=9, color=HEX_NAVY, bold=True, ha='left')
    _label(ax, 0.5, 0.25,
           '→ 본 경로를 통과한 산출물은 내부통제·보안상 문제 없음',
           fs=9, color=HEX_BLUE, bold=False, ha='left')

    plt.savefig(path, dpi=200, bbox_inches='tight', facecolor='white')
    plt.close(fig)
    return path


# ──────────────────────────────────────────────────────────────
# D2: Before / After 비교도 (Geni-Code 사용 시 통제 사각지대)
# ──────────────────────────────────────────────────────────────
def diagram_gap(path):
    fig, ax = plt.subplots(figsize=(11, 6.0))
    ax.set_xlim(0, 11)
    ax.set_ylim(0, 6.0)
    ax.axis('off')

    # Title
    _label(ax, 5.5, 5.7, '[쟁점] 업무용 PC Python 실행 허용이 만드는 통제 사각지대',
           fs=13, color=HEX_NAVY, bold=True)

    # ── Upper row: BEFORE (통제 경로) ─────────────
    _label(ax, 0.3, 4.95, 'BEFORE', fs=11, color=HEX_BLUE, bold=True, ha='left')
    _label(ax, 1.6, 4.95, '기존 통제 경로 (결재·QA·변경관리 적용)',
           fs=10, color=HEX_GRAY, ha='left')

    _box(ax, 0.5, 3.9, 1.9, 0.7, '개발자 / Geni-Code\n산출물', fill=HEX_NAVY, fs=9)
    _box(ax, 2.9, 3.9, 1.6, 0.7, '결재', fill=HEX_GOLD, fs=10)
    _box(ax, 5.0, 3.9, 1.9, 0.7, 'QA 검증', fill=HEX_GOLD, fs=10)
    _box(ax, 7.4, 3.9, 2.0, 0.7, '변경관리 시스템', fill=HEX_GOLD, fs=10)
    _box(ax, 9.9, 3.9, 0.9, 0.7, '운영', fill=HEX_BLUE, fs=10)

    for x1, x2 in [(2.4, 2.9), (4.5, 5.0), (6.9, 7.4), (9.4, 9.9)]:
        _arrow(ax, x1, 4.25, x2, 4.25, color=HEX_NAVY, lw=1.8)

    # ── Divider ─────────────
    ax.add_patch(Rectangle((0.3, 3.1), 10.5, 0.02, color=HEX_GRAY, alpha=0.5))

    # ── Lower row: AFTER (사각지대) ─────────────
    _label(ax, 0.3, 2.7, 'AFTER', fs=11, color=HEX_RED, bold=True, ha='left')
    _label(ax, 1.6, 2.7, '업무PC에 Python 실행 허용 시 신설되는 경로',
           fs=10, color=HEX_GRAY, ha='left')

    # Shadow path
    _box(ax, 0.5, 1.6, 1.9, 0.7, '직원', fill=HEX_NAVY, fs=10)
    _box(ax, 2.9, 1.6, 1.9, 0.7, 'Geni-Code 요청\n(코드 생성)', fill=HEX_ACCENT, fs=9)
    _box(ax, 5.3, 1.6, 2.0, 0.7, '업무PC에서\nPython 직접 실행', fill=HEX_RED, fs=9)
    _box(ax, 7.8, 1.6, 2.9, 0.7, '업무 데이터·파일·네트워크 접근',
         fill=HEX_RED, fs=9)

    for x1, x2 in [(2.4, 2.9), (4.8, 5.3), (7.3, 7.8)]:
        _arrow(ax, x1, 1.95, x2, 1.95, color=HEX_RED, lw=1.8)

    # Bypassed gates (dashed ghosts)
    _ghost_box(ax, 2.9, 0.6, 1.6, 0.55, '결재 (우회)', edge=HEX_GRAY, fg=HEX_GRAY)
    _ghost_box(ax, 5.0, 0.6, 1.9, 0.55, 'QA 검증 (우회)', edge=HEX_GRAY, fg=HEX_GRAY)
    _ghost_box(ax, 7.4, 0.6, 2.0, 0.55, '변경관리 (우회)', edge=HEX_GRAY, fg=HEX_GRAY)
    _label(ax, 0.5, 0.25, '※ 위 통제 지점이 우회됨 → 감사·추적 불가',
           fs=8, color=HEX_RED, bold=True, ha='left')

    plt.savefig(path, dpi=200, bbox_inches='tight', facecolor='white')
    plt.close(fig)
    return path


if __name__ == '__main__':
    p1 = diagram_current_flow(os.path.join(OUT_DIR, 'geni-code_d1_current_flow.png'))
    p2 = diagram_gap(os.path.join(OUT_DIR, 'geni-code_d2_gap.png'))
    print('Generated:', p1)
    print('Generated:', p2)
