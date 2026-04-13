# 이 코드베이스로 배우는 DDD 스터디 가이드

## 문서 목적

이 문서는 이 프로젝트를 다시 설계하거나 리라이트하기 위한 문서가 아니다.

이 문서의 목적은 이 코드베이스를 통해 아래를 학습하는 것이다.

- 이 코드가 어떤 문제를 풀려고 하는가
- 왜 저자들은 이런 구조를 택했는가
- 어떤 설계는 왜 일관적인가
- 어떤 설계는 맞는 답이라기보다 trade-off 인가
- 코드를 리뷰할 때 무엇을 의심하고 무엇을 인정해야 하는가
- AI 시대에 DDD 코드베이스를 어떻게 읽고, 질문하고, 비판할 것인가

이 문서를 읽을 때 기본 태도는 다음과 같다.

1. "이 아키텍처는 좋은가?"부터 묻지 않는다.
2. "어떤 문제가 이 선택을 강제했는가?"를 먼저 묻는다.
3. "이 선택은 무엇을 보호하는가?"를 본다.
4. "이 선택이 새로 만든 비용은 무엇인가?"를 따진다.
5. "상황이 달라지면 무엇을 바꿔야 하는가?"까지 생각한다.

이 저장소는 특히 학습용으로 좋다.
이유는 코드가 꽤 의도적이고, 선택들이 드러나 있기 때문이다.
완벽해서가 아니라, 왜 이런 선택을 했는지 읽기 좋기 때문에 학습 가치가 높다.

## 가장 먼저 붙잡아야 할 원칙

DDD는 레이어를 많이 만드는 기술이 아니다.
DDD는 비즈니스 의사결정을 어디에 둘지 정하고, 그 결정이 코드에서 흐려지지 않게 만드는 작업이다.

이 코드베이스의 핵심 질문은 "도서관 앱을 어떻게 구현할까?"가 아니다.
더 본질적인 질문은 이것이다.

"비즈니스 규칙은 실제로 어디에 살아야 하고, 어떻게 하면 그것이 controller, SQL, framework 코드 속에 녹아 없어지지 않게 할 수 있을까?"

그래서 이 저장소의 구조는 일반적인 CRUD 프로젝트보다 훨씬 더 명시적이다.

## 이 코드가 풀려는 문제는 무엇인가

이 도메인에는 단순 저장 이상의 복잡성이 있다.

- patron 은 아무 책이나 hold 할 수 없다
- patron 타입에 따라 규칙이 달라진다
- book 타입에 따라 규칙이 달라진다
- overdue 상태가 미래의 행동 가능성을 바꾼다
- 어떤 것은 즉시 처리되어야 한다
- 어떤 것은 나중에 read model 을 통해 파생된다
- 같은 "book" 이라는 말도 비즈니스 맥락에 따라 의미가 다르다

그래서 이 프로젝트는 `lending` 과 `catalogue` 를 분리한다.

핵심 문제는 단순히 데이터를 저장하는 것이 아니다.
핵심 문제는 비즈니스 규칙을 보호하는 것이고, 동시에 같은 현실 세계의 명사가 서로 다른 비즈니스 대화 속에서 다른 의미를 갖는다는 사실을 코드에 반영하는 것이다.

이건 DDD가 필요한 대표적인 신호다.

## 왜 Bounded Context 를 둘로 나눴을까

`lending` 과 `catalogue` 의 분리는 이 프로젝트에서 가장 중요한 첫 번째 설계 결정이다.

왜 이렇게 했을까.

- `catalogue` 에서는 핵심 일이 대체로 책과 인스턴스를 등록하는 것이다
- `lending` 에서는 누가, 어떤 책을, 어떤 조건에서, 얼마나 오래 hold 할 수 있는지 같은 의사결정이 핵심이다

저자들이 말하는 바는 분명하다.

"도메인의 모든 부분이 같은 수준의 아키텍처를 필요로 하지는 않는다."

이건 DDD에서 매우 중요한 감각이다.

### 이 판단이 중요한 이유

모든 곳에 같은 수준의 복잡한 설계를 강제로 적용하면 다음 문제가 생긴다.

