Title: ip Address to Integer
Subtitle: MySQL IP 주소 변환 함수 (inet_aton, inet_ntoa)
Category: database
Date: 2024-01-01 00:00
Tags: ip address, mysql

MySQL에서는 IP 주소를 다룰 때 유용한 함수들을 제공하며, 그 중 IPv4 및 IPv6 주소를 변환해주는 INET 함수를 확인해보자.  

## INET_ATON(_expr_)

IPv4 네트워크 주소를 문자열로 제공하면 네트워크 바이트 순서([Big Endian](https://www.tcpschool.com/c/c_refer_endian))로 주소의 숫자 값을 나타내는 정수를 반환하고,
인수가 정상적이지 않거나 NULL인 경우 NULL을 반환한다.  

```shell
mysql> SELECT INET_ATON('10.0.5.9');  
        -> 167773449
        
mysql> SELECT INET_ATON(null);
        -> NULL
```

변환하는 방법은 a.b.c.d 주소를 8비트씩 시프트하여 하나의 정수로 결합하는 것이다.  
A = a * 256^3, B = b * 256^2, C = c * 256^1, D = d * 1(=256^0) 로 계산하여 A+B+C+D를 반환한다.  

### 주의 사항

- IPv6나 단축형 IP 주소(예: '127.0.0.1'의 표현인 '127.1')는 결과가 보장되지 않아 사용해서는 안된다.
- 저장할 때, INT를 사용한다면 첫 번째 옥텟이 127보다 큰 IP 주소는 올바르게 저장할 수 없어서 INT UNSIGNED 열을 사용해야 한다. (128.0.0.0 - 255.255.255.255)

## INET_NTOA(_expr_)

INET_ATON(ip Address to Number)의 역.  
네트워크 바이트 순서로 된 정수가 주어지면 IPv4 네트워크 주소를 반환하고, INET_ATON와 동일하게 인수가 정상적이지 않거나 NULL인 경우 NULL을 반환한다.  

```shell
mysql> SELECT INET_NTOA(167773449);
        -> '10.0.5.9'
```

변환하는 방법은 정수를 8비트씩 나눠서 각 옥텟을 추출하고, 점으로 구분된 문자열로 변환하는 것이다.  
만약 [직접 변환](https://www.digikey.kr/ko/resources/conversion-calculators/conversion-calculator-number-conversion)하겠다면, 
정수를 2진수로 변환하고 8비트씩 나눠서 각 옥텟을 추출하고, 점으로 구분된 문자열로 변환한다.  

## INET6_ATON(_expr_)

IPv6 또는 IPv4 네트워크 주소를 문자열로 입력받아, 네트워크 바이트 순서(빅 엔디언)로 변환된 이진 문자열을 반환한다.
IPv6 주소는 VARBINARY(16) 형식으로 변환하고, IPv4 주소는 VARBINARY(4) 형식으로 변환한다.
INET_ATON과 동일하게 인수가 정상적이지 않거나 NULL인 경우 NULL을 반환한다.

### 주의 사항

다음과 같은 형식의 주소는 허용되지 않는다.

- 후행 영역 ID 포함 (fe80::3%1, fe80::3%eth0 등)
- 네트워크 마스크 포함 (2001:45f:3:ba::/64, 198.51.100.0/24 등)
- 클래스가 있는 IPv4 주소 (198.51.1 등)
- 후행 포트 번호 포함 (198.51.100.2:8080 등)
- 16진수 또는 8진수 표기 (198.0xa0.1.2, 198.51.010.1 등)
    - 만약 198.51.010.1을 입력하면, 198.51.8.1이 아니라 198.51.10.1로 처리

## INET6_NTOA(_expr_)

숫자 형태로 표현된 이진 문자열의 IPv6 또는 IPv4 네트워크 주소가 주어지면 연결 문자 집합의 문자열로 주소의 문자열 표현을 반환한다.
인수가 정상적이지 않거나 NULL인 경우 NULL을 반환한다.  

```shell
mysql> SELECT INET6_NTOA(INET6_ATON('fdfe::5a55:caff:fefa:9089'));
        -> 'fdfe::5a55:caff:fefa:9089'
mysql> SELECT INET6_NTOA(INET6_ATON('10.0.5.9'));
        -> '10.0.5.9'

mysql> SELECT INET6_NTOA(UNHEX('FDFE0000000000005A55CAFFFEFA9089'));
        -> 'fdfe::5a55:caff:fefa:9089'
mysql> SELECT INET6_NTOA(UNHEX('0A000509'));
        -> '10.0.5.9'
```

### 주의 사항

- 반환 문자열의 최대 길이는 39(4 x 8 + 7)이다.
- IPv6 주소의 경우 소문자를 사용한다.
- INET6_NTOA()가 mysql 클라이언트 내부에서 호출되면 --binary-as-hex의 값에 따라 16진수 표기법을 사용하여 바이너리 문자열이 표시된다.

## 기타

- IS_IPV4(), IS_IPV6()로 IP 주소 유형 확인 가능하다.
- 대부분 IPv6에 익숙하지 않다.
- 대량의 네트워크 데이터를 보다 효율적으로 저장하고 검색하는 데 유용한 것 같다.
- 검색할 때는 between을 사용하는게 제일 나은 방법인 것 같다.

```sql
SELECT * FROM table WHERE ip BETWEEN INET_ATON('10.0.5.0') AND INET_ATON('10.0.5.255');
```
