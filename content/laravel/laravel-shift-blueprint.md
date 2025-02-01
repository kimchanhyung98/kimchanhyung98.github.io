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

`blueprint:new` 명령어로 yaml 파일을 생성하고, 간단하게 모델과 컨트롤러를 정의한다.

```shell

```yaml
# [draft.yaml]

models:
  Post:
    title: string:400
    content: longtext
    published_at: nullable timestamp

controllers:
  Post:
    index:
      query: all
      render: post.index with:posts

    store:
      validate: title, content
      save: post
      send: ReviewNotification to:post.author with:post
      dispatch: SyncMedia with:post
      fire: NewPost with:post
      flash: post.title
      redirect: post.index
```

- `blueprint:build` [명령어](https://blueprint.laravelshift.com/docs/available-commands/)로 코드를 생성하고
  `blueprint:erase`으로 생성된 파일들을 제거할 수 있다.
- 커스텀을 위해 stub을 게시하려면 `blueprint:stubs` , 수정사항 추적이 필요하다면 `blueprint:trace` 명령어를 사용한다.

### [Models](https://blueprint.laravelshift.com/docs/defining-models/)

### [Controllers](https://blueprint.laravelshift.com/docs/defining-controllers/)

### etc

- [drawSQL](https://drawsql.app) : draft.yaml 파일을 시각화하여 ERD를 생성할 수 있다.
- [Building Blueprint - v1.0, Quick Demo](https://youtu.be/A_gUCwni_6c)
- [Rapid Code Generation With Blueprint, Laracasts](https://laracasts.com/series/guest-spotlight/episodes/9)
- [Create Models with Blueprint, Laracasts](https://laracasts.com/series/rapid-laravel-development-with-filament/episodes/1)
