Title: Scramble
Subtitle: Laravel OpenAPI Documentation Generator
Category: laravel
Date: 2024-04-02 00:00

OpenAPI(Swagger) 문서를 작성하기 위해, [L5-Swagger](https://github.com/DarkaOnLine/L5-Swagger)나
[swagger-php](https://github.com/zircote/swagger-php) 등 다양한 패키지를 시도하고 사용했었는데,
Scramble은 다른 패키지들과는 다르게 다른 주석이나 문서를 작성할 필요 없이 API 문서를 자동으로 생성해 준다.

작년 [라라벨 뉴스](https://laravel-news.com/scramble-laravel-api-docs)에서 소개된 이후로 관심이 있어서
최근에 [업데이트된 버전](https://scramble.dedoc.co/blog/scrambledrop-scramble-0100)을 확인하고 사용해보았다.

<details>
<summary>#scrambledrop: Scramble 0.10.0</summary>
<ul>
    <li>문서 URL 사용자 정의 : 문서 도메인 및 경로 커스터마이즈 가능</li>
    <li>다중 API 버전 문서 지원 : 여러 버전의 문서를 등록하고 각각 다른 경로로 제공</li>  
    <li>요청 매개변수 예시 및 기본값 설정 : 요청 매개변수에 예시 및 기본값 제공</li>
    <li>Sanctum 통합 개선 : Sanctum 쿠키 기반 API와 통합</li>
    <li>Tuple 및 Enum 지원 : 문서화에서 튜플과 enum 지원</li>
    <li>기타 개선 사항 : 204 응답 문서화, 유효성 검사 규칙 개선 등</li>
</ul>
</details>

### 설치

Require

- php : ^8.1
- laravel : ^10.x

```php
composer require dedoc/scramble

php artisan vendor:publish --provider="Dedoc\Scramble\ScrambleServiceProvider" --tag="scramble-config"
```

### 설정

사용을 위해 몇 가지 설정 `config/scramble.php`을 변경하고,
개발이나 스테이징 서버에서도 문서를 확인할 수 있도록 `AppServiceProvider`에서 Gate를 설정한다.

![scramble config]({static}/images/laravel-scramble-config.png)
![scramble gate]({static}/images/laravel-scramble-gate.png)

## 사용

추가 설정을 하지 않았더라도, `/docs/api`로 접속하여 확인할 수 있다.

- `/docs/api` : API 문서 뷰어
- `/docs/api.json` : JSON 형식 API 문서

### 확인

- 리소스에 대한 모델을 찾을 수 없는 경우(ex. @mixin), 모든 필드는 `string` 타입으로 표시
- [작동 원리](https://scramble.dedoc.co/developers/how-it-works)
