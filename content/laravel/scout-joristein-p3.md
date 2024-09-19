Title: Scout: combining search, filter
Subtitle: Filtering data with Search engine&Eloquent
Category: laravel
Date: 2023-03-11 00:00

@joristein 게시글 번역 및 내용 정리

- [Laravel Scout P3: combining search, filter and ordering](https://medium.com/@joristein/part-3-laravel-scout-full-text-search-p3-combining-search-filter-and-ordering-f7a0c5558f3f)
- [Pagination with subquery broken](https://github.com/laravel/scout/issues/450)

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
중요한 점은 드라이버가 필터링하려면 데이터를 미리 인덱싱해야 합니다.

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
// Here we are indexing the "number of days off" and "is admin"
// as they would otherwise require complexe query
// with LEFT JOINs, EXIST and SUB queries.
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

// Here, we are calculating the total of the invoice, otherwise
// it would require to calculate the total for each invoice
// in the database when a filter is requested
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

ㅁㄴㅇㄹ