- 단순한 영역이 과설계된다
- 어려운 영역은 여전히 어렵다
- 코드베이스는 명확해지는 대신 의식처럼 장황해진다

이 프로젝트는 `catalogue` 는 상대적으로 단순하게, `lending` 은 강하게 모델링한다.

### 여기서 배워야 할 것

코드 리뷰를 할 때는 이런 질문을 해야 한다.

- 진짜 비즈니스 긴장이 있는 곳은 어디인가
- 어디는 사실상 사실 기록에 가까운가
- 어디에서 잘못된 의사결정이 비즈니스에 가장 큰 피해를 주는가

모델링 에너지는 그곳에 먼저 써야 한다.

### 더 나은 대안은 없을까

상황에 따라 있다.

- `catalogue` 에 가격 정책, 입고 워크플로우, 메타데이터 품질 규칙, 규제 대응 같은 것이 들어오면 더 이상 "단순 CRUD"가 아닐 수 있다
- 반대로 `lending` 의 규칙이 실제 비즈니스에서는 매우 단순하다면 더 가벼운 구조가 맞을 수도 있다

핵심 교훈은 "항상 bounded context 를 나눠라"가 아니다.
"언어, 규칙, 변화 압력이 갈라지는 지점에서 나눠라"가 핵심이다.

## 왜 Modular Monolith 일까

이 프로젝트는 처음부터 마이크로서비스로 가지 않는다.
하나의 코드베이스, 하나의 프로세스 안에서 bounded context 를 패키지 수준으로 나눈다.

왜 이런 선택을 했을까.

- 도메인 경계를 유지하면서 분산 시스템 비용을 너무 빨리 지불하지 않기 위해
- 모델이 아직 형성되는 동안 더 빨리 바꾸고 실험할 수 있게 하기 위해
- 논의를 배포 토폴로지가 아니라 도메인 설계 자체에 집중시키기 위해

이건 매우 실용적인 선택이다.

DDD는 마이크로서비스를 요구하지 않는다.
오히려 너무 일찍 마이크로서비스로 가면, 잘못된 경계를 네트워크 호출로 가려버리기 쉽다.

### 더 나은 대안은 없을까

- Maven module 로 나누면 경계를 더 강하게 만들 수 있다
- 팀 구조, 확장성, 배포 독립성 압력이 크다면 별도 서비스로 가는 것이 맞을 수 있다

하지만 학습과 초기 모델링 단계에서는 현재 선택이 매우 설득력 있다.

## 왜 `Patron` 이 중심 aggregate 일까

이 저장소에서 가장 중요한 모델링 선택 중 하나는 hold 관련 판단의 중심을 `Book` 이 아니라 `Patron` 에 둔다는 점이다.

처음 보면 이상할 수 있다.
사용자 스토리는 대개 "책을 hold 한다"처럼 들리기 때문이다.

그래서 자연스럽게 이런 생각이 든다.

`book.placeOnHoldBy(patron)` 이 더 자연스럽지 않나?

하지만 핵심 invariant 는 대부분 patron 쪽에 있다.

- patron 타입
- 현재 hold 개수
- overdue checkout 개수
- 허용되는 hold 기간

즉 저자들은 "가장 유명한 명사"가 아니라 "가장 중요한 규칙을 보호하는 객체"를 aggregate root 로 선택했다.

이건 아주 좋은 DDD 교훈이다.

"aggregate root 는 단어의 중심이 아니라 invariant 보호의 중심으로 선택한다."

### 이 선택이 해결하는 문제

이렇게 하면 비즈니스 규칙이 다음 곳으로 흩어지는 것을 막을 수 있다.

- controller
- repository
- SQL 조건문
- utility 클래스
- 여기저기 흩어진 validator

결정은 aggregate 가 하게 된다.

### 이 선택이 만드는 비용

- book availability 같은 정보는 여전히 중요하므로 aggregate 간 조율이 필요하다
- application service 가 양쪽 정보를 읽어와야 한다
- 관련 모델을 동기화하기 위해 event 가 필요해진다

즉 설계는 더 명시적이 되지만, 동시에 더 복잡해진다.

### 더 나은 대안은 없을까

상황에 따라 있다.

