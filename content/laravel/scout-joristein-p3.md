Title: Scout: combining search, filter
Subtitle: Filtering data with Search engine&Eloquent
Category: laravel
Date: 2023-03-11 00:00

@joristein 게시글 번역 및 내용 정리

- [Laravel Scout P3: combining search, filter and ordering](https://medium.com/@joristein/part-3-laravel-scout-full-text-search-p3-combining-search-filter-and-ordering-f7a0c5558f3f)
- [Pagination with subquery broken](https://github.com/laravel/scout/issues/450)

---

## 쿼리 빌더

Laravel Scout의 쿼리 빌더는 검색 쿼리를 쉽게 작성할 수 있는 기능을 제공합니다. 몇 가지 주요 기능은 다음과 같습니다:

- **Search**: 기본 검색 기능으로, 주어진 키워드를 사용하여 검색할 수 있습니다.
- **Where Clause**: 검색 조건을 추가할 수 있는 기능으로, 특정 필드에 대해 필터링이 가능합니다.
- **OrderBy**: 결과를 정렬하는 데 사용되며, 여러 정렬 조건을 지원합니다.

이 글에서는 Laravel Scout를 활용한 기본적인 검색 작업부터 복잡한 검색 요구 사항까지 지원할 수 있는 다양한 방법을 소개합니다. 각각의 필요에 맞는 적합한 드라이버를 선택하고, 쿼리 빌더의 다양한 기능을
활용하여 보다 효율적인 검색 환경을 구축할 수 있습니다.

---

# Laravel Scout: 검색, 필터링 및 정렬의 결합

이 글은 Laravel Scout로 전체 텍스트 검색을 구현할 때, 어떻게 검색, 필터링, 그리고 정렬 기능을 함께 사용할 수 있는지를 설명합니다. 이 방법들은 보다 정교한 검색 환경을 구축할 때 유용합니다.

## 검색 기능의 확장

기본 검색 기능 외에도, Laravel Scout는 검색 결과를 보다 세밀하게 조정할 수 있는 방법을 제공합니다. 이를 통해 사용자가 원하는 정확한 결과를 쉽게 찾을 수 있습니다.

### 필터링 (Filtering)

- **Where 조건**: 특정 필드를 기준으로 검색 결과를 필터링할 수 있습니다. 예를 들어, 상태가 활성(Active)인 데이터만 검색하고 싶을 때 유용합니다.

- **범위 필터링**: 날짜나 가격과 같은 연속적인 값을 가지는 필드를 지원하며, 특정 범위 내의 결과를 추출할 수 있습니다.

### 정렬 (Ordering)

- **OrderBy**: 검색 결과에 대해 하나 이상의 필드를 기준으로 정렬이 가능합니다. 예를 들어, 생성 날짜나 이름을 기준으로 오름차순 또는 내림차순 정렬이 가능합니다.

## 실제 예제

글에서는 라라벨에서 어떻게 실제로 이러한 기능들을 구현할 수 있는지 예제 코드를 통해 설명합니다.

예를 들어, 사용자가 입력한 검색어에 대해 특정 카테고리의 항목만 검색하고, 가격을 기준으로 정렬된 결과를 반환할 수 있습니다.

```php
$results = Product::search('키워드')
    ->where('category', 'electronics')
    ->orderBy('price', 'asc')
    ->get();
```

이러한 조합된 검색 기능은 다양한 사용자 요구를 충족할 수 있게 하며, 애플리케이션의 유연성과 사용성을 개선하는 데 큰 도움이 됩니다.

## 결론

Laravel Scout를 사용하면 간단한 텍스트 검색 이상의 기능을 구현할 수 있습니다. 이를 통해 복잡하고 다양한 검색 시나리오에 대응할 수 있으며, 사용자에게 보다 정교한 검색 경험을 제공합니다.

이와 같은 기능을 적절히 활용하면, 애플리케이션에서 검색의 역할을 크게 강화할 수 있습니다.
