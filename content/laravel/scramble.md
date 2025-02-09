Title: Scramble
Subtitle: Laravel OpenAPI Documentation Generator
Category: laravel
Date: 2024-04-02 00:00
Tags: scramble, openapi, swagger

OpenAPI(Swagger) 문서를 작성하기 위해, [L5-Swagger](https://github.com/DarkaOnLine/L5-Swagger){:target="_blank"}나
[swagger-php](https://github.com/zircote/swagger-php){:target="_blank"} 등 다양한 패키지를 시도하고 사용했었는데,
Scramble은 다른 패키지들과는 다르게 다른 주석이나 문서를 작성할 필요 없이 API 문서를 자동으로 생성해 준다.

작년 [라라벨 뉴스](https://laravel-news.com/scramble-laravel-api-docs){:target="_blank"}에서 소개된 이후로 관심이 있어서
최근에 [업데이트된 버전](https://scramble.dedoc.co/blog/scrambledrop-scramble-0100){:target="_blank"}을 확인하고 사용해보았다.

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

```shell
composer require dedoc/scramble

php artisan vendor:publish --provider="Dedoc\Scramble\ScrambleServiceProvider" --tag="scramble-config"
```

### 설정

사용을 위해 몇 가지 설정 `config/scramble.php`을 변경하고,
개발이나 스테이징 서버에서도 문서를 확인할 수 있도록 `AppServiceProvider`에서 Gate를 설정한다.

```php
// config/scramble.php
use Dedoc\Scramble\Http\Middleware\RestrictedDocsAccess;

return [
    'api_path' => 'api',
    'api_domain' => str_replace('http://', '', env('APP_URL')),
    'export_path' => 'api.json',
    'info' => [
        'version' => env('API_VERSION', '0.0.1'),
        'description' => '해당 API나 서비스에 대한 설명 작성',
    ],
```

```php
// app/Providers/AppServiceProvider.php

use App\Models\User;
use Illuminate\Support\Facades\Gate;
use Illuminate\Support\ServiceProvider;

class AppServiceProvider extends ServiceProvider
{
    public function boot(): void
    {
        Gate::define('viewApiDocs', function (User $user) {
            return $user->email === 'admin@app.com';
        });
    }
```

## 사용

추가 설정을 하지 않았더라도, `/docs/api`로 접속하여 확인할 수 있다.

- `/docs/api` : API 문서 뷰어
- `/docs/api.json` : JSON 형식 API 문서

### 확인

- 리소스에 대한 모델을 찾을 수 없는 경우(ex. @mixin), 모든 필드는 `string` 타입으로 표시
- [How it works](https://scramble.dedoc.co/developers/how-it-works){:target="_blank"}
    - Scramble의 작동 원리를 순서대로 정리
    - Gathering API routes : 라우트와 해당 컨트롤러를 분석하여 엔드포인트, Request와 Response를 확인
    - Route to request documentation : Request를 문서화하기 위해, Validate(FormRequest)와 파라미터를 확인
    - Route’s responses documentation :
        - Response를 문서화하기 위해, return type을 분석하고 성공 및 오류 응답을 확인
        - 다양한 시나리오 및 예외를 확인하여 문서화
    - Putting it all together : 분석한(수집된) 정보를 경로나 스키마를 알파벳 순으로 정렬하여, OpenAPI 문서로 변환 
