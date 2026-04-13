# 도메인 명세 설명서

## 문서 목적

이 문서는 이 프로젝트의 구현 구조를 설명하는 문서가 아니다.
이 문서는 "이 시스템이 어떤 비즈니스 세계를 모델링하고 있는가"를 설명하는 도메인 명세 문서다.

즉 이 문서는 다음 질문에 답하기 위해 작성한다.

- 이 시스템 안에서 어떤 행위자와 개념이 중요한가
- 어떤 규칙이 반드시 지켜져야 하는가
- 어떤 사건이 비즈니스적으로 의미 있는가
- 어떤 맥락에서 같은 단어가 다른 의미를 가지는가
- 시스템이 어떤 흐름으로 동작해야 하는가

DDD 관점에서 이 문서는 코드보다 한 단계 위에 있는 "업무 개념 지도"로 읽으면 된다.

## 시스템 한 문장 설명

이 시스템은 공공 도서관에서 책을 등록하고, 이용자가 책을 hold, checkout, return 하는 과정을 관리하며, hold 만료와 overdue 상태를 추적하는 도메인을 다룬다.

## 핵심 목표

이 도메인의 핵심 목표는 단순히 책과 이용자 정보를 저장하는 것이 아니다.

핵심 목표는 다음 두 가지다.

1. 도서관 대출 규칙을 일관되게 지키는 것
2. 시간 경과에 따라 상태가 바뀌는 비즈니스 사건을 추적하는 것

즉, 이 시스템은 "현재 상태 조회"보다 "어떤 규칙에 의해 어떤 상태 변화가 허용되거나 거부되는가"가 더 중요하다.

## 주요 행위자

### Patron

도서관 이용자다.
이 시스템에서 patron 은 단순한 사용자 레코드가 아니라, 대출 자격과 제약을 갖는 핵심 도메인 주체다.

patron 은 두 가지 유형으로 나뉜다.

- `Regular`
- `Researcher`

두 유형은 hold 가능 여부와 hold 기간 규칙에서 차이를 가진다.

### Library Employee

도서 catalog 를 관리하는 역할이다.
책과 책 인스턴스를 catalogue 에 등록한다.

### System

시스템은 단순 저장소가 아니라, 매일 특정 시점에 hold 만료와 overdue checkout 을 점검하는 능동적 역할도 가진다.

즉 이 도메인에는 사람만이 아니라 "시간에 반응하는 시스템"도 행위자처럼 등장한다.

## 핵심 용어

### Book

이 용어는 문맥에 따라 의미가 달라진다.
이 점이 이 프로젝트에서 매우 중요하다.

- `catalogue` 맥락에서의 book:
  ISBN, 제목, 저자 같은 서지 정보를 가진 등록 대상
- `lending` 맥락에서의 book:
  실제로 hold, checkout, return 의 대상이 되는 대출 가능 자원

즉 현실에서는 같은 "책"이지만, 도메인 모델에서는 같은 개념이 아니다.

### Book Instance

catalogue 에 등록된 특정 실물 또는 대출 단위다.
같은 ISBN 을 가진 책이라도 여러 인스턴스가 있을 수 있다.

### Book Type

책은 대출 관점에서 두 가지 유형을 가진다.

- `Circulating`
- `Restricted`

`Restricted` 는 더 강한 제약을 가진다.

### Hold

이용자가 특정 책을 대출하기 위해 선점해 두는 상태다.
hold 는 즉시 checkout 이 아니라 "대출 권리를 일정 기간 보유"하는 의미에 가깝다.

### Close-ended Hold

종료 시점이 있는 hold 다.
일정 기간 안에 checkout 하지 않으면 만료될 수 있다.

### Open-ended Hold

종료 시점이 정해지지 않은 hold 다.
이 hold 는 만료되지 않는다.
단, 모든 patron 이 사용할 수 있는 것은 아니다.

### Checkout

책을 실제로 대출한 상태다.
checkout 은 최대 기간 제한을 가진다.

### Overdue Checkout