- 책의 availability 가 가장 중요한 invariant 라면 `Book` 이 더 강한 aggregate root 일 수 있다
- 도메인이 훨씬 단순하다면 application service 안에서 transactional check 로 충분할 수도 있다

하지만 현재 도메인에서는 reject 로직이 patron 중심이기 때문에 `Patron` 선택은 충분히 설득력 있다.

## 왜 거대한 if-else 가 아니라 Policy 일까

`Patron` aggregate 는 hold 가능 여부 판단을 `PlacingOnHoldPolicy` 목록으로 나눈다.

왜 이런 방식을 썼을까.

- 각각의 규칙이 이름 있는 개념이 된다
- 규칙 조합이 쉬워진다
- 새 규칙이 생겨도 거대한 메서드를 갈아엎지 않아도 된다
- 테스트가 규칙 단위로 분리된다

이건 단순한 코드 정리 기법이 아니다.
도메인 이해를 코드 구조로 옮긴 것이다.

"자격 판단은 하나의 규칙이 아니라, 독립적으로 의미 있는 제약들의 집합이다."

### 더 나은 대안은 없을까

- specification pattern 으로 표현할 수도 있다
- 규칙이 운영 중에 자주 바뀌고 비개발자가 관리해야 한다면 rule engine 도 고려할 수 있다
- 규칙이 적고 안정적이라면 단순한 imperative 메서드가 더 나을 수도 있다

현재 구조는 외부 rule platform 까지 가지 않으면서도 규칙을 명시적으로 드러내고 싶은 경우에 잘 맞는다.

## 왜 상태 변경을 직접 저장하지 않고 Event 로 드러낼까

이 프로젝트는 의미 있는 상태 변경을 domain event 로 다루려는 방향이 강하다.

왜 이렇게 했을까.

- 상태 변경이 명시적으로 드러난다
- side effect 추적이 쉬워진다
- aggregate 사이의 통신 형식이 안정된다
- 테스트에서 객체 필드뿐 아니라 비즈니스 결과를 event 로 검증할 수 있다

그래서 patron repository 같은 곳은 일반적인 CRUD repository 와 다르게 동작한다.

- 새로운 상태를 저장한다
- 정규화된 domain event 를 publish 한다

이건 전형적인 layered CRUD 보다는 훨씬 event 중심적인 사고다.

### 이 선택이 해결하는 문제

이 설계는 DDD의 매우 중요한 질문 하나에 답한다.

"aggregate 는 서로의 내부를 직접 건드리지 않고 어떻게 협력하는가?"

이 코드베이스의 답은 event 다.

### 여기서 반드시 의심해야 할 점

이 패턴은 강력하지만, 책임이 섞일 위험도 있다.
repository 가 persistence 와 publication 을 모두 담당하면 더 이상 단순 persistence abstraction 이 아니다.

의도된 선택이라면 괜찮다.
하지만 리뷰할 때는 반드시 아래를 물어야 한다.

- event 는 aggregate 계약의 일부인가, 아니면 infrastructure 편의인가
- transaction 경계는 누가 책임지는가
- 저장은 성공하고 publish 가 실패하면 어떻게 되는가
- event 는 도메인의 진실인가, 구현 세부사항인가

### 더 나은 대안은 없을까

- aggregate 저장 후 event 를 application service 로 반환하고 outbox 에서 publish 할 수 있다
- event history 자체를 source of truth 로 삼는 event sourcing 도 가능하다
- 도메인이 단순하다면 classical repository 와 service orchestration 이 더 낫다

현재 구현은 교육용으로는 아주 좋은 중간 지점이다.
하지만 유일한 정답은 아니다.

## 왜 기본은 Immediate Consistency 이고, 설계는 Eventual Consistency 를 열어둘까

이 저장소에서 가장 배울 점이 많은 부분 중 하나다.

문서와 코드는 동시에 두 가지를 보여준다.

- 현재 구현은 immediate consistency 로 충분히 동작할 수 있다
- 하지만 설계는 eventual consistency 로 갈 수 있게 열어두었다

왜 이렇게 했을까.

실제 시스템은 처음부터 broker, outbox, retry, deduplication, 운영 자동화를 다 갖춘 상태로 시작하지 않는 경우가 많기 때문이다.

