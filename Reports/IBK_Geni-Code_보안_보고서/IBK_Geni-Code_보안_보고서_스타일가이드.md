# IBK Geni-Code 보안 보고서 — 스타일 가이드

> 참조 양식: `영일피혁_경영보고서_2026.pdf`
> 원본 생성기: `C:/SIY_DEV/영일피혁/generate_report.py` (fpdf2 + matplotlib, Python)
> 본 가이드는 해당 원본의 레이아웃·색상·타이포그래피를 IBK Geni-Code 보고서에 이식하기 위한 기준.

---

## 1. 페이지 기본 설정

| 항목 | 값 |
|------|-----|
| 용지 | A4 세로 (210 × 297 mm) |
| 본문 좌우 여백 | 10 mm (본문 유효폭 190 mm) |
| 자동 페이지 나눔 하단 여백 | 20 mm |
| 기본 폰트 | Malgun Gothic (`malgun.ttf` / `malgunbd.ttf`) |
| 본문 줄 간격 | 5.5 mm |

---

## 2. 컬러 팔레트

| 역할 | 이름 | RGB | HEX |
|------|------|-----|-----|
| Primary | Navy | 0, 32, 63 | `#002040` |
| Secondary | Blue | 0, 82, 136 | `#005288` |
| Accent | Cyan | 0, 145, 200 | `#0091C8` |
| Divider/Strong Accent | Gold | 180, 150, 50 | `#B49632` |
| Warning | Red | 200, 50, 50 | `#C83232` |
| Meta/Caption | Gray | 100, 100, 100 | `#646464` |
| Table Stripe | Light Gray | 245, 247, 250 | `#F5F7FA` |
| Surface | White | 255, 255, 255 | `#FFFFFF` |

---

## 3. 타이포그래피 (Pt 기준)

| 요소 | 폰트 | 크기 | 색상 | 비고 |
|------|------|------|------|------|
| 표지 메인 타이틀 | Malgun Bold | 28 | White | 네이비 배경 |
| 표지 서브 타이틀 | Malgun Bold | 22 | White | |
| 표지 날짜 | Malgun Reg | 14 | 연회색(200,200,220) | |
| 목차 헤더 "목 차" | Malgun Bold | 20 | Navy | 중앙 정렬 |
| 섹션 제목 L1 (I., II., …) | Malgun Bold | 16 | Navy | 좌측 3mm 네이비 막대 |
| 섹션 제목 L2 (3.1, 3.2) | Malgun Bold | 12 | Blue | |
| 소제목 | Malgun Bold | 10 | Navy | |
| 본문 | Malgun Reg | 9 | (40,40,40) | |
| 불릿 리스트 | Malgun Reg | 9 | (40,40,40) | `•` 마커 사용 |
| 표 헤더 | Malgun Bold | 8 | White / Navy 배경 | |
| 표 본문 | Malgun Reg | 8 | (40,40,40) | |
| 캡션 | Malgun Reg | 7 | Gray | 중앙 정렬 |
| 헤더·푸터 | Malgun Reg | 7 | Gray | |

---

## 4. 구성 요소 스타일

### 4.1 헤더 / 푸터
- **헤더**(표지·목차 제외): 우측 `"IBK Geni-Code 보안관련 보고서 | Confidential"` + 하단 Navy 가로선(0.3mm)
- **푸터**: 하단 라이트그레이 가로선 + 좌측 `"© 2026 Confidential"` + 우측 페이지 번호

### 4.2 표지 (Cover)
- 상단 0–160mm 영역을 **Navy 풀블리드 사각형**으로 채움
- 제목(흰색, 28pt) → 서브타이틀(흰색, 22pt) → **Gold 가로선(60~150mm, 0.8mm 굵기)** → 발행월(연회색)
- 하단(175mm~): `CONFIDENTIAL` 표기 + 문서 취급 주의 문구 + 데이터 기준·작성자
- 표지에는 헤더·푸터 없음

### 4.3 목차 (TOC)
- 중앙 정렬 "목 차" (Navy, 20pt Bold)
- 항목: 로마숫자 장번호 + 제목 + 점선 리더 + 페이지 번호
- 목차 페이지에는 헤더 없음(푸터는 있음)

### 4.4 섹션 제목
- **L1**: 좌측 3mm × 10mm Navy 수직 막대 + 텍스트 시작 위치 x=17mm + `{로마숫자}. {제목}` 형태
- **L2**: 들여쓰기 없이 `{숫자} {제목}` (예: `3.1 현행 반영 체계`)

### 4.5 Key Finding 박스 (Executive Summary용)
- 번호 셀(8×8mm, Navy 배경, 흰 글자, Bold 11pt)
- 옆에 본문(9pt), x=22mm부터 배치
- 여러 개 나열 시 박스 사이 2mm 간격

