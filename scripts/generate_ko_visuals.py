from __future__ import annotations

import os
import textwrap
from pathlib import Path

from PIL import Image, ImageDraw, ImageFont


ROOT = Path(__file__).resolve().parents[1]
DOCS = ROOT / "docs"
KO_DOCS = DOCS / "ko"

FONT_PATH = "/System/Library/Fonts/AppleSDGothicNeo.ttc"
TITLE_FONT_SIZE = 36
HEADER_FONT_SIZE = 24
BODY_FONT_SIZE = 22
PADDING = 28
LINE_GAP = 10
PANEL_BG = "#F8FAFC"
HEADER_COLOR = "#475569"
TITLE_COLOR = "#0F172A"
BODY_COLOR = "#1E293B"
ACCENT = "#2563EB"


VISUAL_TEXT = {
    "images/es/bigpicture/close-ended-holding-process.png": {
        "title": "종료 시점이 있는 책 Hold 흐름",
        "lines": [
            "Regular patron 이 종료 시점이 있는 hold 를 생성한다.",
            "hold 이후 최대 보유 수 도달, 취소, checkout, 만료까지 이어지는 큰 흐름을 보여준다.",
            "하루가 시작되면 daily sheet 를 확인해 오래된 hold 를 만료시킨다.",
        ],
    },
    "images/es/bigpicture/definitions-1.png": {
        "title": "Holding 관련 핵심 정의",
        "lines": [
            "close-ended hold 와 open-ended hold 를 구분하기 위한 용어 정리 보드다.",
            "이벤트와 상태를 같은 말로 오해하지 않도록 초기에 언어를 맞추는 목적을 가진다.",
        ],
    },
    "images/es/bigpicture/open-ended-holding-process.png": {
        "title": "종료 시점이 없는 책 Hold 흐름",
        "lines": [
            "Researcher patron 이 open-ended hold 를 생성하는 흐름이다.",
            "취소와 checkout 은 가능하지만, hold expired 이벤트는 존재하지 않는다.",
        ],
    },
    "images/es/bigpicture/the-book-returning-process.png": {
        "title": "책 반납 흐름",
        "lines": [
            "어떤 patron 이든 책을 반납할 수 있다.",
            "반납 시 overdue 해제, 요금 부과 시작, 일일 overdue 점검과 연결되는 흐름을 나타낸다.",
        ],
    },
    "images/es/bigpicture/definitions-2.png": {
        "title": "Checkout 관련 정의",
        "lines": [
            "checkout, overdue checkout, return 같은 개념의 의미를 맞추기 위한 정의 보드다.",
        ],
    },
    "images/es/bigpicture/book-catalogue.png": {
        "title": "Catalogue 흐름",
        "lines": [
            "도서관 직원이 책과 책 인스턴스를 catalogue 에 추가하는 과정을 설명한다.",
            "일부 제거 시나리오는 hot spot 으로 남겨 두고 이후 논의 대상으로 미룬다.",
        ],
    },
    "images/es/bigpicture/book-catalogue-definitions.png": {
        "title": "Catalogue 용어 정의",
        "lines": [
            "catalogue 맥락의 book 과 lending 맥락의 book 이 다르다는 점을 드러내는 정의 보드다.",
        ],
    },
    "images/em/holding.png": {
        "title": "Example Mapping: Holding",
        "lines": [
            "holding 영역에서 다뤄야 할 대표 사례들을 모은 예시 맵이다.",
        ],
    },
    "images/em/checking-out.png": {
        "title": "Example Mapping: Checkout",
        "lines": [
            "checkout 관련 대표 사례들을 정리한 예시 맵이다.",
        ],
    },
    "images/em/expiring-hold.png": {
        "title": "Example Mapping: Hold 만료",
        "lines": [
            "hold 만료와 관련된 예시를 모은 맵이다.",
        ],
    },
    "images/em/canceling-hold.png": {
        "title": "Example Mapping: Hold 취소",
        "lines": [
            "hold 취소와 관련된 예시를 모은 맵이다.",
        ],
    },
    "images/em/overdue-checkouts.png": {
        "title": "Example Mapping: Overdue Checkout",
        "lines": [
            "기한 초과 대출과 관련된 예시를 모은 맵이다.",
        ],
    },
    "images/em/adding-to-catalogue.png": {
        "title": "Example Mapping: Catalogue 추가",
        "lines": [
            "catalogue 에 책과 인스턴스를 추가하는 예시를 모은 맵이다.",
        ],
    },
    "images/dl/holding/example-1.png": {
        "title": "정규 patron 이 6번째 hold 를 시도하는 예시",
        "lines": [
            "이미 5개의 hold 를 가진 regular patron 이 추가 hold 를 시도한다.",
            "최대 hold 수 규칙 때문에 실패하는 흐름이다.",
        ],
    },
    "images/dl/holding/example-2.png": {
        "title": "이용 불가능한 책에 대한 hold 시도",
        "lines": [
            "available 하지 않은 책은 hold 할 수 없다.",
        ],
    },
    "images/dl/holding/example-3.png": {
        "title": "Overdue checkout 초과 상태에서의 hold 시도",
        "lines": [
            "해당 branch 에 overdue checkout 이 너무 많으면 hold 는 거절된다.",
        ],
    },
    "images/dl/holding/example-4.png": {
        "title": "정규 patron 과 restricted 책",
        "lines": [
            "regular patron 은 restricted book 을 hold 할 수 없다.",
        ],
    },
    "images/dl/holding/example-5.png": {
        "title": "정규 patron 의 정상적인 hold 성공",
        "lines": [
            "자격 조건을 모두 만족하면 close-ended hold 를 생성할 수 있다.",
        ],
    },
    "images/dl/holding/example-6.png": {
        "title": "정규 patron 의 추가 성공 시나리오",
        "lines": [
            "앞선 규칙을 만족하는 경우 hold 성공 흐름을 보완한다.",
        ],
    },
    "images/dl/holding/example-7.png": {
        "title": "연구자 patron 도 overdue 초과 시 거절",
        "lines": [
            "researcher patron 도 overdue checkout 이 많으면 hold 가 거절된다.",
        ],
    },
    "images/dl/holding/example-8.png": {
        "title": "연구자 patron 과 이용 불가능한 책",
        "lines": [
            "researcher patron 역시 available 하지 않은 책은 hold 할 수 없다.",
        ],
    },
    "images/dl/holding/example-9.png": {
        "title": "연구자 patron 과 restricted 책",
        "lines": [
            "researcher patron 은 restricted book 을 hold 할 수 있다.",
        ],
    },
    "images/dl/holding/example-10.png": {
        "title": "연구자 patron 의 hold 성공 예시 1",
        "lines": [
            "researcher patron 이 규칙을 만족하며 hold 를 생성하는 성공 시나리오다.",
        ],
    },
    "images/dl/holding/example-11.png": {
        "title": "연구자 patron 의 hold 성공 예시 2",
        "lines": [
            "연구자에게 허용된 hold 시나리오를 추가로 보여준다.",
        ],
    },
    "images/dl/holding/example-12.png": {
        "title": "정규 patron 과 open-ended hold",
        "lines": [
            "regular patron 은 종료 시점이 없는 hold 를 생성할 수 없다.",
        ],
    },
    "images/dl/holding/example-13.png": {
        "title": "연구자 patron 의 open-ended hold",
        "lines": [
            "researcher patron 은 open-ended hold 를 생성할 수 있다.",
        ],
    },
    "images/dl/cancelinghold/example-1.png": {
        "title": "존재하지 않는 hold 취소",
        "lines": [
            "hold 가 존재하지 않으면 취소는 실패해야 한다.",
        ],
    },
    "images/dl/cancelinghold/example-2.png": {
        "title": "정상적인 hold 취소",
        "lines": [
            "존재하는 hold 는 정상적으로 취소할 수 있다.",
        ],
    },
    "images/dl/cancelinghold/example-3.png": {
        "title": "다른 사람이 건 hold 취소 시도",
        "lines": [
            "자신이 걸지 않은 hold 는 취소할 수 없다.",
        ],
    },
    "images/dl/cancelinghold/example-4.png": {
        "title": "hold 취소 후 새 hold 가능",
        "lines": [
            "최대 hold 수에 도달했던 patron 이 하나를 취소하면 다시 hold 할 수 있다.",
        ],
    },
    "images/dl/cancelinghold/example-5.png": {
        "title": "중복 취소 금지",
        "lines": [
            "같은 hold 를 두 번 취소할 수는 없다.",
        ],
    },
    "images/dl/bookcheckouts/example-1.png": {
        "title": "hold 가 있어야 checkout 가능",
        "lines": [
            "책 checkout 은 hold 존재를 전제로 한다.",
        ],
    },
    "images/dl/bookcheckouts/example-2.png": {
        "title": "타인의 hold 는 checkout 불가",
        "lines": [
            "다른 patron 이 hold 한 책은 checkout 할 수 없다.",
        ],
    },
    "images/dl/bookcheckouts/example-3.png": {
        "title": "정상적인 checkout 흐름",
        "lines": [
            "hold 된 책이 checkout 되며 hold 가 완료 상태로 전이된다.",
        ],
    },
    "images/dl/bookcheckouts/example-4.png": {
        "title": "hold 취소 후 checkout 시도",
        "lines": [
            "이미 취소된 hold 로는 checkout 할 수 없다.",
        ],
    },
    "images/dl/bookcheckouts/example-5.png": {
        "title": "hold 는 있지만 실제 책이 없는 경우",
        "lines": [
            "도메인 모델의 book 과 현실의 책 사이에 차이가 있을 수 있음을 드러내는 예시다.",
        ],
    },
    "images/dl/expiringhold/example-1.png": {
        "title": "만료 대상 hold 찾기",
        "lines": [
            "daily sheet 를 조회해 만료되어야 할 close-ended hold 를 찾는다.",
        ],
    },
    "images/dl/expiringhold/example-2.png": {
        "title": "취소된 hold 는 만료 대상 아님",
        "lines": [
            "만료 전에 취소된 hold 는 expired 로 등록되면 안 된다.",
        ],
    },
    "images/dl/expiringhold/example-3.png": {
        "title": "hold 는 한 번만 만료",
        "lines": [
            "같은 hold 를 중복으로 expired 처리하면 안 된다.",
        ],
    },
    "images/dl/overduecheckouts/example-1.png": {
        "title": "overdue checkout 등록",
        "lines": [
            "daily sheet 를 통해 기한을 넘긴 checkout 을 매일 식별한다.",
        ],
    },
    "images/dl/overduecheckouts/example-2.png": {
        "title": "반납된 책은 overdue 로 등록하지 않음",
        "lines": [
            "이미 returned 상태인 책은 overdue checkout 으로 등록되지 않아야 한다.",
        ],
    },
    "images/dl/addingtocatalogue/example-1.png": {
        "title": "등록된 ISBN 에 인스턴스 추가",
        "lines": [
            "같은 ISBN 의 책이 catalogue 에 존재하면 인스턴스를 추가할 수 있다.",
        ],
    },
    "images/dl/addingtocatalogue/example-2.png": {
        "title": "등록되지 않은 ISBN 에 인스턴스 추가 실패",
        "lines": [
            "먼저 책이 등록되어 있지 않으면 book instance 추가는 실패한다.",
        ],
    },
    "images/aggregates/agg-1.png": {
        "title": "Aggregate 후보 1: Book 중심",
        "lines": [
            "Book 을 중심 aggregate 로 볼 수 있는 첫 번째 시도다.",
        ],
    },
    "images/aggregates/agg-2.png": {
        "title": "Aggregate 후보 2: Patron 이 Book 을 받는 구조",
        "lines": [
            "Patron 이 더 많은 invariant 를 보호하므로 Book 을 입력으로 받는 방향을 검토한다.",
        ],
    },
    "images/aggregates/agg-3.png": {
        "title": "최종 Aggregate 모델",
        "lines": [
            "Patron 을 먼저 수정하고, Book 은 이후 이벤트로 정합성을 맞추는 최종 모델이다.",
        ],
    },
    "images/architecture-big-picture.png": {
        "title": "아키텍처 큰 그림",
        "lines": [
            "bounded context 와 읽기/쓰기 모델의 큰 구조를 설명하는 다이어그램이다.",
        ],
    },
    "images/eventstorming-big-picture.jpg": {
        "title": "Big Picture EventStorming 워크숍 사진",
        "lines": [
            "도메인 전반의 흐름과 사건을 벽면에 정리한 실제 워크숍 보드다.",
        ],
    },
    "images/eventstorming-definitions.png": {
        "title": "핵심 용어 정의 보드",
        "lines": [
            "ubiquitous language 를 맞추기 위해 사용한 정의 정리 자료다.",
        ],
    },
    "images/eventstorming-design-level.jpg": {
        "title": "Design Level EventStorming 워크숍 사진",
        "lines": [
            "개별 시나리오와 규칙을 더 세밀하게 파고든 설계 수준 보드다.",
        ],
    },
    "images/eventstorming-domain-desc.png": {
        "title": "도메인 설명 원본 보드",
        "lines": [
            "문제 공간을 처음 공유하기 위해 사용한 도메인 설명 자료다.",
        ],
    },
    "images/example-mapping.png": {
        "title": "Example Mapping 보드",
        "lines": [
            "비즈니스 예시를 영역별로 묶고 우선순위를 잡는 중간 단계 보드다.",
        ],
    },
    "images/placing-on-hold-policy-max.png": {
        "title": "정책 다이어그램: 최대 Hold 수",
        "lines": [
            "regular patron 의 최대 hold 수 제한 규칙을 설명한다.",
        ],
    },
    "images/placing-on-hold-policy-open-ended.png": {
        "title": "정책 다이어그램: Open-ended Hold",
        "lines": [
            "open-ended hold 가 researcher patron 에게만 허용되는 규칙을 설명한다.",
        ],
    },
    "images/placing-on-hold-policy-overdue.png": {
        "title": "정책 다이어그램: Overdue Checkout",
        "lines": [
            "overdue checkout 수가 hold 자격에 영향을 주는 규칙을 설명한다.",
        ],
    },
    "images/placing-on-hold-policy-restricted.png": {
        "title": "정책 다이어그램: Restricted Book",
        "lines": [
            "restricted book hold 자격이 patron 유형에 따라 달라지는 규칙을 설명한다.",
        ],
    },
    "images/placing_on_hold.jpg": {
        "title": "Placing on Hold 워크숍 사진",
        "lines": [
            "hold 생성 유스케이스를 세밀하게 분석한 실제 워크숍 사진이다.",
        ],
    },
    "c4/component-diagram.png": {
        "title": "C4 컴포넌트 다이어그램",
        "lines": [
            "Regular/Researcher Patron 과 Librarian 이 시스템을 어떻게 사용하는지 보여준다.",
            "Patron Profile, Daily Sheet, Patron, Book, Catalogue 가 하나의 Library App 안에서 협력한다.",
            "Database 는 patron, book, catalogue, hold/checkouts sheet 저장소 역할을 맡는다.",
        ],
    },
}


