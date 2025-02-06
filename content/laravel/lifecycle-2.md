Title: Laravel HTTP Request
Subtitle: Illuminate/Http/Request 확인하기
Category: laravel
Date: 2024-05-02 00:00

## Details

[Lifecycle](https://chanhyung.kim/w/laravel-lifecycle)을 확인해 보았으나, Request 클래스에 대한 자세한 내용은 없다.  
'Illuminate\Http\Request 인스턴스는 애플리케이션에 유입되는 HTTP 요청을 검사하기 위해,
다양한 메소드를 제공하고 Symfony\Component\HttpFoundation\Request 클래스를 상속한다'는 정도.

- API 문서를 확인하면 docs보다는 자세하게 Request 클래스의 메소드와 속성을 확인할 수 있고, View source를 통해 코드를 확인할 수 있다.
    - [laravel api](https://laravel.com/api/master/Illuminate/Http/Request.html)
- 프로젝트를 진행한다면 실제 경로는 vendor/laravel/framework/src/Illuminate/Http/Request.php

### [Source](https://github.com/laravel/framework/blob/master/src/Illuminate/Http/Request.php)

```http
POST http://localhost/test-api?name=테스트1&nickname=tester1&email=tester1@example.com&password=Password1!@
Content-Type: application/json

{
  "name": "테스트2",
  "nickname": "tester2",
  "email": "tester2@example.com",
  "password": "Password2@#"
}
```

관련 코드를 순서대로 확인해보고, 임의의 입력과 로그를 추가하여 Request 처리 과정을 확인해보자.

```php
[public/index.php]

// Bootstrap Laravel and handle the request...
(require_once __DIR__.'/../bootstrap/app.php')
    ->handleRequest(Request::capture());
```

<!-- trace: public/index.php (here) → Illuminate/Http/Request.php : capture() -->
이전에 확인했던 라라벨의 라이프 사이클을 토대로, public/index.php에서 Request capture로 연결되는 것을 확인  

```php
[Illuminate/Http/Request.php]

/**
 * Create a new Illuminate HTTP request from server variables.
 *
 * @return static
 */
public static function capture()
{
    static::enableHttpMethodParameterOverride();

    return static::createFromBase(SymfonyRequest::createFromGlobals());
}
```

<!-- trace: Illuminate/Http/Request.php (here) → symfony/http-foundation/Request.php : enableHttpMethodParameterOverride() -->
<!-- trace: Illuminate/Http/Request.php (here) → symfony/http-foundation/Request.php : createFromGlobals() -->
<!-- trace: Illuminate/Http/Request.php (here) → symfony/http-foundation/Request.php : createFromBase() -->

```php
[symfony/http-foundation/Request.php]

/**
 * 의도된 HTTP 메서드를 결정하기 위해 _method 요청 매개변수 지원을 활성화합니다.
 *
 * 이 기능을 활성화하면 코드에서 CSRF 문제가 발생할 수 있으므로 주의하세요.
 * 필요한 경우 CSRF 토큰을 사용하고 있는지 확인하세요.
 * HTTP 메서드 매개변수 재정의가 활성화된 경우, "POST" 메서드를 가진 HTML 폼이 수정되어
 * _method 요청 매개변수를 통해 "PUT" 또는 "DELETE" 요청을 보낼 수 있습니다.
 * 이러한 메서드가 CSRF에 대해 보호되지 않으면, 이는 잠재적인 취약점을 나타냅니다.
 *
 * 실제 HTTP 메서드가 POST일 때만 HTTP 메서드를 재정의할 수 있습니다.
 */
public static function enableHttpMethodParameterOverride(): void
{
    self::$httpMethodParameterOverride = true;
}
```

<!-- trace: Illuminate/Http/Request.php → symfony/http-foundation/Request.php : enableHttpMethodParameterOverride() (here) -->

```php
[symfony/http-foundation/Request.php]

/**
 * Creates a new request with values from PHP's super globals.
 */
public static function createFromGlobals(): static
{
    $request = self::createRequestFromFactory($_GET, $_POST, [], $_COOKIE, $_FILES, $_SERVER);

    if (str_starts_with($request->headers->get('CONTENT_TYPE', ''), 'application/x-www-form-urlencoded')
        && \in_array(strtoupper($request->server->get('REQUEST_METHOD', 'GET')), ['PUT', 'DELETE', 'PATCH'], true)
    ) {
        parse_str($request->getContent(), $data);
        $request->request = new InputBag($data);
    }

    // logger($request);

    return $request;
}
```

<!-- trace: Illuminate/Http/Request.php → symfony/http-foundation/Request.php : createFromGlobals() (here) -->
이어서 enableHttpMethodParameterOverride를 확인하고 SymfonyRequest의 createFromGlobals도 확인  

<details>
<summary>symfony/http-foundation/Request.php → dump createFromGlobals</summary>

```php
Symfony\Component\HttpFoundation\Request {#34
  +attributes: Symfony\Component\HttpFoundation\ParameterBag {#37
    #parameters: []
  }
  +request: Symfony\Component\HttpFoundation\InputBag {#35
    #parameters: []
  }
  +query: Symfony\Component\HttpFoundation\InputBag {#36
    #parameters: array:4 [
      "name" => "테스트1"
      "nickname" => "tester1"
      "email" => "tester1@example.com"
      "password" => "Password1!@"
    ]
  }
  +server: Symfony\Component\HttpFoundation\ServerBag {#40
    #parameters: array:27 [
      "DOCUMENT_ROOT" => "/var/www/html/public"
      "REMOTE_ADDR" => "192.168.1.1"
      "REMOTE_PORT" => "28274"
      "SERVER_SOFTWARE" => "PHP/8.3.7 (Development Server)"
      "SERVER_PROTOCOL" => "HTTP/1.1"
      "SERVER_NAME" => "0.0.0.0"
      "SERVER_PORT" => "80"
      "REQUEST_URI" => "/api/req-test?name=%ED%85%8C%EC%8A%A4%ED%8A%B81&nickname=tester1&email=tester1@example.com&password=Password1!@"
      "REQUEST_METHOD" => "POST"
      "SCRIPT_NAME" => "/index.php"
      "SCRIPT_FILENAME" => "/var/www/html/public/index.php"
      "PATH_INFO" => "/api/req-test"
      "PHP_SELF" => "/index.php/api/req-test"
      "QUERY_STRING" => "name=%ED%85%8C%EC%8A%A4%ED%8A%B81&nickname=tester1&email=tester1@example.com&password=Password1!@"
      "CONTENT_TYPE" => "application/json"
      "HTTP_CONTENT_TYPE" => "application/json"
      "HTTP_USER_AGENT" => "PostmanRuntime/7.40.0"
      "HTTP_ACCEPT" => "*/*"
      "HTTP_CACHE_CONTROL" => "no-cache"
      "HTTP_POSTMAN_TOKEN" => "12345678-0d36-4771-a9c7-1234567890"
      "HTTP_HOST" => "localhost"
      "HTTP_ACCEPT_ENCODING" => "gzip, deflate, br"
      "HTTP_CONNECTION" => "keep-alive"
      "CONTENT_LENGTH" => "122"
      "HTTP_CONTENT_LENGTH" => "122"
      "REQUEST_TIME_FLOAT" => 1234567890.1234
      "REQUEST_TIME" => 1234567890
    ]
  }
  +files: Symfony\Component\HttpFoundation\FileBag {#39
    #parameters: []
  }
  +cookies: Symfony\Component\HttpFoundation\InputBag {#38
    #parameters: []
  }
  +headers: Symfony\Component\HttpFoundation\HeaderBag {#41
    #headers: array:9 [
      "content-type" => array:1 [
        0 => "application/json"
      ]
      "user-agent" => array:1 [
        0 => "PostmanRuntime/7.40.0"
      ]
      "accept" => array:1 [
        0 => "*/*"
      ]
      "cache-control" => array:1 [
        0 => "no-cache"
      ]
      "postman-token" => array:1 [
        0 => "12345678-0d36-4771-a9c7-1234567890"
      ]
      "host" => array:1 [
        0 => "localhost"
      ]
      "accept-encoding" => array:1 [
        0 => "gzip, deflate, br"
      ]
      "connection" => array:1 [
        0 => "keep-alive"
      ]
      "content-length" => array:1 [
        0 => "122"
      ]
    ]
    #cacheControl: array:1 [
      "no-cache" => true
    ]
  }
  #content: null
  #languages: null
  #charsets: null
  #encodings: null
  #acceptableContentTypes: null
  #pathInfo: null
  #requestUri: null
  #baseUrl: null
  #basePath: null
  #method: null
  #format: null
  #session: null
  #locale: null
  #defaultLocale: "en"
  -preferredFormat: null
  -isHostValid: true
  -isForwardedValid: true
  -isSafeContentPreferred: ? bool
  -trustedValuesCache: []
  -isIisRewrite: false
  pathInfo: "/api/req-test"
  requestUri: "/api/req-test?name=%ED%85%8C%EC%8A%A4%ED%8A%B81&nickname=tester1&email=tester1@example.com&password=Password1!@"
  baseUrl: ""
  basePath: ""
  method: "POST"
  format: "html"
}
```

</details>  

```php
[Illuminate/Http/Request.php]

/**
 * Create an Illuminate request from a Symfony instance.
 *
 * @param  \Symfony\Component\HttpFoundation\Request  $request
 * @return static
 */
public static function createFromBase(SymfonyRequest $request)
{
    logger($request->request);  // 1st log
    
    $newRequest = new static(
        $request->query->all(), $request->request->all(), $request->attributes->all(),
        $request->cookies->all(), (new static)->filterFiles($request->files->all()) ?? [], $request->server->all()
    );

    $newRequest->headers->replace($request->headers->all());

    $newRequest->content = $request->content;

    if ($newRequest->isJson()) {
        $newRequest->request = $newRequest->json();
    }
    
    logger($newRequest);  // 2nd log
    
    return $newRequest;
}
```

<!-- trace: Illuminate/Http/Request.php → symfony/http-foundation/Request.php : createFromBase() (here) -->
capture → createFromBase를 거치면서 body가 추가되는 것을 확인  

<details>
<summary>Illuminate/Http/Request.php → dump 1st log</summary>

$request->request 는 빈값. form-data, x-www-form-urlencoded를 처리 후, json 처리

```php
Symfony\Component\HttpFoundation\InputBag {#35
	#parameters: []
}
```

</details>  

<details>
<summary>Illuminate/Http/Request.php → dump 2st log</summary>

Header content type이 json이면, $newRequest->request 오버라이딩

```php
[Illuminate/Http/Concerns/InteractsWithContentTypes.php]

/**
 * Determine if the request is sending JSON.
 *
 * @return bool
 */
public function isJson()
{
    return Str::contains($this->header('CONTENT_TYPE') ?? '', ['/json', '+json']);
}
```

</details>  

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
    // logger($request);
    
    $kernel = $this->make(HttpKernelContract::class);

    $response = $kernel->handle($request)->send();

    $kernel->terminate($request, $response);
}
```

Request::capture()가 생성한 Symfony\Component\HttpFoundation\Request 인스턴스를 handleRequest 메소드로 전달  
해당 값(request)을 전달받은 handleRequest는 body, param 값이 모두 있는 것도 확인  

<details>
<summary>Illuminate/Foundation/Application.php → dump handleRequest</summary>

```php
Illuminate\Http\Request {#42
  +attributes: Symfony\Component\HttpFoundation\ParameterBag {#47
    #parameters: []
  }
  +request: Symfony\Component\HttpFoundation\InputBag {#46
    #parameters: array:4 [
      "name" => "테스트2"
      "nickname" => "tester2"
      "email" => "tester2@example.com"
      "password" => "Password2@#"
    ]
  }
  +query: Symfony\Component\HttpFoundation\InputBag {#50
    #parameters: array:4 [
      "name" => "테스트1"
      "nickname" => "tester1"
      "email" => "tester1@example.com"
      "password" => "Password1!@"
    ]
  }
  +server: Symfony\Component\HttpFoundation\ServerBag {#45
    #parameters: array:27 [
      "DOCUMENT_ROOT" => "/var/www/html/public"
      "REMOTE_ADDR" => "192.168.65.1"
      "REMOTE_PORT" => "60089"
      "SERVER_SOFTWARE" => "PHP/8.3.7 (Development Server)"
      "SERVER_PROTOCOL" => "HTTP/1.1"
      "SERVER_NAME" => "0.0.0.0"
      "SERVER_PORT" => "80"
      "REQUEST_URI" => "/api/req-test?name=%ED%85%8C%EC%8A%A4%ED%8A%B81&nickname=tester1&email=tester1@example.com&password=Password1!@"
      "REQUEST_METHOD" => "POST"
      "SCRIPT_NAME" => "/index.php"
      "SCRIPT_FILENAME" => "/var/www/html/public/index.php"
      "PATH_INFO" => "/api/req-test"
      "PHP_SELF" => "/index.php/api/req-test"
      "QUERY_STRING" => "name=%ED%85%8C%EC%8A%A4%ED%8A%B81&nickname=tester1&email=tester1@example.com&password=Password1!@"
      "CONTENT_TYPE" => "application/json"
      "HTTP_CONTENT_TYPE" => "application/json"
      "HTTP_USER_AGENT" => "PostmanRuntime/7.40.0"
      "HTTP_ACCEPT" => "*/*"
      "HTTP_CACHE_CONTROL" => "no-cache"
      "HTTP_POSTMAN_TOKEN" => "12345678-0d36-4771-a9c7-1234567890"
      "HTTP_HOST" => "localhost"
      "HTTP_ACCEPT_ENCODING" => "gzip, deflate, br"
      "HTTP_CONNECTION" => "keep-alive"
      "CONTENT_LENGTH" => "122"
      "HTTP_CONTENT_LENGTH" => "122"
      "REQUEST_TIME_FLOAT" => 1234567890.1234
      "REQUEST_TIME" => 1234567890
    ]
  }
  +files: Symfony\Component\HttpFoundation\FileBag {#49
    #parameters: []
  }
  +cookies: Symfony\Component\HttpFoundation\InputBag {#48
    #parameters: []
  }
  +headers: Symfony\Component\HttpFoundation\HeaderBag {#44
    #headers: array:9 [
      "content-type" => array:1 [
        0 => "application/json"
      ]
      "user-agent" => array:1 [
        0 => "PostmanRuntime/7.40.0"
      ]
      "accept" => array:1 [
        0 => "*/*"
      ]
      "cache-control" => array:1 [
        0 => "no-cache"
      ]
      "postman-token" => array:1 [
        0 => "12345678-0d36-4771-a9c7-1234567890"
      ]
      "host" => array:1 [
        0 => "localhost"
      ]
      "accept-encoding" => array:1 [
        0 => "gzip, deflate, br"
      ]
      "connection" => array:1 [
        0 => "keep-alive"
      ]
      "content-length" => array:1 [
        0 => "122"
      ]
    ]
    #cacheControl: array:1 [
      "no-cache" => true
    ]
  }
  #content: """
    {
        "name": "테스트2",
        "nickname": "tester2",
        "email": "tester2@example.com",
        "password": "Password2@#"
    }
    """
  #languages: null
  #charsets: null
  #encodings: null
  #acceptableContentTypes: null
  #pathInfo: null
  #requestUri: null
  #baseUrl: null
  #basePath: null
  #method: null
  #format: null
  #session: null
  #locale: null
  #defaultLocale: "en"
  -preferredFormat: null
  -isHostValid: true
  -isForwardedValid: true
  -isSafeContentPreferred: ? bool
  -trustedValuesCache: []
  -isIisRewrite: false
  #json: Symfony\Component\HttpFoundation\InputBag {#46}
  #convertedFiles: null
  #userResolver: null
  #routeResolver: null
  pathInfo: "/api/req-test"
  requestUri: "/api/req-test?name=%ED%85%8C%EC%8A%A4%ED%8A%B81&nickname=tester1&email=tester1@example.com&password=Password1!@"
  baseUrl: ""
  basePath: ""
  method: "POST"
  format: "html"
}
```

</details>  

## Summary

- Laravel lifecycle과 실제 Request 처리 과정을 확인
- createFromBase 메소드를 확인하여 Request의 body, param 및 처리 과정을 확인
