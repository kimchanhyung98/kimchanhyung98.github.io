Title: Laravel Blueprint
Subtitle: Laravel 개발자를 위한 코드 생성 도구
Category: laravel
Date: 2024-06-21 00:00
Tags: blueprint, code-generation

## [Blueprint](https://blueprint.laravelshift.com/){:target="_blank"}

반복적인 코드 작성이 번거로워 템플릿이나 보일러플레이트를 고려하고 작성했었는데  
간단한 yaml 파일을 작성하여 모델, 마이그레이션, 컨트롤러 코드 초안을 생성해주는 Blueprint 패키지를 알게 되었다.
프로젝트 초기에 기본적인 DB와 CRUD 구조를 빠르게 생성할 수 있어, 비즈니스 로직에 집중할 수 있게 도와준다.

### [Installation](https://blueprint.laravelshift.com/docs/installation/){:target="_blank"}

Blueprint와 Test Assertions 패키지를 설치하고, `.gitignore`에 `.blueprint` 디렉토리(로컬 캐시)를 추가한다.

```shell
composer require -W --dev laravel-shift/blueprint
composer require --dev jasonmccreary/laravel-test-assertions  # optional

echo '/.blueprint' >> .gitignore
```

### [Components](https://blueprint.laravelshift.com/docs/generating-components/){:target="_blank"}

