Title: Scout: drivers
Subtitle: [번역] Why do we even need Laravel Scout?
Category: laravel
Date: 2023-03-10 00:00
Tags: scout, search, algolia

@joristein 게시글 번역 및 내용 정리

- [Laravel Scout P2: drivers & limitations](https://medium.com/@joristein/laravel-scout-full-text-search-p2-limitations-drivers-builder-46aef7f03cf5){:target="_blank"}
    - [Elastic Search는 별도](https://laravel-news.com/explorer){:target="_blank"}

---

## Scout가 필요한 이유

컨트롤러에 검색 열 목록을 직접 정의하는 것은 유지보수가 어렵고, 별도의 서비스에서 관리되어야 합니다.  
검색 결과는 사용자 오타에 유연하게 대응할 수 있게 되어야 하며, 이는 더 나은 사용자 경험을 제공합니다.

![search-google]({static}/images/laravel-scout-search-google.webp)

모든 데이터를 스캔해야 하기 때문에 대량의 데이터를 검색할 경우(LIKE) 성능 저하가 발생할 수 있습니다.  
검색 결과는 데이터베이스 저장 순서에 따라 정렬되어 사용자에게 더 관련성이 높은 결과를 보장할 수 없습니다.

![search-db]({static}/images/laravel-scout-db-search-like.webp)

결론적으로 데이터베이스 기반 검색은 성능이 부족해 사용자 만족도를 떨어뜨릴 수 있습니다.  
Scout는 전용 서비스로 검색을 위임하여 이 문제를 해결하고, 다양한 드라이버를 지원합니다.

## 검색 방법

![how-to-search]({static}/images/laravel-scout-how-to-search.webp)

검색은 `::search()` 호출 시 시작되며, 드라이버가 인덱스된 데이터에서 검색을 수행하여 후보 목록을 반환합니다.   
이 목록을 바탕으로 데이터베이스에서 데이터를 가져와 Eloquent 컬렉션으로 반환합니다.

## 드라이버

Scout는 다양한 드라이버를 지원하며 `.env` 파일에서 `SCOUT_DRIVER`를 원하는 드라이버로 설정할 수 있습니다.

### null

아무것도 하지 않으며 데이터를 인덱싱하지 않고, 빈 검색 결과를 반환합니다. ("비활성화"로 생각할 수 있습니다)

**장점**

- 검색 엔진이 애플리케이션을 중단시키는 극단적인 경우, 임시로 비활성화할 수 있습니다.

**단점**

- 아무것도 하지 않기 때문에 단점이 없습니다.

### collection

데이터를 인덱싱하지 않으며 모든 모델을 순회하며 직접 비교를 시도합니다.  
모델의 `toSearchableArray()` 함수를 호출해야 하기 때문에 데이터베이스에서 모든 모델을 로드해야 합니다.

**장점**

- 테스트 실행이나 개발 환경에 적합합니다.
- 큰 알고리즘을 사용하지 않으므로 항상 동일한 결과를 제공합니다.

**단점**

- 성능이 매우 낮아 속도를 현저히 떨어뜨립니다.
- 결과는 typo를 고려하지 않으며 데이터베이스에 저장된 순서대로 반환됩니다.

### database(SQL)

Scout를 사용하지 않고, 데이터베이스에 SQL 문을 이용하여 검색을 맡깁니다.  
(예: `WHERE col LIKE` 또는 `MATCH (col) AGAINST (x)`)

**장점**

- 소규모에서 중규모 프로젝트에 적합하며, 데이터베이스가 이미 최적화되어 있습니다.
- 풀 텍스트 인덱스와 호환되어 쿼리 성능을 향상시킬 수 있지만, 검색 방식은 달라질 수 있습니다.

**단점**

- 오타를 고려하지 않으며, 데이터베이스에 저장된 순서대로 반환됩니다.
- `toSearchableArray()`에 의해 반환된 키는 모델의 열로 존재해야 하므로 관계나 집계된 값에서 검색할 수 없습니다.

### algoila

Algolia는 사용하기 쉬우며 다양한 설정을 제공하는 유료 서비스입니다.   
무료 플랜으로도 소규모 프로젝트나 로컬 테스트에는 충분할 수 있습니다.

**장점**

- 서버나 서비스를 유지할 필요가 없어, 로컬 및 프로덕션 환경 구축이 용이합니다.
- 동의어, 순위, AB 테스트 등 많은 설정을 제공합니다.
- (약간의 수정이 필요하지만) Laravel을 건너뛰고 프론트엔드에서 직접 Algolia로 검색을 할 수 있습니다.

**단점**

- 많은 데이터나 쿼리를 수행할 경우 비용이 발생할 수 있습니다.
- 요청(유저 -> 앱 서버 -> Algolia 서버)이 두 번 필요해 검색이 느려질 수 있습니다.

### meilisearch

Meilisearch는 많은 잠재력을 가진 오픈 소스입니다.  
서버에 설치하거나 유료 서비스를 통해 호스팅할 수 있습니다.

**장점**

- 성능 문제 없이 대량의 데이터를 처리할 수 있습니다.
- 모든 설정은 config/scout.php에 있어, 환경 간의 데이터를 내보내고 가져올 필요가 없습니다.

**단점**

- Meilisearch를 위한 추가적인 인스턴스(서버)와 배포 과정이 필요합니다.

### tntsearch

Tntsearch는 PHP 경량 솔루션으로 애플리케이션 로컬에 인덱싱합니다.  
(Laravel이 기본적으로 지원하지 않는 드라이버입니다)

**장점**

- 모든 것이 로컬에서 이루어지므로, 추가 설정이나 설치 없이 사용할 수 있습니다.

**단점**

- 인스턴스 로컬에 저장되므로 여러 인스턴스 간에 공유되지 않아, 로드 밸런서를 사용할 수 없습니다.
    - (로드 밸런서가 필요한 경우라면 더 나은 드라이버를 사용하는 것이 좋습니다)
- 예상치 못한 결과가 나올 때가 있고, 조정할 수 있는 몇 가지 설정이 있습니다.

## 드라이버 차이점(주의사항)

#### 1. 'database' 드라이버를 사용할 때, Relation 검색

Scout가 데이터베이스로 작동할 때는 실제 테이블에 존재하는 열만을 대상으로 검색을 수행합니다.  
따라서 다른 테이블과의 Relation에서 가져온 데이터는 직접 검색되지 않습니다.

```php
class Post extends Model
{
    use Searchable;

    public function toSearchableArray()
    {
        return [
            'id' => $this->id,
            'title' => $this->title,
            'short_description' => $this->metas?->short_description,
        ];
    }
    
    public function metas()
    {
        return $this->hasOne(Meta::class);
    }
}
```

이런 구조에서는 'relations'에서 가져오는 데이터를 검색하기 위해서는 Algolia, Meilisearch 등을 사용하거나,
데이터베이스 스키마에 직접 해당 열을 추가하는 방법을 고려해야 합니다.

#### 2. null 또는 ''(빈 문자열) 검색

검색 시스템에서 `null`이나 빈 문자열로 인한 예외 처리 방식은 드라이버마다 다를 수 있습니다.
대부분의 드라이버: `null`이나 `''`로 검색을 시도하면, 모든 항목을 반환합니다.
TNTSearch에서는 예상치 못한 빈 배열 반환 문제를 해결하기 위해 추가적인 로직이 필요합니다.

```php
// meilisearch
User::search($search)->get()->count(); // 15

// tntsearch
User::search($search)->get()->count(); // 0
```

#### 3. 검색 열과 정렬 열 구분

이 문제는 검색 시스템에서 특정 열만을 대상으로 검색하고, 다른 열은 정렬 목적으로 사용하는 방법에 관한 것입니다.
Algolia와 Meilisearch와 같은 드라이버는 데이터 인덱싱을 구성할 수 있는 유연성을 제공합니다.

```php
class Post extends Model
{
    use Searchable;

    public function toSearchableArray()
    {
        return [
            'id' => $this->id,
            'title' => $this->title,
            'created_at' => $this->created_at,
        ];
    }
}
```

`toSearchableArray()` 메서드에서 반환하는 배열에 여러 열(예: `id`, `title`, `created_at`)이 포함되어 있지만  
Algolia나 Meilisearch에서는 `title` 열로만 검색을 수행하도록 설정할 수 있습니다.
`created_at` 같은 열은 검색에는 사용되지 않지만 결과 정렬에 활용될 수 있습니다.

```php
User::factory()->count(15)->create(['created_at' => '2023-01-01']);

$search = '2023';

// meilisearch
User::search($search)->get()->count(); // 0

// database
User::search($search)->get()->count(); // 15
```

데이터베이스 드라이버는 인덱싱에 대해 사용자 정의가 제한적입니다.  
따라서, 검색어가 모든 가능한 열(여기서는 `created_at` 포함)에 대해 검색됩니다.   
이로 인해 검색 결과가 다르게 나올 수 있습니다.

## 결론

각 드라이버의 차이점 때문에 초기에 드라이버 선택을 잘 해야 합니다.  
드라이버 특성에 맞춰 코드를 수정해야 하는 경우가 생길 수 있으므로, 검색 기능을 구현할 때는 복잡성을 줄이고 단순하게 설계하는 것이 중요합니다.  
