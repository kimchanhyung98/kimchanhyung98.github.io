Title: Laravel lifecycle
Subtitle: Laravel lifecycle 문서 확인
Category: laravel
Date: 2024-05-01 00:00

### What happened?

토이프로젝트를 진행하는 중 프론트 개발자가 실수로 Body와 Param을 둘 다 전달했다.  
Body, Param 모두 동일하게 입력을 받을 텐데 Laravel이 어떤 값을 어디서 먼저 처리하는지가 궁금하여, 프레임워크의 동작 방식을 알아보고 Illuminate/Http/Request를 자세히 확인해 보았다.

## [Request Lifecycle](https://laravel.com/docs/master/lifecycle)

어떤 도구를 사용할 때, 그 도구의 동작 방식을 이해하면 더 효율적으로 사용할 수 있는 것 처럼  
애플리케이션 개발도 마찬가지로, Laravel 프레임워크의 내부 동작 방식을 이해하고 Request 처리 과정을 확인하면     
프레임워크를 사용하는데 더 편리하고, 빠르게 개발할 수 있을 것이다. (아마도...)

### index.php

1. 웹 서버(Nginx, Apache) 구성에 따라, 모든 요청([Request](https://laravel.com/api/master/Illuminate/Http/Request.html))은 진입점인
   `public/index.php` 파일로 전달된다.
2. `index.php` 파일은 Composer가 생성한 `autoload.php`를 로드한다.
3. `bootstrap/app.php`에서 Laravel 애플리케이션의 인스턴스를 가져와서,
   애플리케이션/서비스 [컨테이너](https://laravel.com/docs/11.x/container)의 인스턴스를 생성하여 작업을 시작한다. (Laravel이 처음 수행하는 작업)

```php
[public/index.php]

// Register the Composer autoloader...
require __DIR__.'/../vendor/autoload.php';

// Bootstrap Laravel and handle the request...
(require_once __DIR__.'/../bootstrap/app.php')
    ->handleRequest(Request::capture()); 
```

```php
[Illuminate/Foundation/Application.php]

/**
 * Handle the incoming HTTP request and send the response to the browser.
 *
 * @param  \Illuminate\Http\Request  $request
 * @return void
 */
public function handleRequest(Request $request)
{
    $kernel = $this->make(HttpKernelContract::class);
    $response = $kernel->handle($request)->send();
    $kernel->terminate($request, $response);
}
```

- `handleRequest` 메소드로 요청을 HTTP Kernel로 전달한다.
    - `handleCommand`을 이용하여 Console Kernel로 전달할 수도 있다.

### HTTP / Console Kernels

커널의 handle 메소드는 Request를 받아서 Response를 반환하는 간단한 구조이다.

- 들어오는 Request는 HTTP 커널로 전송한다.
- 커널은 Request가 실행되기 전에 필요한 설정을 수행하는 부트스트래퍼를 실행하고, 미들웨어 스택을 통해 Request를 전달한다.
- 미들웨어는 HTTP [세션](https://laravel.com/docs/11.x/session)을 읽고 쓰고, CSRF 토큰을 검증하는 등 작업을 처리한다.

```php
[Illuminate\Foundation\Http\Kernel.php]

/**
 * Handle an incoming HTTP request.
 *
 * @param  \Illuminate\Http\Request  $request
 * @return \Illuminate\Http\Response
 */
public function handle($request)
{
    $this->requestStartedAt = Carbon::now();

    try {
        $request->enableHttpMethodParameterOverride();
        $response = $this->sendRequestThroughRouter($request);
    } catch (Throwable $e) {
        $this->reportException($e);
        $response = $this->renderException($request, $e);
    }

    $this->app['events']->dispatch(
        new RequestHandled($request, $response)
    );

    return $response;
}
```

### Service Provider

다양한 구성 요소(데이터베이스, 큐, 검증, 라우팅 등)를 부트스트래핑하고 구성하는 역할이다.

- Laravel은 이 [프로바이더](https://laravel.com/docs/11.x/providers) 목록을 반복하면서 각각의 프로바이더를 인스턴스화한다.
- 모든 프로바이더에서 register 메소드가 호출되고, 등록된 후, boot 메소드가 호출된다. 이 과정에서 모든 주요 기능이 초기화된다.
    - 사용자 정의 서비스 프로바이더 생성은 bootstrap/providers.php

```php
[Illuminate/Foundation/Application.php]

/**
 * Begin configuring a new Laravel application instance.
 *
 * @param  string|null  $basePath
 * @return \Illuminate\Foundation\Configuration\ApplicationBuilder
 */
public static function configure(?string $basePath = null)
{
    $basePath = match (true) {
        is_string($basePath) => $basePath,
        default => static::inferBasePath(),
    };

    return (new Configuration\ApplicationBuilder(new static($basePath)))
        ->withKernels()
        ->withEvents()
        ->withCommands()
        ->withProviders();
}
```

```php
[Illuminate/Foundation/Configuration/ApplicationBuilder.php]

/**
 * Register additional service providers.
 *
 * @param  array  $providers
 * @param  bool  $withBootstrapProviders
 * @return $this
 */
public function withProviders(array $providers = [], bool $withBootstrapProviders = true)
{
    RegisterProviders::merge(
        $providers,
        $withBootstrapProviders
            ? $this->app->getBootstrapProvidersPath()
            : null
    );

    return $this;
}
```

```php
[Illuminate/Foundation/Application.php]

/**
 * Get the path to the bootstrap directory.
 *
 * @param  string  $path
 * @return string
 */
public function bootstrapPath($path = '')
{
    return $this->joinPaths($this->bootstrapPath, $path);
}

/**
 * Get the path to the service provider list in the bootstrap directory.
 *
 * @return string
 */
public function getBootstrapProvidersPath()
{
    return $this->bootstrapPath('providers.php');
}
```

```php
[Illuminate/Filesystem/functions.php]

/**
 * Join the given paths together.
 *
 * @param  string|null  $basePath
 * @param  string  ...$paths
 * @return string
 */
function join_paths($basePath, ...$paths)
{
    foreach ($paths as $index => $path) {
        if (empty($path) && $path !== '0') {
            unset($paths[$index]);
        } else {
            $paths[$index] = DIRECTORY_SEPARATOR.ltrim($path, DIRECTORY_SEPARATOR);
        }
    }

    return $basePath.implode('', $paths);
}
```

### Focus on Service Providers

서비스 프로바이더는 Laravel 애플리케이션 부트스트래핑의 핵심이다.

- 사용자 정의 서비스 프로바이더는 `app/Providers` 디렉토리에 저장되고, 부트스트래핑 및 서비스 컨테이너 바인딩을 추가하는 데 사용된다.

### Routing

요청이 미들웨어를 통과하면, 라우트 또는 컨트롤러 메서드가 실행되고 응답(response)이 반환된다.

- 애플리케이션이 부트스트래핑되고 모든 서비스 프로바이더가 등록된 후, 라우터는 요청(Request)을 처리하여 적절한 라우트나 컨트롤러에 전달한다.
- [미들웨어](https://laravel.com/docs/11.x/middleware)는 Request를 필터링하거나 검사하는 역할을 하며, 인증, 유지보수 모드 확인 등의 기능을 수행한다.

### Finishing Up

컨트롤러(혹은 라우트)가 반환한 응답(Response)은 다시 미들웨어를 통해 전달, 애플리케이션이 Response를 수정할 수 있는 기회를 준다.  
마지막으로, HTTP 커널은 Response를 애플리케이션 인스턴스에 반환하고 `send` 메서드를 호출하여 Response를 사용자에게 전송한다.

- [laravel-request-lifecycle](https://medium.com/@ankitatejani84/laravel-request-lifecycle-7c2145aa1257), [learning-the-lifecycle-of-laravel](https://medium.com/@nisma.hossain.41982/learning-the-lifecycle-of-laravel-4e674e176d34)