이건 아키텍처 성숙도의 표현이다.

"비즈니스가 아직 요구하지 않는 분산 일관성 비용을 너무 빨리 지불하지 않는다."

### 이 선택이 해결하는 문제

- 이벤트 중심 모델링은 유지하면서도 인프라 복잡성은 억제한다
- 테스트가 읽기 쉬워진다
- 미래의 전환 경로를 남긴다

### 숨은 교훈

DDD 와 event-driven design 은 전부 아니면 전무가 아니다.
이벤트라는 언어를 먼저 도입하고, 비동기 인프라는 나중에 붙일 수 있다.

### 더 나은 대안은 없을까

- 신뢰성과 확장성이 초기에 중요하다면 바로 outbox 패턴을 도입하는 편이 낫다
- 일관성을 매우 엄격하게 보장해야 한다면 한 transaction 안에서 더 많은 일을 처리하도록 경계를 다시 잡을 수도 있다

더 중요한 교훈은 이것이다.

- domain communication style
- infrastructure delivery style

이 둘은 관련이 있지만 같은 결정이 아니다.

## 왜 CQRS 비슷한 Read Model 을 둘까

이 프로젝트에는 `PatronProfile`, `DailySheet` 같은 조회 중심 모델이 등장한다.

왜 이렇게 했을까.

- write model 의 역할은 invariant 보호다
- read model 의 역할은 조회와 운영 지원이다
- hold 만료 대상 찾기, overdue checkout 찾기 같은 일은 목적 특화 projection 이 훨씬 쉽다

많은 DDD 학습자가 두 가지 실수를 자주 한다.

- 모든 조회를 aggregate 를 통해 하려고 한다
- 반대로 조회 모델이 진짜 비즈니스 모델을 잠식하게 둔다

이 프로젝트는 그 둘을 분리하려고 한다.

### 이 선택이 해결하는 문제

- 단순 조회를 위해 무거운 aggregate 를 읽지 않아도 된다
- 스케줄링과 운영 workflow 구현이 쉬워진다
- command 와 query 를 서로 다른 책임으로 최적화할 수 있다

### 더 나은 대안은 없을까

- 더 작은 시스템이라면 직접 SQL query service 만으로 충분할 수 있다
- 더 큰 시스템이라면 projection pipeline, outbox, consumer 구조를 더 명시적으로 가져가는 편이 낫다

여기서 중요한 것은 구현 디테일보다 원칙이다.

"invariant 를 지키는 모델과 화면/운영을 위한 뷰 모델을 혼동하지 않는다."

## 왜 ArchUnit 테스트를 쓸까

이 코드베이스는 architecture rule 을 테스트로 강제한다.

왜 이런 방식을 썼을까.

- 아키텍처 다이어그램은 시간이 지나면 쉽게 썩는다
- 좋은 의도만으로는 경계가 유지되지 않는다
- 팀이 압박을 받으면 가장 먼저 편의적인 dependency leakage 가 생긴다

이 테스트들은 아래 같은 주장을 보호한다.

- `catalogue` 는 `lending` 에 의존하면 안 된다
- domain model 은 infrastructure 에 의존하면 안 된다
- Spring 이 core domain logic 으로 침투하면 안 된다

이건 말뿐인 설계가 아니라, 실행 가능한 제약으로 아키텍처를 바꾸는 시도다.

### 더 나은 대안은 없을까

- 빌드 레벨 모듈 경계를 더 강하게 만들 수 있다
- package visibility 와 module system 으로 더 강하게 막을 수도 있다
- 아예 분리된 모듈/서비스로 나눌 수도 있다

그래도 architecture test 는 여전히 가치가 있다.
아키텍처를 문서가 아니라 executable constraint 로 만들기 때문이다.

## 이 설계에서 무엇이 일관적인가

학습 관점에서 가장 강한 부분은 다음이다.

- 문제 중심의 `catalogue` / `lending` 분리
- invariant 중심의 aggregate 선택
- policy 를 통한 규칙 모델링
- event 기반의 cross-aggregate communication
- read model 분리
- 테스트로 강제되는 architecture rule