정해진 checkout 기간을 넘긴 대출 상태다.
이 상태는 이후 hold 가능 여부에 영향을 준다.

### Daily Sheet

매일 점검해야 하는 hold 만료 대상과 overdue 대상 목록을 표현하는 도메인 뷰다.
이건 단순한 기술적 테이블이 아니라 "매일 운영 판단을 위한 업무 시트"라는 개념이다.

### Patron Profile

특정 patron 이 현재 가진 hold 와 checkout 을 보는 읽기 모델이다.
이용자 관점의 상태 요약 화면에 해당한다.

## Bounded Context

이 시스템은 두 개의 주요 bounded context 로 이해할 수 있다.

## 1. Catalogue

책과 책 인스턴스를 등록하는 맥락이다.

핵심 관심사는 다음이다.

- 어떤 책이 존재하는가
- 어떤 ISBN 이 등록되어 있는가
- 특정 책 인스턴스를 대출 가능한 대상으로 만들 수 있는가

이 맥락에서 중요한 것은 "책의 존재와 분류"다.

## 2. Lending

책을 hold, checkout, return 하는 맥락이다.

핵심 관심사는 다음이다.

- 누가 어떤 책을 hold 할 수 있는가
- hold 가 언제 만료되는가
- 누가 checkout 할 수 있는가
- overdue 상태가 이후 행동을 어떻게 막는가

이 맥락에서 중요한 것은 "자격, 제약, 상태 전이"다.

## 왜 이 둘을 나누는가

같은 "book" 이라는 단어를 쓰더라도 관심사가 완전히 다르기 때문이다.

- catalogue 는 등록과 분류 중심이다
- lending 은 규칙과 의사결정 중심이다

이 분리는 단순한 기술 분리가 아니라 언어 분리다.

## 도메인의 핵심 규칙

아래 규칙은 이 도메인을 이해할 때 가장 먼저 붙잡아야 한다.

### Hold 관련 규칙

1. 한 시점에 available 한 책은 한 patron 만 hold 할 수 있다.
2. `Restricted` 책은 `Researcher` patron 만 hold 할 수 있다.
3. `Regular` patron 은 동시에 최대 5개의 hold 만 가질 수 있다.
4. `Researcher` patron 은 hold 수 제한이 없다.
5. `Regular` patron 은 open-ended hold 를 만들 수 없다.
6. `Researcher` patron 은 open-ended hold 를 만들 수 있다.
7. 특정 library branch 에서 overdue checkout 이 2개 이상인 patron 은 그 branch 에서 hold 할 수 없다.
8. close-ended hold 는 정해진 시한 안에 checkout 되지 않으면 만료된다.
9. open-ended hold 는 만료되지 않는다.

### Checkout 관련 규칙

1. 책은 최대 60일까지 checkout 할 수 있다.
2. checkout 은 hold 가 존재할 때만 가능하다.
3. 다른 patron 이 hold 한 책은 checkout 할 수 없다.
4. return 이 발생하면 checkout 상태는 종료된다.
5. checkout 기한을 넘기면 overdue 상태가 된다.

### Catalogue 관련 규칙

1. 책 인스턴스는 먼저 해당 ISBN 의 책이 catalogue 에 등록되어 있어야만 추가할 수 있다.
2. 같은 ISBN 을 가진 책이라도 `Circulating` 과 `Restricted` 인스턴스가 공존할 수 있다.

## 시간 개념

이 도메인에서는 "지금 상태" 못지않게 "언제 무슨 일이 발생했는가"가 중요하다.

특히 아래 두 흐름은 시간의 영향을 강하게 받는다.

- hold 만료
- overdue checkout 등록

즉 이 시스템은 단순 request-response 시스템이 아니라, 시간에 따라 도메인 상태가 재해석되는 시스템이다.

## 상태 전이 관점에서 본 핵심 흐름

## 1. 책 등록 흐름

### 목적

도서관이 대출 가능한 자원을 catalogue 에 등록한다.

### 흐름

