Title: Interview Review
Subtitle: PHP 백엔드 개발자 면접 후기
Category: misc
Date: 2024-08-20 00:00

## 면접 후기

이번 이직은 개발팀장에서 다시 개발자로 포지션을 변경하는, 새로운 도전의 시간이었다.
최근 2년 동안 다른 사람들의 이력서를 확인만 해왔는데 직접 이력서를 작성하고 오랜만에 면접에 들어가니, 그간의 경력이 우습게도 어렵고 낯설게 느껴졌다.

시장이 좋지 않아서 인지 PHP 채용 공고가 적어서, 학력 무관한 서울 내에 있는 40여개 회사에 전부 지원했고 여섯 번의 면접을 보았다.
별다른 준비를 하지 않고 즉흥적으로 대답하였더니 상당히 긴장되었고, 예상 밖의 질문에 당황하기도 했다.
특히 화상 면접의 경우, 명확하게 들리지 않기도 하고 표정이나 분위기를 읽을 수 없어 대면 면접보다 더 어려웠다.

세 개의 회사에서 긍정적인 답변을 받았고, 그 중 기술적으로 더 성장할 수 있는 회사를 선택했다.  
(사실, 집과 가깝다는 점도 중요한 선택 요인이었다...)

## 질문 정리

기억에 남는 질문과 답변, 혹은 유용한 정보를 간단하게 정리

### 일반

#### 간단하게 혹은 1분 자기소개

- 이름, 나이, 경력, 지원동기 등을 포함하여 1분 내외로 소개

#### 공백 기간이 있었는데, 이 기간 동안 무엇을 하셨나요?

#### 대학교에서 어떤 내용을 배웠고, 왜 휴학하셨나요?

#### 평소에 어떻게 공부하고 있나요?

- 책이나 강의, 토이 프로젝트, 스터디 운영 등을 통해 공부하는 방법과 주제

### 이전 직장

#### 이전 회사에서 담당하신 업무와 프로젝트에 대해 설명해주세요.

#### 업무 중 마찰이나 갈등을 겪었을 때, 어떻게 대처하고 해결했나요?

#### 퇴사를 하게 된 특별한 이유가 있나요?

### 팀 관리

#### 개발팀은 어떻게 구성되어 있었나요?

- 다양한 사람들과 협업하며, 업무를 이해하고 지원

#### 프로젝트 관리나 개발 프로세스는 어떻게 진행했나요?

- 지라 혹은 노션 사용 방법과 애자일(스크럼, 칸반) 등의 방법론

#### 지라나 컨플루언스를 왜, 어떻게 활용했나요?

