Title: ip Address to Integer
Subtitle: IP 주소 변환 함수 (inet_aton, inet_ntoa)
Category: database
Date: 2024-01-01 00:00

MySQL에서는 IP 주소를 다룰 때 유용한 함수를 제공하며, 그 중 IPv4 및 IPv6 주소를 변환해주는 INET 함수를 확인해보자.

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
A = a * 256^3, B = b * 256^2, C = c * 256^1, D = d * 1(255^0) 로 계산하여 A+B+C+D를 반환한다.

### 주의 사항

- IPv6나 단축형 IP 주소(예: '127.0.0.1'의 표현인 '127.1')는 결과가 보장되지 않아 사용해서는 안된다.
- 저장할 때, INT를 사용한다면 첫 번째 옥텟이 127보다 큰 IP 주소는 올바르게 저장할 수 없어서 INT UNSIGNED 열을 사용해야 한다. (128.0.0.0 - 255.255.255.255)

## INET_NTOA(_expr_)

INET_ATON(ip Address to Number)의 역  
네트워크 바이트 순서로 된 정수가 주어지면 IPv4 네트워크 주소를 반환하고, INET_ATON와 동일하게 인수가 정상적이지 않거나 NULL인 경우 NULL을 반환한다.

```shell
mysql> SELECT INET_NTOA(167773449);
        -> '10.0.5.9'
        
mysql> SELECT INET_NTOA(null);
        -> NULL
```

변환하는 방법은 정수를 8비트씩 나눠서 각 옥텟을 추출하고, 점으로 구분된 문자열로 변환하는 것이다.  
만약 [직접 변환](https://www.digikey.kr/ko/resources/conversion-calculators/conversion-calculator-number-conversion)하겠다면,
정수를 2진수로 변환하고 8비트씩 나눠서 각 옥텟을 추출하고, 점으로 구분된 문자열로 변환한다.


## inet6_aton

보통 ipv6에 익숙하지 않는데, 로컬 개발 환경에서 ipv6로 작동하면서 inet6_aton('::1') ?
::1 은 ipv6에서 localhost를 의미


## check
IS_IPV4() / IS_IPV6() - IP 주소 유형 확인

주어진 문자열이 IPv4인지, IPv6인지 확인하는 함수입니다.

SELECT IS_IPV4('192.168.0.1'), IS_IPV6('2001:db8::ff00:42:8329');

결과: 1 (IPv4), 1 (IPv6)

데이터를 보다 효율적으로 저장하고 검색하는 데 유용
 대량의 네트워크 데이터를 다루는 경우, 정수 형식으로 변환하여 저장하면 성능 향상에 도움이 됩니다.