1. 직원이 책의 서지 정보를 등록한다
2. 등록된 책에 대해 특정 인스턴스를 추가한다
3. 인스턴스가 추가되면 lending 맥락에서 대출 가능한 책이 생성될 수 있다

### 중요한 점

catalogue 의 변화가 lending 쪽의 "available book" 생성으로 이어질 수 있다.
즉 context 간에는 느슨하지만 의미 있는 연결이 있다.

## 2. Hold 생성 흐름

### 목적

patron 이 특정 책에 대한 대출 권리를 선점한다.

### 전제 조건

- 책이 available 해야 한다
- patron 이 자격을 충족해야 한다
- 책의 유형과 patron 의 유형이 맞아야 한다
- 해당 branch 에 overdue 제약이 없어야 한다

### 성공 시 결과

- `BookPlacedOnHold` 이벤트가 발생한다
- 책 상태는 on hold 로 바뀐다
- patron 의 현재 hold 상태가 갱신된다
- daily sheet 와 patron profile 이 갱신될 수 있다

### 실패 시 결과

- `BookHoldFailed` 이벤트가 발생한다
- 실패 이유는 비즈니스 규칙 위반이다

### 도메인적으로 중요한 의미

hold 는 단순한 상태 플래그가 아니다.
hold 는 "이 patron 이 이 책을 빌릴 권리를 일정 기간 확보했다"는 비즈니스 사실이다.

## 3. Hold 취소 흐름

### 목적

patron 이 자신이 가진 hold 를 철회한다.

### 전제 조건

- 해당 hold 가 실제로 존재해야 한다
- 그 hold 는 해당 patron 의 hold 여야 한다

### 성공 시 결과

- `BookHoldCanceled` 이벤트가 발생한다
- 책은 다시 available 상태가 될 수 있다
- patron profile 과 daily sheet 가 갱신된다

### 실패 시 결과

- `BookHoldCancelingFailed` 이벤트가 발생한다

## 4. Checkout 흐름

### 목적

hold 상태의 책을 실제 대출 상태로 전환한다.

### 전제 조건

- hold 가 존재해야 한다
- checkout 하는 patron 이 해당 hold 의 소유자여야 한다
- checkout 기간은 최대 60일을 넘을 수 없다

### 성공 시 결과

- `BookCheckedOut` 이벤트가 발생한다
- hold 는 완료된다
- checkout sheet 와 patron profile 이 갱신된다

### 실패 시 결과

- `BookCheckingOutFailed` 이벤트가 발생한다

## 5. Hold 만료 흐름

### 목적

close-ended hold 중 기한을 넘긴 것을 자동 만료 처리한다.

### 실행 주체

시스템

### 입력

daily sheet 에서 만료 대상 hold 목록

### 결과

- `BookHoldExpired` 이벤트가 발생한다
- 책은 hold 상태에서 벗어난다
- 관련 뷰가 갱신된다

### 중요한 점

hold 만료는 patron 의 직접 요청이 아니라 시간 경과에 의해 발생한다.

## 6. Overdue 등록 흐름

### 목적

checkout 기한을 넘긴 대출을 overdue 로 등록한다.

### 실행 주체

시스템

### 입력

daily sheet 에서 overdue 대상 checkout 목록

### 결과

- `OverdueCheckoutRegistered` 이벤트가 발생한다
- 이후 같은 branch 에서 hold 가능 여부에 제약이 생긴다

## 주요 도메인 이벤트

이 시스템에서 중요한 것은 "상태"만이 아니라 "무슨 일이 있었는가"다.
아래 이벤트들은 이 도메인의 핵심 비즈니스 사건이다.

### Patron 관련

- `PatronCreated`

### Hold 관련

- `BookPlacedOnHold`
- `BookHoldFailed`
- `BookHoldCanceled`
- `BookHoldCancelingFailed`
- `BookHoldExpired`
- `MaximumNumberOhHoldsReached`

### Checkout 관련

- `BookCheckedOut`
- `BookCheckingOutFailed`
- `BookReturned`
- `OverdueCheckoutRegistered`

### Catalogue 관련

- `BookInstanceAddedToCatalogue`