- `blueprint:new` 명령어로 yaml 파일을 생성하고, 간단하게 모델과 컨트롤러를 정의한다.
- `blueprint:build` [명령어](https://blueprint.laravelshift.com/docs/available-commands/){:target="_blank"}로 코드를 생성하고,
  `blueprint:erase`으로 생성된 파일들을 제거할 수 있다.
- 커스텀을 위해 stub을 게시하려면 `blueprint:stubs` , 수정사항 추적이 필요하다면 `blueprint:trace` 명령어를 사용한다.

---

`blueprint:build` 명령어로 코드를 생성하고, 간단한 예시 파일을 작성해보자.

```shell

```yaml
# [draft.yaml]

models:
  Post:
    title: string:400
    content: longtext
    published_at: nullable timestamp

  Comment:
    content: longtext
    published_at: nullable timestamp

  # additional models...

controllers:
  Post:
    index:
      query: all
      render: post.index with:posts
    create:
      render: post.create
    store:
      validate: title, content
      save: post
      send: ReviewNotification to:post.author with:post
      dispatch: SyncMedia with:post
      fire: NewPost with:post
      flash: post.title
      redirect: post.index

  Comment:
    show:
      render: comment.show with:comment

```

### [Models](https://blueprint.laravelshift.com/docs/defining-models/){:target="_blank"}

#### 모델 정의하기

Blueprint에서는 YAML 파일을 사용하여 데이터베이스 모델을 정의할 수 있습니다. 모델 정의는 **models** 섹션에서 이루어지며, 각 모델의 필드와 속성을 명확하게 기술할 수 있습니다. 이를 통해 모델,
마이그레이션, 팩토리, 시더 등의 코드 초안을 자동으로 생성할 수 있습니다.

#### 모델 데이터 타입

Blueprint는 다양한 데이터 타입을 지원하여 모델 필드를 유연하게 정의할 수 있습니다. 데이터 타입을 정확하게 지정함으로써 데이터베이스 구조를 체계적으로 설계할 수 있습니다.

### 지원되는 주요 데이터 타입

- **기본 타입**
    - `string`: VARCHAR 타입. 기본 길이는 255이며, 길이를 지정할 수 있습니다.
    - `text`: TEXT 타입.
    - `integer`: INTEGER 타입.
    - `bigInteger`: BIGINT 타입.
    - `boolean`: BOOLEAN 타입.
    - `timestamp`: TIMESTAMP 타입.
    - `date`: DATE 타입.
    - `time`: TIME 타입.
    - `float`: FLOAT 타입.
    - `double`: DOUBLE 타입.
    - `decimal`: DECIMAL 타입.

- **특수 타입**
    - `uuid`: UUID 타입.
    - `json`: JSON 타입.
    - `enum`: ENUM 타입. 열거형 값을 정의할 수 있습니다.

#### 키와 인덱스 설정

Blueprint를 사용하면 모델의 키(Primary Key)와 인덱스(Index)를 손쉽게 정의할 수 있습니다. 키와 인덱스를 적절하게 설정함으로써 데이터베이스 성능을 최적화하고 데이터 무결성을 유지할 수
있습니다.

#### 주요 키 및 인덱스 유형

- **Primary Key (주 키)**: 테이블의 고유 식별자로 사용됩니다. 기본적으로 `id` 필드가 주 키로 설정됩니다.
- **Unique Key (고유 키)**: 특정 필드의 값이 고유하도록 제한합니다.
- **Indexes (인덱스)**: 검색 속도를 향상시키기 위해 필드에 인덱스를 추가합니다.

#### 모델 관계 설정

Blueprint는 모델 간의 관계를 명확하게 정의할 수 있는 다양한 관계 설정을 지원합니다. 관계를 설정함으로써 데이터 간의 연관성을 표현하고, 이를 기반으로 Eloquent 모델의 관계 메서드를 자동으로 생성할
수 있습니다.

#### 지원되는 주요 관계 유형

- **One To One**: 한 모델이 다른 모델과 일대일 관계를 가집니다.
- **One To Many**: 한 모델이 여러 모델과 일대다 관계를 가집니다.
- **Many To Many**: 여러 모델이 다수의 모델과 다대다 관계를 가집니다.
- **Has Many Through**: 중간 모델을 통해 간접적으로 관계를 설정합니다.
- **Polymorphic Relations**: 다양한 모델과의 다형적 관계를 설정합니다.

#### 모델 단축 표현

Blueprint는 모델 정의를 더욱 간결하게 작성할 수 있는 다양한 단축 표현(Shorthand)을 지원합니다. 단축 표현을 사용하면 코드의 가독성을 높이고, 더욱 간편하게 모델을 정의할 수 있습니다.

#### 주요 단축 표현

- **Field Shorthand**: 필드 타입과 옵션을 간단하게 표현할 수 있습니다.
- **Relationship Shorthand**: 관계를 짧은 문법으로 정의할 수 있습니다.
- **Method Chaining**: 여러 옵션을 체이닝 방식으로 연결할 수 있습니다.

#### 데이터베이스 시더 생성

Blueprint를 사용하면 초기 데이터베이스 시더(Database Seeders)를 간편하게 생성할 수 있습니다. 시더를 통해 테스트 데이터나 초기 데이터를 손쉽게 삽입할 수 있으며, 이를 통해 개발 및 테스트
과정에서 효율성을 높일 수 있습니다.

#### 시더 정의 방법

시더는 **seeders** 섹션에서 정의하며, 각 시더는 특정 모델에 대한 데이터를 생성하는 로직을 담고 있습니다. Faker 라이브러리를 활용하여 다양한 테스트 데이터를 자동으로 생성할 수 있습니다.


---


Blueprint는 Laravel 애플리케이션에서 코드 생성을 자동화할 수 있도록 도와주는 도구로,
YAML 기반의 draft 파일 하나로 모델 정의부터 데이터베이스 시더 생성까지 연관된 여러 작업을 한 번에 처리할 수 있습니다.

1. 모델 정의와 데이터 타입

Blueprint의 draft 파일 내에서는 models 섹션을 사용하여 여러 모델을 정의합니다.
각 모델은 StudlyCase의 단수형 이름을 사용하며, 모델 내 컬럼은 key: value 형식으로 정의됩니다.
여기서 value에는 Laravel에서 지원하는 다양한 데이터 타입이 포함되며,
예를 들어 string:400, decimal:8,2, enum:pending,successful,failed와 같이 콜론(:)을 이용해 길이나 정밀도 같은 속성을 지정할 수 있습니다.
또한, nullable, default, unique 등과 같은 수정자(modifiers)도 함께 사용할 수 있어 각 컬럼의 특성을 세밀하게 제어할 수 있습니다.

2. 키, 인덱스 및 외래키 설정

모델 내 컬럼 정의 시 index, unique, foreign 등의 수정자를 활용하면, 해당 컬럼에 자동으로 인덱스나 외래키 제약 조건을 부여할 수 있습니다.
예를 들어, user_id와 같은 컬럼명은 Laravel의 네이밍 규칙에 따라 자동으로 users 테이블의 id 컬럼과 연관되며,
필요시 복합 인덱스도 indexes 키를 통해 정의할 수 있습니다.

3. 모델 간 관계 설정

Blueprint는 모델 간 관계를 정의하기 위한 relationships 섹션을 제공하여,
belongsTo, hasOne, hasMany, belongsToMany와 같은 Laravel의 관계 메서드를 쉽게 구현할 수 있습니다.
기본적으로 외래키 컬럼(예: user_id)만 정의해도 자동으로 belongsTo 관계가 생성되지만, 추가적으로 명시적으로 관계를 지정할 수도 있습니다.
또한, 별칭(alias)이나 피벗 테이블 생성과 같은 고급 기능을 지원해 복잡한 관계 설정도 간편하게 처리됩니다.

4. 모델 Shorthands

개발자 편의를 위해 Blueprint는 각 모델에 대해 id, created_at, updated_at 컬럼을 암묵적으로 추가합니다.
필요에 따라 이 기본 컬럼들을 직접 정의하거나 비활성화할 수 있으며, softDeletes 또는 softDeletesTz 같은 shorthands를 사용하면
논리적 삭제 기능도 쉽게 구현할 수 있습니다.

5. 데이터베이스 시더 생성

draft 파일 내 seeders 섹션에 쉼표로 구분된 모델 이름을 나열하면, 해당 모델에 대한 데이터베이스 시더가 자동으로 생성됩니다.
이 시더는 모델 팩토리를 활용하여 기본적으로 몇 개의 레코드를 생성하도록 구성되므로, 초기 데이터 설정을 빠르게 진행할 수 있습니다.

요약
Blueprint를 사용하면 한 YAML 파일 내에서 모델의 컬럼 정의, 데이터 타입 및 수정자 지정, 키/인덱스와 외래키 설정, 모델 간 관계 설정,
그리고 기본 컬럼 및 시더 생성까지 모든 과정을 한 번에 관리할 수 있습니다.
이를 통해 Laravel 애플리케이션 개발의 반복 작업을 줄이고, 코드 생성 과정을 효율적으로 자동화할 수 있습니다.

### [Controllers](https://blueprint.laravelshift.com/docs/defining-controllers/){:target="_blank"}

1. 컨트롤러 정의 및 기본 설정
   컨트롤러는 draft 파일의 controllers 섹션에서 정의합니다.

- 리소스 컨트롤러: 단 한 줄의 설정(예: resource: Post)으로 RESTful 메서드(index, create, store, show, edit, update, destroy)를 자동 생성할 수
  있습니다.
- 커스텀 액션: 단순히 메서드 이름과 해당 동작(예: view 반환, 리다이렉션, 데이터 유효성 검사 등)을 지정하여 원하는 로직을 추가할 수도 있습니다.

2. 컨트롤러 내의 명령어(Statements)
   Blueprint는 컨트롤러 메서드 내부에 작성될 **명령어(statement)**를 정의할 수 있는 DSL을 제공합니다.

- 각 명령어는 컨트롤러 액션 내에서 수행할 구체적 동작을 지정합니다.
- 예를 들어, 뷰를 반환하거나, 리다이렉션을 수행하거나, 요청 데이터를 검증하는 등의 작업을 간단한 구문으로 기술할 수 있습니다.
  이러한 명령어를 통해 생성된 컨트롤러 메서드는 Laravel의 관례에 맞게 작성됩니다.

3. 모델 참조(Model References)와의 연계
   컨트롤러에서 모델을 참조하는 방식도 Blueprint에 내장되어 있습니다.

- 자동 의존성 주입: 컨트롤러 내에서 모델 이름을 직접 언급하면, Blueprint가 해당 모델의 인스턴스를 라우트 모델 바인딩과 함께 자동으로 주입하도록 코드를 생성합니다.
- 이를 통해 컨트롤러 메서드가 보다 깔끔하게 작성되고, 모델 관련 작업이 단순해집니다.

4. 컨트롤러 Shorthands (약식 표기법)
   개발자 편의성을 위해 Blueprint는 컨트롤러 생성에 대한 다양한 단축 구문을 제공합니다.

- 리소스 및 단일 액션: 간단한 표기법을 사용해 전체 리소스 컨트롤러나 단일 액션(Invokable) 컨트롤러를 빠르게 스캐폴딩할 수 있습니다.
- 이러한 shorthands는 기본 CRUD 메서드 외에도 필요에 따라 커스터마이징 할 수 있는 틀을 제공합니다.

5. 생성된 테스트 코드
   Blueprint는 컨트롤러 코드와 함께 기본적인 테스트 코드도 자동 생성합니다.

- 테스트 생성: 컨트롤러에 정의된 액션에 따라, 각 메서드가 올바르게 작동하는지 확인하는 PHPUnit 기반의 테스트 케이스를 생성합니다.
- 이를 통해 초기 개발 시 자동화된 테스트 환경을 쉽게 갖출 수 있어, 코드 품질 관리에 도움을 줍니다.

종합 정리
Blueprint의 컨트롤러 관련 기능은 다음과 같이 통합되어 있습니다.

- 정의 및 생성: YAML 파일의 controllers 섹션에서 컨트롤러를 정의하고, 리소스 컨트롤러나 커스텀 액션을 설정할 수 있습니다.
- 명령어(Statements): 각 액션 내에서 수행할 로직을 간단한 DSL 문법으로 기술해 자동으로 코드로 변환합니다.
- 모델과의 연계: 컨트롤러에서 모델 참조를 통해 자동 의존성 주입과 라우트 모델 바인딩을 활용, 코드를 간결하게 만듭니다.
- Shorthands: 단축 표기법을 통해 빠르고 효율적으로 컨트롤러를 스캐폴딩하며, Invokable 등 다양한 형태를 지원합니다.
- 자동 테스트: 생성된 컨트롤러 코드에 맞춰 기본적인 테스트 케이스를 자동으로 만들어, 초기 개발 환경에서 검증을 쉽게 수행할 수 있도록 합니다.

---

- 키와 인덱스
  foreign 속성 설정

user_id: id foreign
owner_id: id foreign:users
uid: id foreign:users.id

복합 인덱싱도 지원함

User:
indexes:

- unique: owner_id, badge_number

- 관계

models:
Post:
title: string:400
published_at: timestamp nullable
relationships:
hasMany: Comment
belongsToMany: Media, Site
belongsTo: \Spatie\LaravelPermission\Models\Role

애플리케이션의 일부가 아닌 모델을 지정하려면 정규화된 클래스 이름을 제공할 수 있습니다.
반드시 초기 \(백슬래시)를 포함해야 합니다. 예를 들어, \Spatie\LaravelPermission\Models\Role.

models:
Post:
relationships:
hasMany: Comment:reply

별칭 복수형으로 자동 변환함

중간 모델
https://laravel.com/docs/11.x/eloquent-relationships#defining-custom-intermediate-table-models
User:
relationships:
belongsToMany: Team:&Membership

- 속기
  약어 제공, 모든 모델에 자동으로 id, timestamps를 추가한다.
  비활성화하려면 timestamps: false로 설정한다. 타임존이 필요하다면 timestampsTz

카멜케이스와 소문자 등 주의

models:
Widget:
id: id
deleted_at: timestamp
created_at: timestamp
updated_at: timestamp

models:
Widget:
softDeletes

컨트롤러 statements

dispatch: SyncMedia with:post
fire: NewPost with:post
notify: post.author ReviewPost with:post
notify: user AccountAlert
query: where:title where:content order:published_at limit:5
redirect: post.show with:post
render: post.show with:post,foo,bar
resource: user
resource: paginate:users # https://laravel.com/docs/11.x/eloquent-resources
respond: post.show with:post
send: ReviewPost to:post.author with:post
store: post.title
update: post
update: title, content, author_id
validate: post
validate: title, content, author_id

모델 참조
https://blueprint.laravelshift.com/docs/model-references/

controllers:
Post:
index:
query: all
render: post.index with:posts
create:
find: user.id
render: post.create with:user
store:
validate: title, published_at
save: post
redirect: post.show
show:
query: all:comments
render: post.show with:post,comments

리소스 컨트롤러
https://blueprint.laravelshift.com/docs/controller-shorthands/#resource-shorthand

controllers:
Post:
index:
query: all:posts
render: post.index with:posts
create:
render: post.create
store:
validate: post
save: post
flash: post.id
redirect: post.index
show:
render: post.show with:post
edit:
render: post.edit with:post
update:
validate: post
update: post
flash: post.id
redirect: post.index
destroy:
delete: post
redirect: post.index

controllers:
Post:
resource

# generate only index and show actions

resource: index, show

# generate only store and update API actions

resource: api.store, api.update

# generate "web" index and API destroy actions

resource: index, api.destroy

controllers:
Post:
resource: all
download:
find: post.id
respond: post
show:
query: comments where:post.id
render: post.show with:post,comments

Invokable Shorthand

controllers:
Report:
invokable

controllers:
Report:
__invoke:
render: report

controllers:
Report:
invokable:
fire: ReportGenerated
render: report

### etc

- [drawSQL](https://drawsql.app){:target="_blank"} : draft.yaml 파일을 시각화하여 ERD를 생성할 수 있다.
- [Building Blueprint - v1.0, Quick Demo](https://youtu.be/A_gUCwni_6c){:target="_blank"}
- [Rapid Code Generation With Blueprint, Laracasts](https://laracasts.com/series/guest-spotlight/episodes/9){:target="_
  blank"}
- [Create Models with Blueprint, Laracasts](https://laracasts.com/series/rapid-laravel-development-with-filament/episodes/1){:
  target="_blank"}