def load_font(size: int) -> ImageFont.FreeTypeFont:
    return ImageFont.truetype(FONT_PATH, size)


def wrap(draw: ImageDraw.ImageDraw, text: str, font: ImageFont.ImageFont, width: int) -> list[str]:
    words = text.split()
    lines: list[str] = []
    current = ""
    for word in words:
        trial = word if not current else f"{current} {word}"
        if draw.textlength(trial, font=font) <= width:
            current = trial
        else:
            if current:
                lines.append(current)
            current = word
    if current:
        lines.append(current)
    if not lines:
        lines.append(text)
    return lines


def visual_entries():
    for relative, payload in VISUAL_TEXT.items():
        src = DOCS / relative
        out_root = KO_DOCS / relative
        yield src, out_root, payload["title"], payload["lines"]


def panel_height(draw: ImageDraw.ImageDraw, title: str, lines: list[str], width: int) -> tuple[int, list[str]]:
    title_font = load_font(TITLE_FONT_SIZE)
    header_font = load_font(HEADER_FONT_SIZE)
    body_font = load_font(BODY_FONT_SIZE)
    wrapped: list[str] = []
    for line in lines:
        wrapped.extend(wrap(draw, f"• {line}", body_font, width - PADDING * 2))
    title_lines = wrap(draw, title, title_font, width - PADDING * 2)
    height = PADDING
    height += int(header_font.size * 1.4)
    height += LINE_GAP * 2
    height += len(title_lines) * int(title_font.size * 1.45)
    height += LINE_GAP
    height += len(wrapped) * int(body_font.size * 1.5)
    height += PADDING
    return height, title_lines + ["__BODY_SPLIT__"] + wrapped


