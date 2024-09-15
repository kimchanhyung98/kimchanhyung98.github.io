Title: Scout
Subtitle: adding full-text search to Eloquent models
Category: laravel
Date: 2023-03-01 00:00

간단한 스카우트 소개 ㅁㄴㅇㄹ
유저랑 게시글로 간단한 예시 및 테스트 진행

## Installation

패키지 설치 및 설정 (필요 시, config 파일 수정)

```shell
composer require laravel/scout
php artisan vendor:publish --provider="Laravel\Scout\ScoutServiceProvider"
```

## Create Models and Migrations

Post 모델과 마이그레이션(시드와 팩토리도) 생성

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

php artisan migrate --seed 실행

## Configure the Application to use Laravel Scout

사용할 스카우트 드라이버 설정

```
# .env
SCOUT_DRIVER=algolia  # 로컬 테스트 시, collection 사용
```

생성한 Post 모델에 Searchable과 toSearchableArray 추가하고  
간단한 컨트롤러도 하나 추가

```php
# Post model
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


# PostController
# php artisan make:controller PostController --invokable
class PostController extends Controller
{
    public function __invoke(Request $request)
    {
        $posts = Post::search($request->q)->
            ->orderBy('id', 'desc')
            ->simplePaginate($request->per_page ?? 10)
 
        return response()->json(data: $posts);
    }
}

# routes
Route::get('/search', PostController::class);
```

## Search

```shell
php artisan scout:flush Post
php artisan scout:import Post
php artisan scout:status
```

### ref

- https://laravel.com/docs/master/scout
- https://laravel-news.com/laravel-scout-practical-guide