### 운영/정합성 관련 특수 이벤트

- `BookDuplicateHoldFound`

이 이벤트는 이미 다른 patron 이 hold 중인 책에 대해 중복 hold 상황이 감지되었음을 뜻한다.
즉 이 시스템은 이상 상황도 도메인 사건으로 다룬다.

## 도메인 모델이 특별히 중요하게 보는 것

이 도메인은 다음을 중요한 비즈니스 진실로 본다.

### 1. Patron 의 자격

patron 유형은 단순 속성이 아니다.
어떤 행동이 허용되는지를 결정하는 규칙의 핵심 입력이다.

### 2. Book 의 availability

책이 존재하는 것과 대출 가능하다는 것은 다르다.
대출 도메인에서는 "available 한가"가 핵심 상태다.

### 3. Branch 단위 제약

overdue 규칙은 전역이 아니라 branch 기준으로 작동한다.
즉 같은 patron 이라도 branch 에 따라 hold 가능 여부가 달라질 수 있다.

### 4. 시간

close-ended hold 와 overdue checkout 은 시간 없이는 정의될 수 없다.
이 도메인은 시간에 민감하다.

### 5. 읽기 모델의 업무 의미

`PatronProfile` 과 `DailySheet` 는 단순 조회 DTO 가 아니다.
둘 다 실제 업무에서 의미 있는 뷰다.

- `PatronProfile`: 한 patron 이 자신의 현재 상태를 이해하기 위한 뷰
- `DailySheet`: 운영자가 매일 처리해야 할 예외/후속 작업을 위한 뷰

## 이 명세에서 특히 혼동하기 쉬운 부분

### "Book" 은 하나의 개념이 아니다

catalogue 의 book 과 lending 의 book 은 구분해서 이해해야 한다.

### Hold 와 Checkout 은 같은 것이 아니다

hold 는 대출 권리 확보 상태다.
checkout 은 실제 대출 상태다.

### 실패도 중요한 도메인 결과다

이 시스템에서는 실패가 단순 예외가 아니라 비즈니스 결과일 수 있다.
즉 "hold 실패" 자체가 도메인적으로 의미 있는 사건이다.

### 시간에 의해 발생하는 사건이 있다

모든 상태 변화가 사용자 요청으로 시작되는 것은 아니다.
만료와 overdue 등록은 시스템 주도 흐름이다.

## 비즈니스 관점에서 본 성공 기준

이 시스템이 올바르게 동작한다는 것은 아래가 보장된다는 뜻이다.

- 자격 없는 patron 은 hold 할 수 없어야 한다
- hold 가능한 patron 은 필요한 경우 정상적으로 hold 할 수 있어야 한다
- hold 와 checkout 은 시간과 규칙에 맞게 상태가 전이되어야 한다
- 만료와 overdue 는 빠지지 않고 반영되어야 한다
- catalogue 변경은 lending 가능 자원 생성과 의미 있게 연결되어야 한다
- patron 과 운영자는 각자 필요한 뷰를 통해 현재 상황을 이해할 수 있어야 한다

## 이 문서를 읽고 나서 코드에서 확인해야 할 것

이 문서로 도메인을 먼저 이해한 뒤, 코드에서는 아래를 확인하면 된다.

1. hold 자격 규칙이 어디서 보호되는가
2. hold 와 checkout 상태 전이가 어떤 이벤트로 표현되는가
3. `DailySheet` 와 `PatronProfile` 이 어떻게 갱신되는가
4. `catalogue` 에서 `lending` 으로 어떤 사건이 넘어가는가
5. 실패가 예외인지, 도메인 결과인지 구분되어 있는가

## 함께 보면 좋은 문서

- `README.md`
- `docs/ko/big-picture.md`
- `docs/ko/design-level.md`
- `docs/ko/ddd-study-guide.md`
- `docs/ko/ddd-monolith-rebuild-notes.md`

이 문서가 "무슨 세계를 다루는가"를 설명한다면, 위 문서들은 "왜 이렇게 모델링했는가"를 더 잘 설명해 준다.