def render():
    probe = Image.new("RGB", (100, 100), "white")
    draw = ImageDraw.Draw(probe)
    for src, dst, title, lines in visual_entries():
        image = Image.open(src).convert("RGB")
        panel_h, wrapped = panel_height(draw, title, lines, image.width)
        canvas = Image.new("RGB", (image.width, image.height + panel_h), "white")
        canvas.paste(image, (0, 0))

        overlay = ImageDraw.Draw(canvas)
        y = image.height + PADDING

        header_font = load_font(HEADER_FONT_SIZE)
        title_font = load_font(TITLE_FONT_SIZE)
        body_font = load_font(BODY_FONT_SIZE)

        overlay.rectangle(
            [0, image.height, image.width, image.height + panel_h],
            fill=PANEL_BG,
        )
        overlay.line(
            [(0, image.height), (image.width, image.height)],
            fill=ACCENT,
            width=4,
        )
        overlay.text((PADDING, y), "한국어 해설", font=header_font, fill=HEADER_COLOR)
        y += int(header_font.size * 1.4) + LINE_GAP * 2

        body_mode = False
        for line in wrapped:
            if line == "__BODY_SPLIT__":
                body_mode = True
                y += LINE_GAP
                continue
            font = body_font if body_mode else title_font
            fill = BODY_COLOR if body_mode else TITLE_COLOR
            overlay.text((PADDING, y), line, font=font, fill=fill)
            y += int(font.size * (1.5 if body_mode else 1.45))

        dst.parent.mkdir(parents=True, exist_ok=True)
        canvas.save(dst)


if __name__ == "__main__":
    missing = [str(src) for src, _, _, _ in visual_entries() if not src.exists()]
    if missing:
        raise SystemExit(f"Missing source visuals: {missing}")
    render()
