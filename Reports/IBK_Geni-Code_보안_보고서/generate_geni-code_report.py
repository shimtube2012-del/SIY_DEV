#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
IBK Geni-Code 도입 관련 보안 검토 보고서 PDF 생성
참조 양식: 영일피혁_경영보고서_2026.pdf (C:/SIY_DEV/영일피혁/generate_report.py)
"""

import os
from fpdf import FPDF

# ── Configuration ──────────────────────────────────────────────
FONT_PATH = "C:/Windows/Fonts/malgun.ttf"
FONT_BOLD_PATH = "C:/Windows/Fonts/malgunbd.ttf"
OUTPUT_DIR = os.path.dirname(os.path.abspath(__file__))
OUTPUT_PDF = os.path.join(OUTPUT_DIR, "IBK_Geni-Code_보안_보고서_2026.pdf")
D1_PATH = os.path.join(OUTPUT_DIR, "geni-code_d1_current_flow.png")
D2_PATH = os.path.join(OUTPUT_DIR, "geni-code_d2_gap.png")

AUTHOR_DEPT = "디지털혁신부"
AUTHOR_NAME = "팀장 심일용"
ISSUE_MONTH = "2026년 4월"
HEADER_TEXT = "IBK Geni-Code 보안 검토 보고서  |  Confidential"

# Colors (영일피혁 원본 팔레트)
C_NAVY = (0, 32, 63)
C_BLUE = (0, 82, 136)
C_ACCENT = (0, 145, 200)
C_RED = (200, 50, 50)
C_GRAY = (100, 100, 100)
C_LIGHT_GRAY = (230, 230, 230)
C_WHITE = (255, 255, 255)
C_GOLD = (180, 150, 50)


# ══════════════════════════════════════════════════════════════
# PDF CLASS
# ══════════════════════════════════════════════════════════════
class ReportPDF(FPDF):
    def __init__(self):
        super().__init__(orientation='P', unit='mm', format='A4')
        self.add_font('malgun', '', FONT_PATH)
        self.add_font('malgun', 'B', FONT_BOLD_PATH)
        self.set_auto_page_break(auto=True, margin=20)
        self._is_cover = False
        self._is_toc = False
        self.toc_entries = []

    def header(self):
        if self._is_cover or self._is_toc:
            return
        if self.page_no() <= 1:
            return
        self.set_font('malgun', '', 7)
        self.set_text_color(*C_GRAY)
        self.set_y(8)
        self.cell(0, 5, HEADER_TEXT, align='R')
        self.set_draw_color(*C_NAVY)
        self.set_line_width(0.3)
        self.line(10, 15, 200, 15)
        self.set_y(18)

    def footer(self):
        if self.page_no() == 1:
            return
        self.set_y(-15)
        self.set_font('malgun', '', 7)
        self.set_text_color(*C_GRAY)
        self.set_draw_color(*C_LIGHT_GRAY)
        self.line(10, self.get_y() - 2, 200, self.get_y() - 2)
        self.cell(95, 8, '© 2026 IBK. Confidential', align='L')
        self.cell(95, 8, f'{self.page_no()}', align='R')

    # ── Section Titles ────────────────────────────────────────
    def section_title(self, number, title, level=1):
        if level == 1:
            # Ensure at least body lines fit after title
            if self.get_y() + 10 + 15 > 270:
                self.add_page()
            self.toc_entries.append((number, title, self.page_no()))
            self.set_font('malgun', 'B', 16)
            self.set_text_color(*C_NAVY)
            self.set_fill_color(*C_NAVY)
            self.rect(10, self.get_y(), 3, 10, 'F')
            self.set_x(17)
            self.cell(0, 10, f'{number}. {title}', ln=True)
            self.ln(3)
        elif level == 2:
            if self.get_y() + 8 + 12 > 270:
                self.add_page()
            self.set_x(10)
            self.set_font('malgun', 'B', 12)
            self.set_text_color(*C_BLUE)
            self.cell(0, 8, f'{number} {title}', ln=True)
            self.ln(1)

    def sub_heading(self, text):
        if self.get_y() + 7 + 12 > 270:
            self.add_page()
        self.set_x(10)
        self.set_font('malgun', 'B', 10)
        self.set_text_color(*C_NAVY)
        self.cell(0, 7, text, ln=True)
        self.ln(1)

    # ── Body Text ─────────────────────────────────────────────
    def body_text(self, text, indent=0):
        self.set_font('malgun', '', 9)
        self.set_text_color(40, 40, 40)
        if indent:
            self.set_x(10 + indent)
        self.multi_cell(190 - indent, 5.5, text)
        self.ln(1)

    def bullet(self, text, indent=15):
        self.set_font('malgun', '', 9)
        self.set_text_color(40, 40, 40)
        self.set_x(indent)
        self.cell(4, 5.5, '•')
        self.multi_cell(190 - indent - 4, 5.5, text)

    # ── Key Finding Box ───────────────────────────────────────
    def key_finding(self, number, title, text):
        # Estimate needed height: title ~6 + wrapped body
        # Rough guess: 18~22 mm
        if self.get_y() + 22 > 270:
            self.add_page()
        y = self.get_y()
        self.set_fill_color(*C_NAVY)
        self.set_text_color(*C_WHITE)
        self.set_font('malgun', 'B', 11)
        self.set_x(12)
        self.cell(8, 8, str(number), fill=True, align='C')

        # Title (bold) next to number
        self.set_xy(22, y)
        self.set_text_color(*C_NAVY)
        self.set_font('malgun', 'B', 10)
        self.multi_cell(175, 5.5, title)

        # Body text below, aligned to x=22
        self.set_x(22)
        self.set_text_color(40, 40, 40)
        self.set_font('malgun', '', 9)
        self.multi_cell(175, 5.5, text)
        self.ln(2)

    # ── Table ─────────────────────────────────────────────────
    def add_table(self, headers, data, col_widths=None, header_color=None,
                  align_first_left=True):
        if header_color is None:
            header_color = C_NAVY
        if col_widths is None:
            n = len(headers)
            col_widths = [190 / n] * n

        needed = 8 + len(data) * 6.5 + 5
        if self.get_y() + needed > 270:
            self.add_page()

        self.set_font('malgun', 'B', 8)
        self.set_fill_color(*header_color)
        self.set_text_color(*C_WHITE)
        for i, h in enumerate(headers):
            if i == 0 and align_first_left:
                align = 'L'
            else:
                align = 'C'
            self.cell(col_widths[i], 7, h, border=0, fill=True, align=align)
        self.ln()

        self.set_font('malgun', '', 8)
        self.set_text_color(40, 40, 40)
        for row_idx, row in enumerate(data):
            if row_idx % 2 == 0:
                self.set_fill_color(245, 247, 250)
            else:
                self.set_fill_color(*C_WHITE)
            for i, cell in enumerate(row):
                if i == 0 and align_first_left:
                    align = 'L'
                else:
                    align = 'L'
                self.cell(col_widths[i], 6.5, str(cell), border=0, fill=True, align=align)
            self.ln()
        self.ln(3)

    # ── Chart / Image ─────────────────────────────────────────
    def add_image(self, path, w=170, caption=None):
        # PNG aspect varies; estimate using file read is overkill. Assume ~0.5 ratio
        est_h = w * 0.52
        if self.get_y() + est_h + 8 > 270:
            self.add_page()
        x = (210 - w) / 2
        self.image(path, x=x, y=self.get_y(), w=w)
        self.set_y(self.get_y() + est_h + 2)
        if caption:
            self.set_font('malgun', '', 7)
            self.set_text_color(*C_GRAY)
            self.cell(0, 4, caption, align='C', ln=True)
            self.ln(3)

    # ── Callout Box ───────────────────────────────────────────
    def callout_box(self, title, text, accent=None, body_lines=3):
        if accent is None:
            accent = C_ACCENT
        est_h = 8 + body_lines * 5
        if self.get_y() + est_h > 270:
            self.add_page()
        y = self.get_y()
        self.set_fill_color(*accent)
        self.rect(10, y, 3, est_h - 2, 'F')
        self.set_fill_color(240, 248, 255)
        self.rect(13, y, 187, est_h - 2, 'F')
        self.set_xy(16, y + 2)
        self.set_font('malgun', 'B', 9)
        self.set_text_color(*C_NAVY)
        self.cell(0, 5, title, ln=True)
        self.set_x(16)
        self.set_font('malgun', '', 8)
        self.set_text_color(40, 40, 40)
        self.multi_cell(180, 4.5, text)
        self.set_y(y + est_h)
        self.ln(2)


# ══════════════════════════════════════════════════════════════
# REPORT ASSEMBLY
# ══════════════════════════════════════════════════════════════
def build_report():
    pdf = ReportPDF()

    # ── COVER PAGE ─────────────────────────────────────────────
    pdf._is_cover = True
    pdf.add_page()
    pdf.set_fill_color(*C_NAVY)
    pdf.rect(0, 0, 210, 160, 'F')

    pdf.set_y(50)
    pdf.set_font('malgun', 'B', 28)
    pdf.set_text_color(*C_WHITE)
    pdf.cell(0, 15, 'IBK 기업은행', align='C', ln=True)
    pdf.set_font('malgun', 'B', 20)
    pdf.cell(0, 12, 'Geni-Code 도입 관련', align='C', ln=True)
    pdf.cell(0, 12, '보안 검토 보고서', align='C', ln=True)
    pdf.ln(6)
    pdf.set_draw_color(*C_GOLD)
    pdf.set_line_width(0.8)
    pdf.line(60, pdf.get_y(), 150, pdf.get_y())
    pdf.ln(8)
    pdf.set_font('malgun', '', 14)
    pdf.set_text_color(200, 200, 220)
    pdf.cell(0, 8, ISSUE_MONTH, align='C', ln=True)

    pdf.set_y(175)
    pdf.set_font('malgun', '', 10)
    pdf.set_text_color(*C_GRAY)
    pdf.cell(0, 7, 'CONFIDENTIAL', align='C', ln=True)
    pdf.set_font('malgun', '', 9)
    pdf.cell(0, 6, '본 보고서는 내부 경영검토 목적으로 작성되었으며,', align='C', ln=True)
    pdf.cell(0, 6, '사전 서면 동의 없이 외부 배포를 금합니다.', align='C', ln=True)
    pdf.ln(10)
    pdf.set_font('malgun', '', 9)
    pdf.set_text_color(120, 120, 120)
    pdf.cell(0, 6, '원본 자료: IBK Geni-Code 보안관련 유의사항 (2026.04)', align='C', ln=True)
    pdf.cell(0, 6, f'작성: {AUTHOR_DEPT} {AUTHOR_NAME}', align='C', ln=True)
    pdf._is_cover = False

    # ── EXECUTIVE SUMMARY ──────────────────────────────────────
    pdf.add_page()
    pdf.section_title('I', 'Executive Summary')

    pdf.sub_heading('핵심 발견사항 (Key Findings)')

    pdf.key_finding(
        1,
        '기존 서버시스템에 반영되는 산출물 통제는 기존 체계로 충분하다',
        'IBK의 개발-QA-운영 3단계 프로세스, 부장·팀장 결재, 변경관리 시스템은 '
        '작성 주체(사람·IBK Geni-Code·AIDD 외부 솔루션)와 무관하게 동일하게 적용된다. '
        '따라서 본 경로를 통과한 Geni-Code 산출물은 내부통제·보안상 문제가 없다.'
    )
    pdf.key_finding(
        2,
        '쟁점은 산출물이 아닌 "실행 환경"에 있다',
        'Geni-Code 사용을 위해 업무용 PC에서 Python 실행뿐 아니라 '
        'Flask·Django·Tomcat 등 웹서버·WAS의 기동까지 허용해야 한다. '
        '업무용 PC는 본래 "허가된 프로그램만 실행" 원칙(앱 화이트리스트)으로 통제되어 온 '
        '클라이언트 전용 장비로, 이 같은 실행 허용은 예외일 뿐 아니라 '
        '업무PC를 사실상 서버로 전환시켜 공격 표면을 크게 확대한다.'
    )
    pdf.key_finding(
        3,
        '기술적 통제만으로는 부족 — 행위적·관리적 통제 병행 필요',
        '망분리·앱 화이트리스트 등 기술적 통제는 Python 허용으로 실질 무력화된다. '
        '사용자를 전제로 한 보안 서약·실행환경 제한·로그 감사·교육을 병행해야 '
        'Geni-Code의 생산성과 내부통제를 동시에 확보할 수 있다.'
    )

    pdf.ln(2)
    pdf.sub_heading('대응 방안 우선순위')
    pdf.add_table(
        ['우선순위', '과제', '기대 효과'],
        [
            ['1순위', 'Geni-Code 사용자 보안 서약서 도입', '행위적 통제 확보, 위반 시 책임 명확화'],
            ['2순위', '업무PC 실행환경 제한·로그 감사 (Python·웹서버·WAS)', '쉐도우IT·비인가 자동화·서버화 탐지'],
            ['3순위', '허용 라이브러리 화이트리스트·모델 무결성·PII 차단', '외부 패키지 및 모델 경유 유입 위협 예방'],
            ['4순위', 'IBK AI 거버넌스 프레임워크 수립 (VI장)', '업무PC 실행 사용 패턴의 통제 체제 공백 해소'],
        ],
        col_widths=[22, 78, 90]
    )

    # ── TABLE OF CONTENTS ──────────────────────────────────────
    pdf._is_toc = True
    pdf.add_page()
    pdf.set_font('malgun', 'B', 20)
    pdf.set_text_color(*C_NAVY)
    pdf.cell(0, 15, '목  차', align='C', ln=True)
    pdf.ln(8)

    toc_items = [
        ('I', 'Executive Summary'),
        ('II', '개요'),
        ('III', '현행 프로그램 반영 체계'),
        ('IV', '쟁점: 업무용 PC의 통제 사각지대'),
        ('V', '대응 방안'),
        ('VI', 'IBK AI 거버넌스 반영 방안'),
        ('VII', '결론'),
        ('부록', 'A. 도식 / B. 참고 문서·규정'),
    ]
    pdf.set_font('malgun', '', 11)
    pdf.set_text_color(40, 40, 40)
    for num, title in toc_items:
        pdf.set_x(30)
        pdf.cell(20, 8, num, align='L')
        pdf.cell(0, 8, title, ln=True)
    pdf._is_toc = False

    # ── II. 개요 ───────────────────────────────────────────────
    pdf.add_page()
    pdf.section_title('II', '개요')

    pdf.section_title('1', '배경', level=2)
    pdf.body_text(
        'AI 기반 코드 어시스턴트는 금융권을 포함한 전 산업에서 개발 생산성의 표준 도구로 '
        '자리 잡고 있다. IBK기업은행은 인터넷망과 업무망이 분리된 망분리 환경에서 '
        '운영되므로, 클로드 코드 등 외부 클라우드 기반 도구를 사내에 직접 도입할 수 없다. '
        '이에 업무망 내부에 Qwen Coder 기반 온프레미스 코드 어시스턴트 '
        '"IBK Geni-Code"를 구축하였다.'
    )

    pdf.section_title('2', '보고서 목적', level=2)
    pdf.bullet('① 현행 시스템에 프로그램이 반영되는 구조를 명확히 공유한다.')
    pdf.bullet('② Geni-Code 도입이 기존 내부통제·보안 체계에 미치는 영향을 평가한다.')
    pdf.bullet('③ 식별된 리스크에 대한 대응 방안을 건의한다.')
    pdf.ln(2)

    pdf.section_title('3', '보고서 구성', level=2)
    pdf.body_text(
        'I. Executive Summary  —  II. 개요  —  III. 현행 프로그램 반영 체계  —  '
        'IV. 쟁점: 업무용 PC의 통제 사각지대  —  V. 대응 방안  —  VI. 결론'
    )

    # ── III. 현행 프로그램 반영 체계 ───────────────────────────
    pdf.add_page()
    pdf.section_title('III', '현행 프로그램 반영 체계')

    pdf.section_title('1', 'IBK 시스템 구성', level=2)
    pdf.body_text(
        'IBK의 주요 업무 시스템은 계정계, 스마트뱅킹, 여신지원시스템 등으로 구성되며, '
        '각 시스템은 독립된 개발(Dev) – QA – 운영 3티어 환경으로 운영된다.'
    )

    pdf.section_title('2', '개발-QA-운영 3단계 프로세스', level=2)
    pdf.add_table(
        ['단계', '역할', '통제 지점'],
        [
            ['개발', '프로그램 작성 및 단위 테스트', '신규: 부장 결재 / 변경: 팀장 결재'],
            ['QA', '통합·기능 검증', '변경관리 시스템 등록'],
            ['운영', '실배포', '형상관리·배포 통제'],
        ],
        col_widths=[22, 78, 90]
    )

    pdf.section_title('3', '결재 및 변경관리 체계', level=2)
    pdf.bullet('신규 프로그램: 부장 결재 후 개발 착수')
    pdf.bullet('기존 프로그램 변경: 팀장 결재 후 개발 착수')
    pdf.bullet('변경관리 시스템: 소스코드 형상관리, 승인 이력, 배포 권한을 일원 관리')
    pdf.ln(2)

    pdf.section_title('4', '망분리 및 외부 반출 통제', level=2)
    pdf.body_text(
        'IBK는 인터넷망과 업무망이 물리적으로 분리된 망분리 환경이다. '
        '업무망 내부에서 생성된 파일이 인터넷망 또는 외부로 반출될 때에는 '
        '별도의 반출 통제 절차(결재·심사·반출 이력 관리)가 적용되어, '
        '내부 데이터의 외부 유출은 기본적으로 이 절차로 1차 차단된다.'
    )
    pdf.body_text(
        '즉, 본 보고서가 다루는 쟁점은 "외부 반출" 단계의 문제가 아니라, '
        '반출 이전 단계인 "업무PC 내부에서의 프로그램 생성·실행" 단계에 '
        '통제 사각지대가 발생한다는 점이다.'
    )

    # 제목과 도식 D1이 같은 페이지에 오도록 선제적으로 페이지 전환
    if pdf.get_y() + 10 + 88 + 10 > 270:
        pdf.add_page()
    pdf.section_title('5', '프로그램 작성·반영 흐름도', level=2)
    pdf.add_image(D1_PATH, w=180, caption='[도식 1] 현행 프로그램 작성·반영 체계')

    pdf.section_title('6', '시사점', level=2)
    pdf.body_text(
        '이 구조에서는 프로그램을 누가(사람·Geni-Code·AIDD) 작성했는지와 무관하게 '
        '동일한 결재·QA·변경관리 절차가 적용된다. '
        '따라서 본 경로를 통과한 Geni-Code 산출물은 내부통제 및 보안상 문제가 없다.'
    )

    # ── IV. 쟁점 ──────────────────────────────────────────────
    pdf.add_page()
    pdf.section_title('IV', '쟁점: 업무용 PC의 통제 사각지대')

    pdf.section_title('1', '기존 엔드포인트 보안 원칙', level=2)
    pdf.body_text(
        'IBK 업무용 PC는 허가된 프로그램만 실행 가능한 애플리케이션 화이트리스트 원칙으로 '
        '통제되어 왔다. 이는 망분리·반출 통제(III장 4절)와 함께 '
        '악성코드 실행, 비인가 도구 유입, 쉐도우IT를 차단하는 '
        '엔드포인트 보안의 핵심 장치다.'
    )

    pdf.section_title('2', 'Geni-Code 사용 전제 조건', level=2)
    pdf.body_text(
        'Geni-Code를 실제 업무에 활용하려면, 업무용 PC에서 다음 실행 환경의 허용이 필요하다.'
    )
    pdf.bullet('Python 인터프리터 실행 — 생성 코드 검증, 로컬 실행, 데이터 가공')
    pdf.bullet('웹서버·WAS 기동 — Flask, Django, FastAPI, Tomcat 등 Geni-Code로 개발한 웹 기반 도구 구동')
    pdf.bullet('필요 시 로컬 DB 엔진·스케줄러 등 추가 런타임')
    pdf.ln(1)
    pdf.body_text(
        '특히 웹서버·WAS의 기동은 업무PC의 네트워크 포트를 바인딩하여 '
        '다른 단말에서 접근 가능한 서버 역할을 수행하게 한다.'
    )

    pdf.section_title('3', '통제 사각지대 발생 메커니즘', level=2)
    pdf.body_text(
        '위 실행 환경이 업무PC에서 허용되면, 직원은 다음 절차 없이도 '
        '실행 프로그램·웹 서비스를 생성·구동할 수 있다.'
    )
    pdf.bullet('결재 미적용 — 신규/변경 결재 흐름 외부')
    pdf.bullet('QA 미적용 — 품질·기능 검증 외부')
    pdf.bullet('변경관리 미적용 — 소스·배포 이력 추적 외부')
    pdf.ln(1)
    pdf.body_text(
        '즉, 기존 시스템 반영 경로에서는 통제가 유효하나, '
        '업무PC 직접 실행 경로는 사각지대가 된다.'
    )

    pdf.section_title('4', '추가 리스크: 업무PC의 서버화', level=2)
    pdf.body_text(
        '업무용 PC는 본래 한 명의 사용자가 로그인하여 쓰는 클라이언트 전용 장비로, '
        '서버 운영을 전제로 한 통제 체계가 적용되지 않는다. '
        'Geni-Code 산출물을 구동하기 위해 웹서버·WAS가 업무PC에서 기동되면 '
        '다음과 같은 구조적 문제가 발생한다.'
    )
    pdf.bullet('서버 인증·접근통제·감사로그 체계 부재 — 업무망 내 누구나 무인증으로 접근 가능')
    pdf.bullet('공격 표면 확대 — 업무망 내부 lateral movement의 발판 제공')
    pdf.bullet('비인가 업무시스템화 — 다른 부서가 해당 웹도구에 의존하기 시작하면 통제 외 "그림자 시스템"으로 고착')
    pdf.bullet('가용성·영속성 취약 — PC 재부팅·장애·사용자 이동 시 서비스 중단 및 데이터 유실 리스크')
    pdf.bullet('엔드포인트 방화벽·IPS 정책 우회 가능성 — 허용 프로세스에 포함된 런타임이 임의 포트를 개방')

    pdf.section_title('5', '모델 자체의 리스크: Qwen Coder 사전 학습 및 학습 데이터', level=2)

    pdf.sub_heading('5-1. 사전 학습 파라미터 오염 리스크')
    pdf.body_text(
        'Geni-Code는 외부에서 공개된 Qwen Coder의 사전 학습 파라미터를 기반으로 구축된다. '
        '사전 학습 단계에서 다음과 같은 리스크가 잠재한다.'
    )
    pdf.bullet('학습 데이터에 포함된 취약 패턴·악성 샘플이 추론 시 그대로 재현')
    pdf.bullet('의도적 백도어(특정 트리거 프롬프트에 취약 코드 생성) 삽입 가능성')
    pdf.bullet('공급망 단계에서 모델 가중치 변조·서명 위조 가능성')
    pdf.ln(1)
    pdf.body_text(
        '다만 이 리스크는 "산출물이 어떤 경로로 실행되는가"에 따라 위험도가 크게 다르다. '
        '정식 경로(개발-QA-운영)로 반영된 산출물은 결재·QA·코드 리뷰에서 '
        '오염된 패턴을 식별·차단할 수 있으므로 리스크가 통상적 수준으로 억제된다. '
        '반면 업무PC 직접 실행 경로에서는 오염된 산출물이 즉시 구동되어 '
        '모델 리스크가 그대로 실체화된다. 즉, 모델 리스크는 '
        '"실행 경로"라는 증폭 기제를 만나 현실화된다.'
    )

    pdf.sub_heading('5-2. 개인정보 학습 리스크와 기술적 차단')
    pdf.body_text(
        '사용자가 프롬프트에 개인정보·고객정보를 입력할 경우, 이 데이터가 '
        '모델 학습에 포함되어 후속 응답에 유출될 리스크가 있다. '
        '기술적 차단 가능성은 운영 모드에 따라 다르다.'
    )
    pdf.add_table(
        ['운영 모드', '개인정보 학습 가능성', '기술적 차단 방안'],
        [
            ['추론 전용 (frozen)', '없음 (가중치 고정)', '기본 적용'],
            ['RAG (검색 증강)', '간접 유출 가능 (대화 로그·인덱스 축적)', '로그 암호화, PII 마스킹, 인덱스 주기 초기화'],
            ['파인튜닝·RLHF', '직접 유출 가능 (추가 학습 발생)', '해당 기능 비활성화 필수'],
        ],
        col_widths=[42, 60, 88]
    )
    pdf.body_text(
        '결론적으로, 모델을 추론 전용(frozen)으로 고정하고 로그·RAG 인덱스에 '
        'PII가 저장되지 않도록 입력 필터링과 마스킹을 적용하면 기술적 차단이 가능하다. '
        '단, 이는 Geni-Code 운영 측의 내부 정책이므로 사용자 측에서는 결과를 '
        '직접 검증하기 어렵다. 따라서 모델 운영자와의 서비스 수준 합의(SLA) '
        '또는 내부 통제 기준에 "추론 전용·PII 비학습"을 명시적으로 규정해야 한다.'
    )

    # 제목과 도식 D2가 같은 페이지에 오도록 선제적으로 페이지 전환
    if pdf.get_y() + 10 + 88 + 10 > 270:
        pdf.add_page()
    pdf.section_title('6', '쟁점 시각화', level=2)
    pdf.add_image(D2_PATH, w=180, caption='[도식 2] Before / After — 통제 사각지대 비교')

    pdf.section_title('7', '대표 위협 시나리오', level=2)
    pdf.callout_box(
        'T1. 비인가 데이터 가공·생성 스크립트',
        'Geni-Code에게 "엑셀 고객 리스트에서 이메일만 뽑아 CSV로 저장"을 요청하고 '
        '생성 코드를 업무PC에서 실행. 외부 반출 자체는 망분리·반출 통제 절차로 '
        '1차 차단되나, DLP·변경관리를 거치지 않은 경로로 민감정보 파일이 '
        '업무PC에 상주·활용되는 것 자체가 내부통제·감사 대응상 문제다.',
        accent=C_RED, body_lines=3
    )
    pdf.callout_box(
        'T2. 쉐도우 자동화 (Shadow IT)',
        '반복 업무 자동화 스크립트를 직원이 임의로 스케줄러에 등록해 상시 구동. '
        '통제 외 자동화가 정식 시스템과 병존하여 장애 원인 추적이 불가하고 감사 대응에 취약.',
        accent=C_RED, body_lines=2
    )
    pdf.callout_box(
        'T3. 외부 패키지 유입 경로의 취약성',
        'Geni-Code가 제안한 파이썬 패키지명이 타이포스쿼팅 또는 트로이화된 변종일 경우, '
        '내부 미러 경유로 유입된 악성 코드가 업무PC에 상주할 수 있다. '
        '실제 PyPI에서 유사 사례가 다수 보고되어 있는 실존 위협이다.',
        accent=C_RED, body_lines=3
    )
    pdf.callout_box(
        'T4. 앱 화이트리스트 무력화',
        'Python 인터프리터 실행이 한 번 허용되면 스크립트를 로더로 삼아 '
        '임의 코드 실행이 가능하며, 이는 기존 엔드포인트 보안 정책의 '
        '실질적 우회 경로를 형성한다.',
        accent=C_RED, body_lines=2
    )
    pdf.callout_box(
        'T5. 업무PC 서버화 및 비인가 내부 서비스 확산',
        'Geni-Code로 개발한 웹도구를 Flask·Django·Tomcat 등으로 업무PC에서 기동하고, '
        '동료들이 브라우저로 접속해 사용. 인증·감사·접근통제·가용성이 보장되지 않은 '
        '비인가 내부 웹서비스가 업무에 고착화되어, 개인정보·기밀 데이터가 '
        '무인증으로 업무망 내 수평 확산되고 감사·책임 추적이 불가해진다.',
        accent=C_RED, body_lines=4
    )
    pdf.callout_box(
        'T6. 오염된 모델 산출물의 업무PC 직접 실행',
        '공개 사전학습된 Qwen Coder에 잠재된 백도어 트리거 또는 취약 패턴이 '
        'Geni-Code 산출물에 포함될 경우, 정식 경로라면 QA·코드 리뷰에서 차단되나 '
        '업무PC 직접 실행 경로에서는 그대로 구동된다. 모델 리스크가 실행 경로를 '
        '통해 증폭·현실화되는 구조적 취약점이다.',
        accent=C_RED, body_lines=3
    )
    pdf.callout_box(
        'T7. 프롬프트 경유 개인정보 간접 유출',
        '직원이 테스트 편의상 실제 고객 데이터를 Geni-Code 프롬프트에 입력하면, '
        '운영 측 로그·RAG 인덱스에 개인정보가 축적되어 감사·규제 대응상 문제를 일으킨다. '
        '모델 자체가 학습하지 않더라도 프롬프트 이력이 평문 저장되면 실질 유출과 동일하다.',
        accent=C_RED, body_lines=3
    )

    # ── V. 대응 방안 ──────────────────────────────────────────
    pdf.add_page()
    pdf.section_title('V', '대응 방안')

    pdf.section_title('1', '기본 원칙', level=2)
    pdf.body_text(
        'AI 코딩 어시스턴트 활용은 금융권 생산성 확보에 불가피하다. '
        '다만 보안은 타협 대상이 아니다. '
        '기술적 통제만으로 부족한 영역은 행위적·관리적 통제로 보완한다.'
    )

    pdf.section_title('2', '1순위 — 행위적 통제: 보안 서약서 도입 (즉시 시행 권고)', level=2)
    pdf.body_text(
        '대상: Geni-Code 사용을 위해 업무PC Python 실행 권한을 부여받는 전 직원'
    )
    pdf.body_text('서약 주요 항목:')
    pdf.bullet('개인정보·고객정보 등 민감정보를 Geni-Code 프롬프트에 입력하지 않을 것')
    pdf.bullet('Geni-Code 산출물을 정식 개발-QA-운영 절차 외의 업무PC 실행용으로 전용하지 않을 것')
    pdf.bullet('허용된 라이브러리 외 설치·사용 금지')
    pdf.bullet('위반 시 인사·징계 책임 수용')
    pdf.ln(1)
    pdf.body_text(
        '기존 정보보호 서약서와 별도 또는 보강 조항 형태로 추진할 수 있다.'
    )

    pdf.section_title('3', '2순위 — 기술적 통제 보완', level=2)
    pdf.bullet('실행 환경 제한: Python을 가상환경(venv) 또는 격리 런타임 내에서만 실행')
    pdf.bullet('실행 로그 감사: 스크립트 실행 이력, 접근 파일, 네트워크 호출을 EDR/DLP 로그로 수집')
    pdf.bullet('스케줄러 자동 실행 차단: Task Scheduler 등을 통한 상시 구동 제한')
    pdf.bullet('네트워크 포트 바인딩 제한: 업무PC의 0.0.0.0/외부 인터페이스 바인딩 차단, '
               '개발 검증용은 localhost(127.0.0.1)만 허용')
    pdf.bullet('웹서버·WAS 기동 통제: 허가된 개발 샌드박스 외 업무PC에서 장기 구동 금지 및 가동 로그 수집')
    pdf.ln(1)

    pdf.section_title('4', '3순위 — 관리적 통제 보완', level=2)
    pdf.bullet('허용 라이브러리 화이트리스트: 내부 PyPI 미러에 검증된 패키지만 배포, 해시 검증 의무화')
    pdf.bullet('모델 무결성 검증: Qwen Coder 가중치 체크섬·서명 검증, 주기적 재검증')
    pdf.bullet('추론 전용·PII 비학습 정책 명시: 파인튜닝/RLHF 비활성화, 프롬프트 입력 PII 필터·마스킹')
    pdf.bullet('사용자 교육 및 인증제: Geni-Code 사용 자격을 이수 교육과 연동')
    pdf.bullet('주기 점검: 분기별 사용 현황·위반 사례 점검 및 경영진 보고')

    # ── VI. AI 거버넌스 반영 방안 ────────────────────────────
    pdf.add_page()
    pdf.section_title('VI', 'IBK AI 거버넌스 반영 방안')

    pdf.section_title('1', '현재 통제 체제의 공백', level=2)
    pdf.body_text(
        'IBK는 시스템 반영 단계의 내부통제(결재·QA·변경관리)와 엔드포인트 보안'
        '(앱 화이트리스트·DLP·망분리·반출 통제)은 성숙하게 운영되고 있다. '
        '그러나 Geni-Code와 같은 AI 도구가 업무PC에서 직접 산출물을 실행하는 '
        '사용 패턴에 대한 거버넌스 프레임워크는 부재하다.'
    )
    pdf.body_text(
        '즉, "AI가 만든 코드를 누가, 어떤 경로로, 어떤 책임 하에 실행할 수 있는가"에 '
        '대한 규정이 없어, 현재는 개별 사용자 판단에 의존하는 공백 상태다.'
    )

    pdf.section_title('2', 'IBK AI 거버넌스 4대 축', level=2)

    pdf.sub_heading('축 1. Geni-Code 산출물 분류 체계')
    pdf.add_table(
        ['등급', '정의', '적용 통제'],
        [
            ['Class A', '정식 시스템에 반영되는 산출물', '기존 개발-QA-운영 통제 (추가 조치 불요)'],
            ['Class B', '업무PC에서 실행하는 일회성·반복 스크립트', '사용 등록·실행 로그·기한 만료 의무'],
            ['Class C', '학습·참고 목적, 실행하지 않음', '최소 통제 (프롬프트 PII 점검만)'],
        ],
        col_widths=[22, 78, 90]
    )

    pdf.sub_heading('축 2. 생애주기 단계별 통제 지점')
    pdf.bullet('프롬프트 입력 — PII 필터, 민감정보 경고 팝업')
    pdf.bullet('모델 추론 — 모델 무결성·SLA 점검, 이상 응답 차단')
    pdf.bullet('산출물 검토 — 사용자 1차 리뷰 + Class B 이상은 부서장 확인')
    pdf.bullet('실행 환경 선택 — A(정식)/B(업무PC)/C(미실행) 분류 선언')
    pdf.bullet('실행 — 로그·네트워크 호출·파일 접근 EDR/DLP 수집')
    pdf.bullet('로그·폐기 — 보존 기간 명시, 이직·부서이동 시 이관 절차')

    pdf.sub_heading('축 3. 책임 소재 명확화')
    pdf.bullet('사용자 — 프롬프트 적정성, 산출물 용도·분류 선언, 서약 준수')
    pdf.bullet('부서장 — 부서 내 Geni-Code 사용 승인·감독, Class B 확인')
    pdf.bullet('모델 운영자(정보보호부·디지털혁신부) — 모델 무결성, PII 차단 SLA, 로그 관리')
    pdf.bullet('감사·준법 — 주기 점검 및 위반 시 조치, 거버넌스 실효성 평가')

    pdf.sub_heading('축 4. 리스크 등급별 허용 범위')
    pdf.add_table(
        ['리스크 등급', '조건', '허용 범위'],
        [
            ['저', '민감정보 미포함 & 일회성 실행', '간단 신고 후 실행'],
            ['중', '민감정보 포함 또는 상시 구동 의도', '결재·등록·로그 감사 의무'],
            ['고', '대고객·원장·계정계 접근 로직 포함', '정식 개발-QA-운영 경로만 허용, 업무PC 실행 금지'],
        ],
        col_widths=[28, 82, 80]
    )

    pdf.section_title('3', '단계별 도입 로드맵', level=2)
    pdf.add_table(
        ['단계', '시기', '주요 과제'],
        [
            ['1단계', '즉시', '보안 서약서 + 산출물 분류 체계 공표'],
            ['2단계', '3개월 내', '사용 등록제·EDR/DLP 로그 감사 체계 구축'],
            ['3단계', '6개월 내', '실행 환경 격리·모델 SLA·Class B 정기 감사 확립'],
            ['4단계', '연 1회', '거버넌스 전반 재검토 및 개선'],
        ],
        col_widths=[22, 28, 140]
    )
    pdf.ln(1)
    pdf.body_text(
        '본 로드맵은 V장의 "대응 방안 우선순위"와 정합하며, '
        '거버넌스는 단발성 대책이 아니라 지속 운영되는 프레임워크임을 전제로 한다.'
    )

    # ── VI. 결론 ──────────────────────────────────────────────
    pdf.add_page()
    pdf.section_title('VII', '결론')

    pdf.body_text(
        'Geni-Code의 산출물 자체는 기존 통제 체계로 안전하게 관리된다. '
        '핵심 쟁점은 사용 전제 조건인 업무용 PC의 Python·웹서버·WAS 실행 허용이 만드는 '
        '통제 사각지대이며, 추가로 공개 사전학습 모델의 잠재 리스크와 '
        '프롬프트 경유 개인정보 유출 가능성까지 고려해야 한다. '
        '이는 기술적 통제만으로 해결되지 않는다.'
    )
    pdf.body_text(
        '따라서 다음의 4단계 대응을 건의한다.'
    )
    pdf.bullet('① 보안 서약서 즉시 도입 (1순위)')
    pdf.bullet('② 실행환경 제한 및 로그 감사 — Python·웹서버·WAS 포함 (2순위)')
    pdf.bullet('③ 라이브러리 화이트리스트·모델 무결성·PII 차단·교육·점검 (3순위)')
    pdf.bullet('④ IBK AI 거버넌스 프레임워크 수립 — 본 보고서 VI장 4대 축 적용 (4순위)')
    pdf.ln(2)

    pdf.callout_box(
        '최종 건의',
        'AI 활용과 금융보안은 양립 가능하다. 전제는 "통제 경로를 신설하지 않는 허용"이 아닌, '
        '"통제 경로를 포함한 허용"이다. '
        '이에 1순위 과제인 보안 서약서 도입을 우선 승인해 주시고, '
        '병행하여 VI장 AI 거버넌스 프레임워크 수립을 착수해 주시기 바랍니다.',
        accent=C_GOLD, body_lines=4
    )

    # ── 부록 ──────────────────────────────────────────────────
    pdf.add_page()
    pdf.section_title('부록', '참고 자료')

    pdf.section_title('A', '도식 파일 목록', level=2)
    pdf.bullet('geni-code_d1_current_flow.png — 현행 프로그램 작성·반영 흐름도')
    pdf.bullet('geni-code_d2_gap.png — 통제 Before/After 비교도')
    pdf.ln(2)

    pdf.section_title('B', '참고 문서 · 규정', level=2)
    pdf.bullet('전자금융감독규정 제13조(내부통제기준), 제15조(정보처리시스템 보호)')
    pdf.bullet('금융보안원 「금융권 AI 활용 보안 가이드」')
    pdf.bullet('NIST SP 800-218 (SSDF) — AI 도구 사용 시 검증 의무')

    # ── Save ──────────────────────────────────────────────────
    pdf.output(OUTPUT_PDF)
    return OUTPUT_PDF


if __name__ == '__main__':
    out = build_report()
    print(f'Generated: {out}')
    print(f'Size: {os.path.getsize(out):,} bytes')