### 4.6 표 (Table)
- 헤더: Navy 배경 + 흰색 Bold 8pt + 좌측 정렬(첫 열)/우측 정렬(나머지)
- 본문: Reg 8pt, **짝수 행은 `#F5F7FA` 스트라이프 배경**
- 행 높이 6.5mm, 헤더 7mm
- 컬럼 너비는 합계 190mm 기준 배분
- **페이지 나눔 규칙**: `남은 공간 < 8 + 행수×6.5 + 5`이면 새 페이지 시작

### 4.7 콜아웃 박스 (Callout / 주의사항)
- 좌측 3mm 색상 수직 바(상황별 Navy/Red/Gold)
- 본체 187mm 폭, 연한 배경(예: `#F0F8FF`)
- 제목(9pt Bold Navy) + 본문(8pt)
- 높이 20mm 기준, 남은 공간 < 25mm면 새 페이지

### 4.8 도식 / 차트
- 중앙 정렬, 기본 폭 170mm, 해상도 200dpi PNG
- 하단 캡션(7pt Gray, 중앙 정렬)
- **남은 공간 < 90mm이면 새 페이지**로 이동

---

## 5. 페이지 나눔(Page Break) 품질 규칙

| 요소 | 규칙 |
|------|------|
| 섹션 제목 | 제목 뒤에 본문 최소 2~3줄이 같은 페이지에 오도록 (제목 고아 방지) |
| 문단 | 중간 잘림 금지, 필요 시 다음 페이지로 이월 |
| 표 | **단일 페이지 완결**이 원칙. 불가피하게 길 경우 헤더 반복 |
| 도식/콜아웃 박스 | 단일 페이지 완결 (분할 금지) |
| 불릿 리스트 | 가능한 한 묶음 유지. 분할 시 최소 2개 이상 같은 페이지 유지 |
| 장 시작 | 각 장(I~)은 새 페이지에서 시작 |

**fpdf2 구현 패턴** (generate_report.py와 동일):
```python
# 표 삽입 전
needed = 8 + len(rows) * 6.5 + 5
if pdf.get_y() + needed > 270:
    pdf.add_page()

# 차트 삽입 전
if pdf.get_y() + 90 > 270:
    pdf.add_page()
```

---

## 6. IBK Geni-Code 보고서 적용 매핑

| 영일피혁 원본 요소 | IBK Geni-Code 보고서 반영 |
|---------------------|------------------------|
| 표지 메인 타이틀 "영일피혁 그룹" | "IBK 기업은행" |
| 표지 서브타이틀 "현황 분석 및 경영전략 보고서" | "Geni-Code 도입 관련 보안 검토 보고서" |
| 발행월 "2026년 3월" | "2026년 4월" |
| 헤더 문자열 | "IBK Geni-Code 보안관련 보고서 | Confidential" |
| 데이터 기준 | "원본: IBK Geni-Code 보안관련 유의사항" |
| 작성 주체 | 사내 담당부서명(확인 필요) |
| Executive Summary → Key Findings 3개 | ① 산출물은 기존 통제로 안전 ② 업무PC Python 허용이 사각지대 ③ 보안 서약 등 행위적 통제 필요 |
| KPI 표 | — (해당 없음, 제외) |
| 전략 권고 표 | "대응 방안 우선순위" 표로 대체 (1~3순위) |
| 장 구조 I~X | I. Executive Summary / II. 개요 / III. 현행 반영 체계 / IV. 쟁점 / V. 대응 방안 / VI. 결론 |

---

## 7. 산출 방법 (권장)

- **채택 방식**: 영일피혁 원본과 동일한 **fpdf2 기반 Python 스크립트**를 신규 작성
  - 이유: 픽셀 단위 레이아웃·페이지 나눔 제어가 확실함. Markdown → PDF 변환으로는 동일 수준 재현이 어려움
- 스크립트 베이스: `C:/SIY_DEV/영일피혁/generate_report.py`를 복제하여 `generate_geni-code_report.py` 생성
- 유지: `ReportPDF` 클래스, 색상 상수, 헬퍼 메서드(`section_title`, `body_text`, `bullet`, `key_finding`, `add_table`, `callout_box`)
- 교체: `build_report()` 내부의 콘텐츠(텍스트·표·권고사항)만 Geni-Code 보고서 내용으로 치환
- 제거: 재무 차트(수익/부채/출하) 관련 chart_* 함수는 이번 보고서에 불필요
- 추가(필요 시): "프로그램 작성·반영 체계 흐름도" 이미지(별도 Mermaid/다이어그램 툴로 PNG 생성 후 `pdf.image()` 삽입)
