Title: Scout: combining search, filter
Subtitle: [번역] Filtering data with Search engine&Eloquent
Category: laravel
Date: 2023-03-11 00:00
Tags: scout, search, filter, eloquent

@joristein 게시글 번역 및 내용 정리

- [Laravel Scout P3: combining search, filter and ordering](https://medium.com/@joristein/part-3-laravel-scout-full-text-search-p3-combining-search-filter-and-ordering-f7a0c5558f3f){:target="_blank"}
- [Pagination with subquery broken](https://github.com/laravel/scout/issues/450){:target="_blank"}

---

## Scout Builder instance

`::search` 함수를 호출하면 반환되는 것이 쿼리 빌더 인스턴스라는 점을 알 수 있습니다.  
그러나 일반적으로 사용하는 `Illuminate\Database\Eloquent\Builder`가 아닌, `Laravel\Scout\Builder`가 반환됩니다.

```php
$eloquentBuilder = User::where('name', 'LIKE', '%John%');
get_class($eloquentBuilder);
// "Illuminate\Database\Eloquent\Builder"

$scoutBuilder = Project::search('John');
get_class($scoutBuilder);
// "Laravel\Scout\Builder"
```

Eloquent 빌더는 SQL 쿼리를 통해 복잡한 데이터베이스 작업을 지원하지만  
Scout 빌더는 검색 엔진과의 상호작용을 목적으로 설계되어 기능이 제한적입니다.

- 이 구조는 검색 엔진이 대량의 데이터를 빠르게 처리할 수 있도록 하며, 데이터 검색의 복잡성을 줄입니다.
- 데이터베이스 자체에 복잡한 필터링을 맡기는 대신, 인덱싱된 데이터로 효율적인 검색을 가능하게 합니다.

## 검색 엔진을 사용하여 데이터 필터링

Laravel Scout에서 `::search`를 사용하면 Scout Builder 인스턴스를 얻습니다.
이 Builder에서 `where` 메서드를 사용하여 검색 조건을 설정할 수 있습니다.

```php
$builder = User::search('John');
$builder->where('is_admin', true);
$builder->where('salary', 50000);
```

다음으로 Meilisearch를 사용하는 경우, 'john'이라는 키워드를 가진 사용자 중 급여가 50,000 이상인 관리자만 검색하도록 지시합니다.
중요한 점은 드라이버가 데이터를 필터링하려면 데이터를 미리 인덱싱해야 합니다.

```php
class User extends Model
{
    use Searchable;

    public function toSearchableArray(): array
    {
        return [
            'id' => $this->id,
            'name' => $this->name,
            'is_admin' => $this->is_admin,
            'salary' => $this->salary,
        ];
    }
}
```

1. **대규모 데이터셋 처리 개선**
    - 데이터베이스가 매우 커져서 MySQL에서도 필터링이 느려지는 경우, 인덱싱된 데이터를 사용하는 것이 유리합니다.
    - 대부분의 기업이 이 정도의 데이터셋에 도달하지는 않지만, 가능성을 염두에 두고 설계할 수 있습니다.

2. **복잡한 계산 및 쿼리 최적화**
    - 인덱싱된 데이터로, 복잡한 쿼리를 피하면서 열 이외의 데이터로 필터링할 수 있습니다.
    - 이는 많은 처리 시간이나 성능이 필요한 데이터를 미리 준비해 두는 방식입니다.

```php
// days_off_count 와 is_admin를 미리 인덱싱
// left join, exist 나 sub 쿼리를 사용하지 않고도 필터링 가능
class Employee extends Model
{
    use Searchable;

    public function toSearchableArray(): array
    {
        return [
            'id' => $this->id,
            'days_off_count' => $this->getDaysOffCount(),
            'is_admin' => $this->premiumOfferActive() && $this->hasPermission('admin_access'),
        ];
    }
}

// invoice 총액을 미리 계산
// 필터를 호출할 때, 데이터베이스에서 각 invoice의 총액을 계산할 필요가 없음
class Invoice extends Model
{
    use Searchable;

    public function toSearchableArray(): array
    {
        return [
            'id' => $this->id,
            'total' => $this->getTotal(withDiscounts: true, withTaxes: true),
        ];
    }
}
```

**마지막 단계**

- 검색 엔진을 통해 데이터를 필터링할 때, 어떤 데이터가 검색에 사용되고 어떤 데이터가 필터링에 사용되는지를 엔진에 명시해야 합니다.
- Algolia에서는 인덱싱이 생성된 후 인덱스 설정에서 찾을 수 있고, Meilisearch에서는 config/scout.php 파일에서 구성할 수 있습니다.

## 데이터베이스를 사용하여 데이터 필터링

검색 엔진을 구현하는 방법에 따라 데이터베이스에서 데이터를 필터링하고 싶을 수 있습니다.
Scout를 사용하면 기본적으로 Eloquent 인스턴스에 접근할 수 없게 되지만, ->query(...) 메서드를 사용하여 다시 Eloquent 빌더에 접근할 수 있습니다.
[#](https://laravel.com/docs/9.x/scout#customizing-the-eloquent-results-query){:target="_blank"}

```php
use Illuminate\Database\Eloquent\Builder;

[...]

$builder = User::search('John')->query(function ($query){
    // get_class($query); "Illuminate\Database\Eloquent\Builder"

    return $query->where('is_admin', true);
});
```

```php
use Illuminate\Database\Eloquent\Builder;

$builder = User::search($request->get('search'))->query(function (Builder $query) use ($request){
    return $query
        ->with(['addresses', 'tags', 'role'])
        ->where('is_admin', true)
        ->isActive() // scope
        ->whereRelation('addresses', 'country', 'France')
        ->when($request->has('role', function ($query) use ($request){
            $query->where('role_id', $request->get('role'));
        }));
});
```

데이터를 나열하는 동시에 데이터를 검색하고 필터링할 수 있는 옵션을 제공하려는 경우 이 방법이 일반적입니다.

::search('')가 호출된 이후에만 사용할 수 있는, ->query(...) 함수 안에 필터가 작성되어 있기 때문에    
사용자가 요청하지 않아도 항상 검색을 수행하게 됩니다.

대부분의 드라이버는 빈 값(null, '')을 검색할 때, '플레이스홀더'로 간주하여 무시하고 전체 데이터를 반환합니다.   
하지만 TNTSearch 드라이버는 예외로, null 값을 받으면 빈 결과를 반환합니다.

## 데이터 정렬

기본적으로, 검색 결과는 드라이버에 의해 검색 적합도(search relevancy)에 따라 정렬됩니다. (Algolia와 Meilisearch 같은 검색 엔진에서 유용합니다)
하지만 SQL 쿼리에서 설정한 정렬 기준이 무시될 수 있으며, 예기치 않은 결과를 초래할 수 있습니다.

예를 들어 아래 코드에서는 사용자의 salary(급여)를 내림차순으로 정렬하려고 했지만, 검색 적합도 우선순위에 따라 결과가 반환됩니다

```php
$builder = User::search('John')->query(function ($query){
    return $query->orderBy('salary', 'desc');
});

dump($builder->get());

// { [
//    {
//     'id' => 2,
//     'name' => 'John',
//     'salary' => 30000,
//    },
//    {
//     'id' => 1,
//     'name' => 'jonathan',
//     'salary' => 90000,
//    }
// ]}
```

내림차순으로 정렬했지만 검색 적합성이 우선되어(주어진 검색어와 더 관련성이 높음)  
'John'이 'Johnetta'보다 먼저 표시되어 salary 기준 내림차순 정렬이 무시됩니다.

데이터 정렬은 필터링과 같은 방식으로 작동합니다.
먼저 모델에서 데이터를 인덱싱해야 하면 Scout Builder에서 `orderBy`를 사용할 수 있습니다.

```php
class User extends Model
{
    use Searchable;

    public function toSearchableArray(): array
    {
        return [
            'id' => $this->id,
            'name' => $this->name,
            'salary' => $this->salary,
        ];
    }
```

```php
$builder = User::search('John');

$builder->orderBy('salary', 'desc');

dump($builer->get());

// { [
//    {
//     'id' => 1,
//     'name' => 'Johnetta',
//     'salary' => 90000,
//    },
//    {
//     'id' => 2,
//     'name' => 'John',
//     'salary' => 30000,
//    }
// ]}
```

## 모든 것을 결합

글을 마무리하기 위해, Meilisearch를 사용하여 검색, 필터링, 정렬을 구현하는 예를 들어보겠습니다.  
Intervention 모델에 Searchable 트레잇을 사용하여 Meilisearch가 인덱싱할 수 있도록 합니다.

```php
class Intervention extends Model
{
    use Searchable;

    public function toSearchableArray(): array
    {
        return [
            'id' => $this->id,
            'name' => $this->name,
            'reference' => $this->reference,
            'duration_seconds' => $this->duration_seconds,
            'created_at' => $this->created_at,
            'date' => $this->date,
        ];
    }
```

Meilisearch가 데이터를 적절히 처리할 수 있도록 `config/scout.php` 설정 파일을 수정합니다.

```php
'meilisearch' => [
    'host' => env('MEILISEARCH_HOST', 'http://localhost:7700'),
    'key' => env('MEILISEARCH_KEY', null),
    'index-settings' => [
        \App\Models\Intervention::class => [
            'searchableAttributes' => ['name', 'reference'],
            'sortableAttributes' => ['duration_seconds', 'created_at', 'date',],
        ],
    ],
],
```

이후, `php artisan scout:sync-index-settings` 명령어로 설정을 Meilisearch와 동기화합니다.

컨트롤러를 만들기 전에, 재사용할 handleScoutRequest trait을 만들어 검색 쿼리, 정렬 기준, 정렬 방향 등을 처리하는 여러 메서드를 정의합니다.

```php
namespace App\Http\Controllers\Traits;

trait handleScoutRequest
{
    // 검색어 처리
    public function getSearchQuery(Request $request, string $query = 'search'): string
    {
        return $request->str($query)->trim()->toString();
    }

    // 정렬 요청 확인
    public function customOrder(Request $request): bool
    {
        return $request->has('sort');
    }

    // 정렬 기준 컬럼 가져오기
    public function getOrderByColumn(Request $request): ?string
    {
        return $request->str('sort')->trim()->toString();
    }

    // 정렬 방향 결정
    public function getOrderByDirection(Request $request): string
    {
        // It is expected to get "/api/interventions?sort=salary" to sort by salary in an ascending order
        // and "/api/interventions?sort=-salary" to sort by salary in an descending order
        $column = $this->getOrderByColumn($request);
        
        return str_starts_with($column, '-') ? 'desc' : 'asc';
    }
}
```

검색, 필터링, 정렬을 모두 처리할 수 있도록 컨트롤러를 구현합니다.
(handleScoutRequest 트레잇을 사용하여 검색어와 정렬 옵션을 추출하고, 조건에 따라 client와 vehicle 필터링도 처리합니다)

```php
class InterventionController extend Controller
{
    use handleScoutRequest;
    
    public function index(Request $request)
    {
        $builder = Intervention
            ::search($this->getSearchQuery($request))
            ->query(function (Builder $query) use ($request) {
                $query
                    ->with(['client','vehicle'])
                    ->when($request->has('client'), function ($query) use ($request) {
                        return $query->where('client_id', $request->get('client'));
                    })
                    ->when($request->has('vehicle'), function ($query) use ($request) {
                        return $query->where('vehicle_id', $request->get('vehicle'));
                    });
            })
            ->when($request->customOrder(), function ($query) use ($request) {
                return $query->orderBy($this->getOrderByColumn($request), $this->getOrderByDirection($request));
            });
    
        return InterventionResource::collection($builder->paginate());
    }
}
```

## 결론

이 글에서 Scout를 사용하여 전체 텍스트 검색을 빠르게 구현하는 방법과 Algolia 및 Meilisearch 같은 강력한 검색 드라이버와 통신하는 방법을 살펴보았습니다.
특히, 검색, 필터링, 정렬과 같은 기능을 결합할 때 코드 작성 방식에 변화를 주어야 하기 때문에 조금 까다로워질 수 있다는 점도 배웠습니다.
구현에 초점을 맞추었지만, 아직 고려해야 할 부분들이 많이 남아있습니다.

- 데이터 형식 맞추기
- 검색 결과에서 검색어 하이라이트 표시
- 여러 모델에서 검색 결과를 보여주는 검색 창 구현
- 자동 완성 기능
- Boolean 검색
- etc.