이 선택들은 각자 따로 노는 패턴이 아니다.
하나의 일관된 이야기로 이어진다.

"비즈니스 의사결정이 눈에 보이게 남고, 실수로 우회하기 어렵게 만들자."

중요한 건 각각의 구현 디테일이 완벽하냐가 아니라, 이 전체 방향성이 서로 충돌하지 않느냐이다.

## 어디를 가장 강하게 비판해야 하는가

좋은 DDD 독자는 패턴 숭배자가 아니다.
다음 지점은 반드시 날카롭게 봐야 한다.

### 1. Repository 책임이 커지는 문제

이 저장소의 repository 는 persistence 만 하지 않는다.
이벤트 발행까지 일부 책임진다.

이건 가능하지만, abstraction 이 여전히 깨끗한지 항상 의심해야 한다.

### 2. Event publication 의 신뢰성

아이디어는 좋다.
하지만 production 수준의 delivery guarantee 는 별개다.

운영 관점에서는 다음을 반드시 물어야 한다.

- retry 는 있는가
- duplicate 는 어떻게 처리하는가
- ordering 은 중요한가
- transaction 과 어떻게 묶이는가
- dead letter 나 재처리는 어떻게 하는가

### 3. Package 이름에 의존한 architecture enforcement

어떤 architecture rule 은 강하다.
하지만 어떤 것은 패키지 naming 과 실제 구조가 완전히 일치하지 않으면 생각보다 약해질 수 있다.

즉 architecture test 는 강력하지만, rule 이 실제 코드 구조를 정확히 반영할 때만 의미가 크다.

### 4. API 의미론과 domain 의미론의 차이

도메인 모델은 꽤 풍부할 수 있다.
하지만 HTTP API 가 성공과 rejection 을 충분히 구분하지 않으면, domain 의 풍부함이 바깥 경계에서 납작해진다.

즉 edge layer 가 도메인 의미를 얼마나 잘 보존하는지도 봐야 한다.

### 5. 교육용 설계와 운영용 설계의 차이

이 저장소는 부분적으로 "학습하기 좋게" 설계되어 있다.
그래서 어떤 선택은 production 최적화보다 명시성을 더 중시한다.

실서비스에서는 그 명시성이 계속 비용 대비 가치를 가지는지 다시 판단해야 한다.

## 리뷰 프레임워크: 반드시 이 세 질문으로 읽기

이 코드베이스를 볼 때 주요 결정마다 항상 같은 세 질문을 던져라.

### A. 문제가 무엇인가

- 여기서 비즈니스 리스크는 무엇인가
- 어떤 invariant 가 깨질 수 있는가
- 어떤 언어적 모호함을 해소하려는가
- 어떤 변화 압력이 이 영역에 걸려 있는가

### B. 왜 이 해법인가

- 이 설계는 무엇을 보호하는가
- 어떤 coupling 을 줄이는가
- 어떤 accidental complexity 를 받아들이는가
- 왜 여기서는 단순 layered CRUD 보다 낫다고 판단했는가

### C. 더 나은 대안은 무엇인가

- 어떤 상황에서는 이 설계를 거부해야 하는가
- 팀 규모, 트래픽, 규제, 운영 요구가 바뀌면 어떻게 달라져야 하는가
- 도메인이 더 단순하다면 무엇을 걷어낼 것인가
- 도메인이 더 역동적이라면 무엇을 더해야 하는가

이 세 질문에 답하지 못하면 아직 코드를 이해한 것이 아니다.

## 당신이 원한 리뷰 관점별 정리

## 판단

작성자가 pattern 이름만 말하는가, 아니면 trade-off 를 설명하는가를 보라.

좋은 설명의 예:

- "여기서 CQRS 비슷한 분리를 둔 이유는 daily operation 조회가 invariant 보호용 write model 과 본질적으로 다르기 때문이다"

약한 설명의 예:

- "DDD 프로젝트니까 CQRS 를 썼다"

## 설계

경계가 기술 레이어가 아니라 비즈니스 언어와 변화 압력에 맞춰져 있는가를 봐야 한다.

좋은 신호:

- `catalogue` 와 `lending` 의 분리
- 목적 특화 read model

약한 신호:

- bounded context 대신 controller/service/repository 만 있는 구조

## 정합성

무엇은 즉시 일관돼야 하고, 무엇은 eventual consistency 여도 괜찮은가를 구분해야 한다.

좋은 신호:

- 그 차이를 코드와 문서에서 인지하고 있다
- 나중에 바꿀 수 있는 seam 이 있다

약한 신호:

- event-driven 이면 자동으로 충분히 정합적일 것이라고 착각한다

## 안정성 / 운영

이 설계가 실제 운영 압력 속에서도 견딜 수 있는지를 물어야 한다.

반드시 물어볼 것:

- 이벤트 발행이 실패하면 어떻게 되는가
- 무엇이 idempotent 한가
- 어디가 관측 가능한가
- 무엇을 replay 할 수 있는가
- 어떤 기능이 timing 에 민감한가

이 프로젝트는 metrics 와 단순한 event publication 으로 대화를 시작하게는 해 주지만, 운영 완성형 설계까지 보여주지는 않는다.

## 기술 선택 이유를 설명하는 힘

기술 선택을 기술 자체가 아니라 도메인/운영 맥락으로 설명할 수 있어야 한다.

예시:

- Spring: 비즈니스 로직 프레임워크가 아니라 wiring 과 infrastructure 지원
- ArchUnit: 아키텍처 제약을 문서가 아니라 테스트로 강제
- H2: 빠른 로컬 학습과 테스트
- Micrometer / Prometheus: 이벤트 흐름과 시스템 상태의 최소 관측성 확보
- Vavr: 성공, 실패, optionality 를 명시적으로 표현

설명이 "유명해서", "많이 써서" 수준이면 부족하다.

## 이 코드베이스가 아주 잘 가르쳐 주는 것

- entity 가 아니라 decision 중심으로 모델링하는 법
- 단순한 context 는 단순하게 두는 법
- language boundary 를 코드에 드러내는 법
- event 로 비즈니스 반응을 느슨하게 연결하는 법
- read 와 write 를 역할별로 분리하는 감각
- architecture 를 executable 하게 만드는 태도

## 이 코드베이스만으로는 배우기 어려운 것

- production-grade event delivery
- outbox / inbox 패턴의 실제 운영
- 장기적인 schema evolution 전략
- distributed tracing 과 incident response
- 팀 간 모델 소유권 관리

즉 이 저장소를 이해했다고 해서 production DDD 를 다 이해한 것은 아니다.
하지만 핵심 사고 훈련에는 아주 좋다.

## 이 저장소를 실제로 공부하는 순서

아래 순서로 읽는 것이 좋다.

1. 도메인 설명과 event storming 문서를 먼저 읽는다
2. 구현 클래스를 보기 전에 bounded context 를 먼저 구분한다
3. 하나의 비즈니스 흐름을 끝까지 따라간다
4. 각 흐름마다 문제, invariant, aggregate, event, read model, failure path 를 적는다
5. 그 다음에야 infrastructure 선택을 평가한다

첫 번째 추천 흐름은 다음이다.

- hold placement
- hold cancellation
- hold expiration
- overdue registration

## 이 저장소에서의 추천 읽기 순서

아래 파일 순서로 읽으면 좋다.

1. `README.md`
2. `docs/ko/big-picture.md`
3. `docs/ko/design-level.md`
4. `src/main/java/io/pillopl/library/LibraryApplication.java`
5. `src/main/java/io/pillopl/library/lending/LendingConfig.java`
6. `src/main/java/io/pillopl/library/catalogue/CatalogueConfiguration.java`
7. `src/main/java/io/pillopl/library/lending/patron/application/hold/PlacingOnHold.java`
8. `src/main/java/io/pillopl/library/lending/patron/model/Patron.java`
9. `src/main/java/io/pillopl/library/lending/book/application/PatronEventsHandler.java`
10. `src/main/java/io/pillopl/library/lending/dailysheet/infrastructure/SheetsReadModel.java`
11. `src/main/java/io/pillopl/library/lending/patron/infrastructure/PatronsDatabaseRepository.java`
12. `src/test/groovy/io/pillopl/library/ModularArchitectureTest.java`
13. `src/test/groovy/io/pillopl/library/lending/architecture/LendingHexagonalArchitectureTest.java`
14. `src/test/groovy/io/pillopl/library/lending/architecture/NoSpringInDomainLogicTest.java`