- [agile](https://www.atlassian.com/ko/agile)

#### 애자일에 대해 가지고 있는 특별한 인사이트(생각이나 경험)가 있나요?

- 적응력과 자율성, 빠른 실패 등

### 기술

#### SOLID 원칙에 대해 간단하게 설명해주세요.

- 코드의 유지보수와 확장성을 위한 객체지향 설계의 5가지 원칙

#### 사용하셨던 DTO, DAO, Repository에 대해 설명해주세요.

- DAO와 Repository는 Eloquent Model이 있어 사용하지 않음

#### HTTP Method나 Status Code에 관한 경험이 있나요?

- Status code 관련 논의나 노후화된 시스템 문제로 GET&POST로만 처리
- [status code decision](https://github.com/for-GET/http-decision-diagram)

#### 결제 시스템을 구현하거나 PG 연동 시, 발생했던 문제와 해결 방법을 말씀해주세요.

- 결제 관련 문제(결제 트랜잭션 관리, 결제 승인 딜레이, 결제 취소 등)와 보안 문제를 경험

#### 개발할 때 선호하는 IDE나 추천하는 플러그인이 있나요?

- VSCode를 커스텀하여 사용해보려 했으나, PHPStorm이 더 편리하다고 생각

#### 새로운 기술이나 언어를 배우는 것에 대해 어떻게 생각하시나요? 학습 의사가 있나요?

- 능력이나 시간이 부족하여, 새로운 기술을 배우는 것에 대해 걱정이 있으나, 끊임없이 공부하고자 함

#### 최근에 관심을 가지고 있는 기술이나 분야가 있나요?

- CI/CD (GitHub Actions) 자동화와 AI 관련 기술이나 서비스에 관심이 있음

#### 기술적으로 가장 어렵거나 복잡했던 일을 하나 공유해주세요.

- 트래픽이 증가하며 발생한 서버와 네트워크 문제. 서버 모니터링과 로그 분석. VPC와 보안, CDN 설정 등

### PHP&Laravel

#### 주로 어떤 기술이나 언어를 선호하고 어떤 버전을 사용하고 있나요?

#### 언어나 프레임워크의 버전을 업그레이드하며 발생했던 문제와 해결 방법을 말씀해주세요.

#### Modern PHP와 PSR에 대해 이해하고 계신가요?

- Modern PUG와 PHP THE RIGHT WAY 확인. PSR, PER 준수
- [modern php](https://edykim.com/ko/post/comparing-paleolithic-php-with-modern-php/)

#### Xdebug 같은 디버깅 도구를 사용하신 경험이 있으신가요? 사용하신다면 어떤 방식으로 사용하셨나요?

- Xdebug는 미사용, debugbar나 clockwork 사용. 간단한 디버깅은 dd나 Log 사용

#### Laravel이 어떻게 동작하는지, 라이프사이클을 알고 계신가요?

#### Eloquent ORM에 대해 알고 계신 내용을 자유롭게 설명해주세요.

- [효과적인 Eloquent](https://velog.io/@seunghaekim/%ED%9A%A8%EA%B3%BC%EC%A0%81%EC%9D%B8-Eloquent)

#### ORM과 Query Builder를 사용해 보셨다면, 차이점과 사용 경험을 말씀해주세요.

- ORM은 생산성을 위해 간결하게 처리. Query Builder는 대규모 데이터나 성능 최적화가 필요한 경우 사용
- [ORM vs Query Builder](https://medium.com/@andreelm/eloquent-orm-vs-query-builder-in-laravel-47f104452644

#### Mutator와 Accessor를 사용하신 경험이 있나요?

- 날짜 형식, 타입이나 암호화된 데이터 핸들링 사용 경험
- [accessors-and-mutators](https://medium.com/@lordNeic/did-you-know-about-laravel-model-accessors-and-mutators-3de69ba376fd)
- [getters and setters](https://colabear754.tistory.com/173)

#### Eager Loading과 Lazy Loading의 차이점과 사용하며 겪었던 문제를 말씀해주세요.

#### (Laravel에서) 사용했던 패턴이나 구조에 대해 설명해주세요.

- Service, Facade, Action 등을 활용

### DB

#### 데이터베이스를 설계해 본 경험이 있으신가요? 어떤 점을 고려하셨나요?

- 정규화, 성능, 확장성 등을 고려하여 설계

#### 데이터베이스 성능을 개선하거나 최적화한 경험이 있으신가요?

- 트래픽 증가로 인해 인덱스, 쿼리 최적화, 캐싱 등을 활용
- [cloudflare hit ratio](https://www.cloudflare.com/ko-kr/learning/cdn/what-is-a-cache-hit-ratio/) , [aws CF](https://docs.aws.amazon.com/ko_kr/AmazonCloudFront/latest/DeveloperGuide/cache-hit-ratio.html)

#### 인덱스를 어떻게 활용하셨고, 문제점이나 사용하면서 느낀 장단점이 무엇인지 궁금합니다.

- 초기에는 잦은 인덱스 생성과 변경으로 인한 성능 저하와 관리 복잡성을 경험

#### 트랜잭션에 대해 간단하게 설명해주세요.

- ACID 특성을 가지며, 데이터 무결성을 보장

#### NoSQL과 RDBMS의 차이점과 사용 경험을 말씀해주세요.

- 웹 서비스에 MySQL을 사용. 유저 로그 등은 MongoDB를 사용

### Git

#### Git이나 Github를 활용한 경험을 말씀해주세요.

- GitOps로 협업, 코드 관리, 배포에서 팀의 효율성 향상과 스트레스 감소를 경험

#### 코드 리뷰 경험이 있으신가요? 주의할 점이나 팁이 있다면 공유해주세요.

- 추상적인 피드백보다는 구체적인 방향이나 의견을 제시하고, 큰 작업을 작은 단위로 나누어 관리

#### Rebase와 Revert의 차이점은 무엇이고, 사용해 본 경험이 있나요?

- [git](https://geekflare.com/dev/git-reset-vs-revert-vs-rebase/)
- [options](https://stackoverflow.com/questions/3528245/whats-the-difference-between-git-reset-mixed-soft-and-hard)

### Server (AWS)

#### 트래픽이 증가하며 발생했던 문제나 서버 최적화 경험이 있으신가요?

- 최초에는 서버 사양 업그레이드로 대응. 쿼리 최적화, 캐싱 등을 활용하고 CDN을 도입하고 로드밸런서와 오토스케일링 등을 설정

#### 서버 모니터링은 어떻게 하셨나요?

- AWS CloudWatch나 Laravel log를 사용하여 slack으로 알림을 받고, 로그는 NoSQL에 저장하고 분석

#### Kafka나 Pub/Sub에 대해 알고 계신가요?

- 토픽, 파티션, 컨슈머 등의 개념을 확인
- [kafka](https://cloud.google.com/learn/what-is-apache-kafka?hl=ko) , [kafka 활용](https://techblog.woowahan.com/17386/)
- [pubsub](https://cloud.google.com/pubsub/docs/overview?hl=ko) , [kakao pubsub](https://docs.kakaocloud.com/service/analytics/pub-sub/pub-sub-overview)

#### AWS의 어떤 서비스들을 사용해 보셨나요?

#### Elastic Beanstalk과 Lightsail의 차이점을 설명해주세요.

- [Lightsail](https://youtu.be/WODr_GPLoFI)은 소규모 프로젝트를 위한 간단한 클라우드 서버 환경 제공
- [EB](https://youtu.be/AfRnvsRxZ_0)는 애플리케이션 배포 자동화, 스케일링 및 로드밸런싱 지원

#### Elastic Beanstalk 배포 방법이나 과정을 설명해주세요.

- GitHub Actions 설정. 코드가 업데이트되면 Docker 이미지를 빌드하고 ECR에 업로드 후 EB에 배포 (필요 시, 직접 EB CLI를 사용하여 배포)

#### 개발 환경 설정이나 배포를 어떻게 진행했는지 말씀해주세요.

- docker, docker-compose와 Laravel Sail 사용
- [docker&container](https://aws.amazon.com/ko/compare/the-difference-between-docker-images-and-containers/)

#### VPC 설정은 어떻게 하셨나요?

- 퍼블릭 서브넷에 ALB 및 NAT Gateway 설정, 프라이빗 서브넷에 RDS 및 내부 서비스 배치
- [NAT](https://docs.aws.amazon.com/ko_kr/vpc/latest/userguide/vpc-nat-comparison.html) , [VPC](https://docs.aws.amazon.com/ko_kr/vpc/latest/userguide/vpc-example-private-subnets-nat.html)
- [LB](https://aws.amazon.com/ko/compare/the-difference-between-the-difference-between-application-network-and-gateway-load-balancing/) , [VPC에서 EB 사용](https://docs.aws.amazon.com/ko_kr/elasticbeanstalk/latest/dg/vpc.html)

#### CI/CD 경험과 본인 만의 노하우가 있다면 공유해주세요.

- GitOps를 지향하며, GitHub Actions로 코드 관리(스캔 및 린트), 테스트, 배포 자동화 설정
- 배포 시, 점진적으로 전환하여 오류에 빠르게 대응하는 등 안정적인 배포를 지향

## 기타

#### 객체지향 프로그래밍과 객체라는 개념에 대해 설명해주세요.

- [OOP란...](https://www.inflearn.com/community/questions/868112/oop-%EB%9E%80-%EB%AC%B4%EC%97%87%EC%9D%B8%EA%B0%80%EC%9A%94?focusComment=265243)

#### 추상화란 무엇이라고 생각하고, 어떤 의미가 있나요?

#### 본인이 생각하는 이상적인 디자인 패턴과 이유를 설명해주세요.
