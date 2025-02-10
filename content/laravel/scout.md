Title: Scout
Subtitle: adding full-text search to Eloquent models
Category: laravel
Date: 2023-03-01 00:00
Tags: scout, search, algolia

데이터 검색을 위한 패키지인 Scout에 대해 간단히 소개하고 설치 방법을 설명하고,  
유저와 게시글을 이용하여 간단한 예시와 테스트를 진행한다.

## Installation

Composer를 사용하여 Scout를 설치하고, 설정 파일을 복사 및 수정한다.

```shell
composer require laravel/scout
php artisan vendor:publish --provider="Laravel\Scout\ScoutServiceProvider"
```

`config/scout.php` 파일이 생성되고 프로젝트에 맞춰 필요한 설정을 수정한다.

## Create Models and Migrations

이제 Post 모델과 관련된 마이그레이션, 시드와 팩토리를 생성한다.

```shell
php artisan make:model Post -m
php artisan make:seeder PostTableSeeder
```

```php
# Post migration
public function up()
{
    Schema::create('posts', function (Blueprint $table) {
        $table->id();
        $table->foreignId('user_id')->constrained();
        $table->string('title', 100);
        $table->text('contents');
        $table->timestamps();
        $table->softDeletes();
    });
}

# Post factory
public function definition(): array
{
    return [
        'user_id' => User::inRandomOrder()->first()->id,
        'title' => $this->faker->sentence(4),
        'contents' => $this->faker->paragraphs(3, true),
    ];
}
```

설정이 완료되었다면 다음 명령어를 사용하여 마이그레이션을 진행하고 시더를 실행한다.

```shell
php artisan migrate --seed
```

## Configure the Application to use Laravel Scout

이제 애플리케이션이 Scout를 사용하여 검색할 수 있도록 설정한다.
`algoliasearch-client-php`를 설치하고 .env 파일에 Algolia 인증 정보를 추가한다.
(블로그에서는 algolia를 사용했지만, 개발 환경에서는 `collection`을 사용한다)

```shell
composer require algolia/algoliasearch-client-php
```

```dotenv
# .env

SCOUT_DRIVER=algolia

ALGOLIA_APP_ID=
ALGOLIA_SECRET=
```

생성한 Post 모델에 `Searchable` 트레이트를 추가하고 `toSearchableArray` 메서드를 정의한다.

```php
class Post extends Model
{
    use HasFactory, Searchable, SoftDeletes;

...

    public function toSearchableArray(): array
    {
        return [
            'id' => $this->id,
            'title' => $this->title,
            'contents' => $this->contents,
        ];
    }
}
```

검색 기능을 테스트하기 위해 `PostController`를 생성하고 간단한 메서드를 추가한다.

```php
# php artisan make:controller PostController --invokable
class PostController extends Controller
{
    public function __invoke(Request $request)
    {
        $posts = Post::search($request->q)
            ->orderBy('id', 'desc')
            ->simplePaginate($request->per_page ?? 10)
 
        return response()->json($posts);
    }
}
```

컨트롤러를 사용할 수 있도록 라우트도 설정한다.

```php
# routes
Route::get('/search', PostController::class);
```

## Search

마지막으로, Scout 명령어를 사용하여 검색 인덱스를 생성하고 상태를 확인한다.

```shell
# php artisan scout:flush Post
php artisan scout:import Post
php artisan scout:status
```

### ref

- [laravel-docs:scout](https://laravel.com/docs/master/scout){:target="_blank"}
- [laravel-news:scout practical guide](https://laravel-news.com/laravel-scout-practical-guide){:target="_blank"}