이 순서는 다음 흐름으로 이어진다.

- 도메인 이야기 이해
- 아키텍처 진입점 파악
- 대표 write use case 읽기
- aggregate 의 의사결정 읽기
- event 반응 읽기
- read model projection 읽기
- persistence 경계 읽기
- architecture enforcement 읽기

## AI 시대에 이 코드베이스를 어떻게 공부할 것인가

AI는 DDD 학습에서 critic, mapper, question generator 로 쓸 때 가장 유용하다.
반대로 "아키텍처 장식기"로 쓰면 거의 항상 해롭다.

### 좋은 AI 질문

- "hold placement 유스케이스를 끝까지 추적하고 각 invariant 가 어디서 보호되는지 찾아줘"
- "`Patron` 의 지식이 aggregate 밖으로 새는 지점을 모두 찾아줘"
- "현재 event publication 방식과 outbox 패턴을 비교해줘"
- "이 아키텍처 제약 중 실제로 강한 것과 관습에 가까운 것을 구분해줘"
- "HTTP 의미론이 domain 의미론을 납작하게 만드는 지점을 찾아줘"

### 나쁜 AI 질문

- "이걸 clean architecture 로 다시 짜줘"
- "더 엔터프라이즈스럽게 바꿔줘"
- "DDD 패턴을 더 넣어줘"

이런 질문은 대체로 pattern inflation 만 만든다.

### 좋은 AI 학습 루프

1. AI 에게 유스케이스 추적을 시킨다
2. 모든 주장에 대해 직접 코드를 검증한다
3. AI 에게 대안 설계를 물어본다
4. 그 대안을 실제 비즈니스 압력과 비교해 평가한다
5. 마지막으로 자기 언어로 decision memo 를 쓴다

길러야 할 능력은 "AI 로 아키텍처를 생성하는 능력"이 아니다.
"AI 를 써서 자신의 아키텍처 판단력을 더 날카롭게 만드는 능력"이다.

직접 손으로 다시 구현해 보는 다음 단계에 관심이 있다면
`docs/ko/ddd-monolith-rebuild-notes.md` 도 함께 보는 것이 좋다.

## AI 시대에 앞으로 어떤 엔지니어가 되어야 하나

이런 코드베이스를 학습 재료로 삼는다면, 앞으로는 다음 근육을 길러야 한다.

- 비즈니스 규칙을 코드 경계로 번역하는 힘
- pattern 이름이 아니라 trade-off 를 설명하는 힘
- essential complexity 와 accidental complexity 를 구분하는 힘
- 아키텍처를 미학이 아니라 failure mode 로 리뷰하는 힘
- 어디는 의도적으로 단순해야 하는지 판단하는 힘
- 어디에는 DDD 를 적용하지 않는 것이 더 나은지 결정하는 힘

AI 는 코드 생성을 더 싸게 만들 것이다.
그럴수록 설명력, 판단력, 경계 설계 능력은 더 중요해진다.

앞으로 더 가치 있는 엔지니어는 pattern 을 많이 외운 사람이 아니다.
다음 다섯 가지를 말할 수 있는 사람이다.

- 문제가 무엇인지
- 무엇이 반드시 참이어야 하는지
- 왜 이 설계가 그것을 보호하는지
- 어떤 trade-off 를 받아들였는지
- 언제 이 설계를 바꿔야 하는지

## 마지막으로 붙잡아야 할 핵심 문장

이 저장소가 가장 강하게 가르쳐 주는 것은 hexagonal architecture 도 아니고, event 도 아니고, DDD 용어 자체도 아니다.

가장 중요한 교훈은 이것이다.

"모델링이란 무엇을 잘못하기 어렵게 만들 것인지 결정하는 일이다."

클래스, 경계, event, projection 을 볼 때마다 이렇게 물어라.

"이 구조는 어떤 실수를 막기 위해 존재하는가?"

그 질문이 pattern 이름을 외우는 것보다 훨씬 더 많은 것을 가르쳐 줄 것이다.
