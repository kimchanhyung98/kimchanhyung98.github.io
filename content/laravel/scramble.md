Title: Scramble
Subtitle: Laravel OpenAPI(Swagger) Documentation Generator
Category: laravel
Date: 2024-09-05 00:00

OpenAPI(Swagger) 문서를 작성하기 위해, 다양한 패키지를 사용했었다.

- [DarkaOnLine/L5-Swagger](https://github.com/DarkaOnLine/L5-Swagger)
- [zircote/swagger-php](https://github.com/zircote/swagger-php)
- [vyuldashev/laravel-openapi](https://github.com/vyuldashev/laravel-openapi)

하지만, 직접 코드(주석이나 어노테이션)를 작성해야 하는 번거로움이 있었다.  
별도의 스웨거 파일 정의없이 자동으로 문서를 생성하는 방법을 찾던 중, [Scramble](https://scramble.dedoc.co/)을 발견했다.

- [Scramble](https://scramble.dedoc.co)
- [laravel-news](https://laravel-news.com/scramble-laravel-api-docs)

## 설치

Require

- php : ^8.1
- laravel : ^10.x

```php
composer require dedoc/scramble
php artisan vendor:publish --provider="Dedoc\Scramble\ScrambleServiceProvider" --tag="scramble-config"
```

### 설정

사용을 위해 몇가지 설정 `config/scramble.php` 을 변경한다.

![scramble config]({static}/images/laravel-scramble-config.png)

개발이나 스테이징 서버에서도 문서를 확인할 수 있도록 Gate를 설정한다.

![scramble gate]({static}/images/laravel-scramble-gate.png)

## 사용

- `/docs/api` : API 문서 뷰어
- `/docs/api.json` : JSON 형식 API 문서

