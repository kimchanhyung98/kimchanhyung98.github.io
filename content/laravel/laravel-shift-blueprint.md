Title: Blueprint
Subtitle: Code generation for Laravel developers
Category: laravel
Date: 2024-02-01 00:00

## [Blueprint](https://blueprint.laravelshift.com/)

반복적인 코드 작성이 번거로워 템플릿이나 보일러플레이트를 고려하고 작성했었는데  
간단한 yaml 파일을 작성하여 모델, 마이그레이션, 컨트롤러 코드 초안을 생성해주는 Blueprint를 알게 되었다.
프로젝트 초기에 기본적인 DB와 CRUD 구조를 빠르게 생성할 수 있어, 비즈니스 로직에 집중할 수 있게 도와준다.

### [Installation](https://blueprint.laravelshift.com/docs/installation/)

Blueprint와 Test Assertions 패키지를 설치하고, `.gitignore`에 `.blueprint` 디렉토리(로컬 캐시)를 추가한다.

```shell
composer require -W --dev laravel-shift/blueprint

composer require --dev jasonmccreary/laravel-test-assertions

# echo '/draft.yaml' >> .gitignore
echo '/.blueprint' >> .gitignore
```

### [Components](https://blueprint.laravelshift.com/docs/generating-components/)

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

- `blueprint:new` 명령어로 yaml 파일을 생성하고, 간단하게 모델과 컨트롤러를 정의한다.
- `blueprint:build` [명령어](https://blueprint.laravelshift.com/docs/available-commands/)로 코드를 생성하고
  `blueprint:erase`으로 생성된 파일들을 제거할 수 있다.
- 커스텀을 위해 stub을 게시하려면 `blueprint:stubs` , 수정사항 추적이 필요하다면 `blueprint:trace` 명령어를 사용한다.

### [Models](https://blueprint.laravelshift.com/docs/defining-models/)

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

### [Controllers](https://blueprint.laravelshift.com/docs/defining-controllers/)

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

- [drawSQL](https://drawsql.app) : draft.yaml 파일을 시각화하여 ERD를 생성할 수 있다.
- [Building Blueprint - v1.0, Quick Demo](https://youtu.be/A_gUCwni_6c)
- [Rapid Code Generation With Blueprint, Laracasts](https://laracasts.com/series/guest-spotlight/episodes/9)
- [Create Models with Blueprint, Laracasts](https://laracasts.com/series/rapid-laravel-development-with-filament/episodes/1)
