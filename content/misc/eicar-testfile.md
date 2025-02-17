Title: EICAR Testfile
Subtitle: [번역] Anatomy of the EICAR Antivirus Test File.
Category: misc
Date: 2024-10-30 00:00
Tags: eicar, antivirus, anti-malware

[@Jerome Bruandet](https://blog.nintechnet.com/author/bruandet/) 게시글 번역 및 내용 정리

- [Anatomy of the EICAR Antivirus Test File.](https://blog.nintechnet.com/anatomy-of-the-eicar-antivirus-test-file/){:
  target="_blank"}
- [kimchanhyung98/eicar-test-files](https://github.com/kimchanhyung98/eicar-testfile){:target="_blank"}
    - [EICAR 테스트 파일](https://www.eicar.org/download-anti-malware-testfile/){:target="_blank"}은
      안티바이러스 프로그램의 정상 작동 여부를 확인하기 위한 68바이트 크기의 16비트 DOS COM 프로그램입니다.
    - 안티바이러스 소프트웨어의 검증(보안 솔루션의 테스트 및 검출)을 목적으로 만들어졌으며, 위험한 코드가 포함되어 있지 않습니다.
    - EICAR Anti-Virus(AV) Test File, EICAR Anti Malware Testfile, EICAR Testfile 등으로 불립니다.

---

## 개요

한 고객이 NinjaFirewall (WP+)의 로그에서 발견한 메시지의 의미를 문의했습니다.

```shell
178.137.xx.xx POST /index.php - EICAR Standard Anti-Virus Test File blocked - [favico.gif, 68 bytes]
```

이 메시지는 누군가가 EICAR 테스트 파일(favico.gif)을 업로드하려 시도했고, NinjaFirewall이 이 시도를 차단했음을 나타냅니다.  
문제 제기를 받고 고객에게 EICAR 테스트 파일에 대한 공식 페이지를 안내하였으나,
고객은 **"어떻게 68개의 문자들이 모여서 프로그램이 되고, 화면에 메시지를 출력할 수 있느냐?"**고 추가로 질문했습니다.

EICAR 테스트 파일은 아래와 같이 단순한 68개의 문자로 구성되어 있습니다.

```plaintext
X5O!P%@AP[4\PZX54(P^)7CC)7}$EICAR-STANDARD-ANTIVIRUS-TEST-FILE!$H+H*
```

단순 문자들로 보이지만, 이 파일은 실제로 실행 가능한 16비트 DOS 프로그램입니다.  
예를 들어, 문자열의 첫 번째 문자 "X"를 살펴보면

- ASCII 테이블에서는 단순히 X라는 문자에 해당합니다.
- 10진수 형식에서는 88입니다.
- 16진수 형식에서는 58h입니다.
- x86 어셈블리 언어에서는 "`pop ax`" 라는 특정 명령어나 instrukction 명령어에 해당합니다.
  이 명령은 스택 포인터(`ss:[sp]`)에서 2바이트 값을 꺼내 16비트 레지스터(`ax`)에 저장(`pop`)하라는 의미입니다.

이와 같이 68개의 문자들 각각 특정한 명령어로 해석될 수 있으므로, 단순한 문자 이상의 의미와 기능(CPU가 이해할 수 있는 기계어 명령어)을 지니게 됩니다.

## 디스어셈블리 목록

EICAR 테스트 파일을 디스어셈블러에 로드하면 다음과 같은 코드 목록이 생성됩니다.

- 첫 번째 열: 현재 세그먼트:오프셋(메모리 주소)
- 두 번째 열: 프로그램 오퍼코드(opcode)
- 세 번째 열: 해당 x86 어셈블리 명령어

```shell
; 실행 가능한 코드의 시작 (29 bytes):  
0001:0100   58       pop ax
0001:0101   354F21   xor ax, 214Fh
0001:0104   50       push ax
0001:0105   254041   and ax, 4140h
0001:0108   50       push ax
0001:0109   5B       pop bx
0001:010A   345C     xor al, 5Ch
0001:010C   50       push ax
0001:010D   5A       pop dx
0001:010E   58       pop ax
0001:010F   353428   xor ax, 2834h
0001:0112   50       push ax
0001:0113   5E       pop si
0001:0114   2937     sub [bx], si
0001:0116   43       inc bx
0001:0117   43       inc bx
0001:0118   2937     sub [bx], si
0001:011A   7D24     jge 0140

; '$'로 종료되는 문자열 (35 bytes):  
0001:011C   db       'EICAR-STANDARD-ANTIVIRUS-TEST-FILE!$'

; 실행 가능한 코드의 끝 (4 bytes):  
0001:0140   48         dec ax
0001:0141   2B482A     sub cx, [bx+si+2Ah]
```

전체 68바이트 중 실행 코드로 사용된 부분은 33바이트입니다.

- 실행 코드는 처음 29바이트와 마지막 4바이트로 구성됩니다.
- 남은 35바이트는 "EICAR-STANDARD-ANTIVIRUS-TEST-FILE!" 문자열과 그 뒤에 오는 종료 문자 '$'로 이루어져 있습니다.

마지막 4바이트의 동작은 다소 모호합니다.

- 0x0140 오프셋에서 `ax` 레지스터를 감소시키고(`dec ax`),
- 0x0141 오프셋에서는 `cx` 레지스터에 대해 특정 값(`bx`와 `si` 기준으로 계산된 값, `sub cx, [bx+si+2Ah]`)을 빼지만,
- 프로그램은 이 값들을 별도로 사용하지 않으므로, 자세한 코드 분석을 통해 의미를 파악해야 합니다.

## 코드 분석

첫 번째 명령어는 스택(`ss:[sp]`)에서 2 바이트를 꺼내(`ax` 레지스터로 pop)옵니다.
<!-- This first instruction pops two bytes from the stack pointer, `ss:[sp]`, into the ax register: -->

```shell
0001:0100 58       pop ax
```

스택이 비어 있으므로 `ax`는 초기화(결과적으로 0으로 설정) 됩니다.   
이는 `mov ax, 0` 또는 좀 더 빠르고 우아한 `xor ax, ax`와 같은 효과를 냅니다.
<!-- Because it is empty, it simply clears `ax`. This is equivalent to instructions such as `mov ax, 0` or the faster (and more elegant) `xor ax, ax`. -->

다음으로, ax와 214Fh를 사용하여 XOR mask를 만듭니다:
<!-- It makes a XOR mask with ax and 214Fh: -->

```shell
0001:0101 354F21   xor ax, 214Fh
```

> 'XOR 마스크를 만든다'는 것은 214Fh 라는 상수를 사용하여, `ax`의 특정 비트들만 선택적으로 반전시키기 위한 기준(패턴)을 설정한다는 의미입니다.  
> 즉, 214Fh 에서 1로 설정된 비트 위치에 해당하는 `ax`의 비트들만 XOR 연산을 통해 토글되어, 원하는 비트 조작을 할 수 있게 해주는 역할을 합니다.

`ax`가 비어 있었기 때문에, 이제 `ax`의 값은 214Fh 가 됩니다.
<!-- Because `ax` was empty, it will be equal to 214Fh now. -->

이 값을 스택에 저장합니다:
<!-- It is saved on the stack: -->

```shell
0001:0104 50       push ax
```

`ax`(현재 값 214Fh)와 4140h 를 사용하여 AND mask를 만듭니다:
<!-- It makes a AND mask with `ax` (214Fh) and 4140h: -->

```shell
0001:0105 254041   and ax, 4140h
```

> 이 명령어는 현재 `ax`의 값(214Fh)와 상수 4140h 를 AND 연산하여, 두 값에서 모두 1인 비트 위치만 1로 남기고 나머지는 0으로 만드는 역할을 합니다.  
> 즉, 4140h 에 지정된 비트만 `ax`에 그대로 남기고, 나머지 비트들은 0으로 만들어 특정 비트들만 선택적으로 필터링합니다.

마스크를 만들기 위해 두 값을 이진수로 나타내면:
<!-- To make a mask, we convert both values to their binary notation: -->

```shell
214Fh: 0010000101001111
4140h: 0100000101000000
------------------------
AND    0000000101000000 => 140h
```

`ax`의 새 값은 이제 140h 입니다.  
EICAR 문자열 데이터 바로 뒤에 오는 첫 번째 바이트의 오프셋 주소임에 유의하세요.  
<!-- ax new value is now 140h. Note that this is the address of the offset of the first byte following the EICAR string data. -->

`ax`의 값이 스택에 저장되고, 그 후 `bx`로 꺼내집니다:
<!-- The value of ax is pushed on the stack, and popped back into bx: -->

```shell
0001:0108 50       push ax
0001:0109 5B       pop bx
```

> `push ax`는 현재 `ax` 레지스터의 값을 스택에 저장하고, `pop bx` 명령어는 스택의 최상단 값을 꺼내 `bx` 레지스터에 대입합니다.  
> 이 과정을 통해 `ax`의 값이 `bx`로 전달되며, 스택을 중간 매개체로 사용하여 값 이동을 수행합니다.  

`al`과 5Ch 를 사용하여 XOR mask를 생성합니다:
<!-- It makes a XOR mask with al and 5Ch: -->

```shell
0001:010A 345C     xor al, 5Ch
```

> 5Ch 의 각 1 비트에 해당하는 `al`의 비트들이 토글됩니다.  
> `al`의 특정 비트만 선택적으로 반전시켜, 원하는 비트 조작(예: 데이터 변환이나 간단한 암호화 효과)을 구현할 수 있습니다.  

`ax`의 값은 현재 0140h 입니다. `al`은 `ax`의 하위 바이트(40h)이고, `ah`는 상위 바이트(01h)입니다:
<!-- ax value is currently 0140h. al is the lower byte of ax (40h), while ah is the higher one (01h): -->

```shell
40h: 01000000
5Ch: 01011100
--------------
XOR  00011100 => 1Ch
```

> `al`(40h)을 이진수 01000000으로 표현하고 5Ch(01011100)와 XOR 연산을 수행하면
> 두 값의 각 비트를 비교하여 서로 다를 때만 1이 되어 결과가 00011100.  
> 1Ch 가 되어 `al`의 특정 비트들을 선택적으로 토글(반전)하는 역할을 합니다.  

`al`의 새 값이 1Ch 가 되었으므로, `ax`의 전체 값은 011Ch 가 됩니다. 이는 EICAR 문자열의 오프셋(주소)을 가리킵니다.
<!-- al‘s new value is 1Ch and hence ax is now equal to 011Ch. It points to the address of the offset of the EICAR string. -->

이 011Ch 값을 스택에 저장하고, 나중에 사용하기 위해 `dx` 레지스터로 꺼냅니다 (이 값은 매우 중요합니다):
<!-- It saves the 011Ch value on the stack and pops it back into the dx register for later use (remember this one, it is important): -->

```shell
0001:010C 50       push ax
0001:010D 5A       pop dx
```

현재 스택 포인터의 값을 `ax` 레지스터에 팝합니다. 이 값은 214Fh 입니다 (0x0104 오프셋의 명령어를 참조하세요):
<!-- It pops the current stack pointer value into ax. It is 214Fh (see the instruction at offset 0x0104): -->

```shell
0001:010E 58       pop ax
```

`ax`와 2834h 를 사용하여 XOR mask를 생성합니다:
<!-- We need to make a XOR mask with ax and 2834h: -->

```shell
0001:010F 353428   xor ax, 2834h

214Fh: 0010000101001111
2834h: 0010100000110100
------------------------
XOR    0000100101111011 => 097Bh
```

> 2834h 에서 1로 설정된 비트 위치에 해당하는 `ax`의 비트들이 토글(반전)되며, 그 결과가 `ax`에 저장됩니다.  

현재 `ax`의 값은 097Bh 입니다. 여기서 기억해야 할 중요한 값은 상위 바이트인 09h 로, 이는 `ah`에 저장되어 있습니다.
이 값은 스택에 저장된 후, `si` 레지스터로 팝됩니다:  
<!-- ax is now equal to 097Bh. The important value to remember here is the higher byte, 09h, which is stored in ah.
It is saved on the stack and popped back into the si register: -->

```shell
0001:0112 50       push ax
0001:0113 5E       pop si
```

이제 좋은 부분입니다: 자기 수정 코드(self-modifying code).
<!-- And now, here comes the good part: the self-modifying code. -->

```shell
0001:0114 2937     sub [bx], si
```

> 메모리 주소 `[bx]`에 저장된 값에서 `si` 레지스터의 값을 뺀 결과를 다시 `[bx]`에 저장합니다.  
> `[bx]`는 코드 내의 특정 주소를 가리키며, 이 연산으로 해당 위치의 데이터(즉, 실행 중인 자신의 코드, 명령어, 상수 등)가 수정됩니다.  

`bx`의 값은 0140h 이며, 따라서 `[bx]`라는 워드 포인터는 오프셋 0x0140 에 위치한 2바이트(48h 와 2Bh)를 가리킵니다.
이 값은 리틀 엔디안 형식으로 2B48h 가 됩니다.  
<!-- bx is equal to 0140h and hence the word pointer [bx] contains the 2 bytes at offset 0x0140 that are 48h and 2Bh, which gives us 2B48h (little-endian data format). -->

여기에 `si`의 값인 097Bh 를 빼면, `[bx]`에 저장된 새 워드 값은 21CDh 가 됩니다.  
<!-- Minus the value of si, 097Bh, the new word at [bx] becomes 21CDh. -->

만약 어셈블리 언어와 DOS 인터럽트에 익숙하다면, 21CDh 가 DOS 인터럽트 21호 호출(`int 21h`)의 opcode임을 눈치챘을 것입니다.  
<!-- If you are familiar with assembly language and the DOS interrupts, you probably noticed that 21CDh is the opcode used for the DOS interrupt 21 call: int 21h. -->

그 후, `bx`의 값(0140h)이 두 번 증가됩니다:  
<!-- Then, it increments bx (0140h) twice: -->

```shell
0001:0116 43       inc bx
0001:0117 43       inc bx
```

`bx`의 값은 이제 0142h 입니다. 이는 프로그램의 마지막 두 바이트(48h 와 2Ah)의 오프셋 주소를 가리킵니다.  
<!-- bx is now equal to 0142h, which means that it points to the address of the offset of the last two bytes of the program, respectively 48h and 2Ah. -->

메모리 주소 `[bx]`에 있는 워드 포인터에서 `si`의 값을 뻅니다.  
<!-- It subtracts si to the word pointer [bx]: -->

```shell
0001:0118 2937     sub [bx], si
```


--- @todo


2A48h에서 si(097Bh)를 빼면 20CDh가 됩니다. 여기서도 COM 프로그램을 종료하는 데 사용되는 또 다른 DOS 인터럽트 호출인 int 20h를 쉽게 알아볼 수 있습니다.
<!-- 2A48h minus si (097Bh) gives 20CDh. Here too, we can easily recognize another DOS interrupt call, int 20h, used to terminate a COM program. -->
프로그램의 마지막 두 바이트는 해당 단어로 즉석에서 패치됩니다. 이것은 자체 수정 코드의 끝입니다.
<!-- The last two bytes of the program are patched on the fly with that word. This is the end of the self-modifying code. -->

다음 명령어는 조건부 명령어이며 다음을 의미합니다. SF 부호 플래그가 OF 오버플로 플래그와 같으면 오프셋 0x0140으로 점프합니다. 이 프로그램에서는 조건이 항상 충족되므로 EICAR 문자열을 건너뜁니다(대안이 없다는 점에 유의하세요. 그렇지 않으면 COM 프로그램이 문자열을 실행하려고 시도하다가 충돌합니다!):
<!-- The next instruction is a conditional one and means: jump to offset 0x0140 if the SF Sign flag equals the OF Overflow one. 
In this program, the condition is always met and hence it will jump over the EICAR string 
(note that there is no alternative, otherwise the COM program would crash trying to execute the string!): -->

```shell
0001:011A 7D24     jge 0140
0001:011C          db 'EICAR-STANDARD-ANTIVIRUS-TEST-FILE!$'
```

그리고 이제 우리는 자체 수정 코드의 결과를 볼 수 있습니다. 원래 디스어셈블리 목록에는 다음과 같은 두 가지 넌센스한 지침이 있었습니다.
<!-- And now, we can see the result of the self-modifying code. In the original disassembly listing, we had these two nonsense instructions: -->

```shell
0001:0140 48         dec ax
0001:0141 2B482A     sub cx, [bx+si+2A]
```

우리는 즉시 패치를 적용했고, 이제 다음과 같은 기능을 제공합니다.
<!-- We just patched them on the fly, and now we have: -->

```shell
0001:0140 CD21     int 21h
0001:0142 CD20     int 20h
```

프로그램 실행 중에 조작된 ah 및 ds:dx 값을 사용하여 다음 매개변수를 사용하여 인터럽트 21h를 호출합니다:
<!-- It will use the values of ah and ds:dx that were manipulated during the execution of the program to call the interrupt 21h with the following parameters: -->

- ah = 09h: DOS int 21h, 디스플레이 문자열 서비스 09h.
- ds:dx = 011Ch: 화면에 표시할 '$'로 끝나는 문자열의 오프셋으로, 여기서는 EICAR 35바이트 문자열을 가리킵니다.
<!-- 
* ah = 09h: DOS int 21h, display string service 09h.
* ds:dx = 011Ch: the offset of the ‘$’ terminated string to display to the screen, which here points to the EICAR 35-byte string. 
-->

마지막으로 DOS 인터럽트 20h를 호출합니다.
<!-- Lastly, it calls the DOS interrupt 20h. -->

그게 다입니다. 이 COM 프로그램은 단순히 "EICAR-STANDARD-ANTIVIRUS-TEST-FILE!" 메시지를 인쇄하고 종료합니다.
<!-- That’s it. This COM program simply prints the “EICAR-STANDARD-ANTIVIRUS-TEST-FILE!” message and quits. -->

## 후속 분석

```shell
jmp     @start
msg     db "EICAR-STANDARD-ANTIVIRUS-TEST-FILE!$"
@start:
mov     dx, offset msg
mov     ah,09h
int     21h
int     20h
```

EICAR 테스트 파일은 다음과 같이 더 간단하게 작성될 수 있으나, 요구 사항을 만족해야 합니다.

- 사용 가능한 문자 제한 : 대문자 알파벳, 숫자, 구두점 등 출력 가능한 ASCII 문자만을 사용해야 합니다. 다른 문자는 허용되지 않습니다.
- 복사 및 출력 가능성 : 텍스트 에디터로 복사 및 붙여넣기가 가능해야 하며, base64 인코딩 없이도 출력할 수 있어야 합니다.
- 빌드 도구 불필요 : 파일을 빌드하기 위해 컴파일러나 링커가 필요하지 않아야 합니다.

자가 수정 코드(self-modifying code)를 사용한 이유:

- 출력 불가능한 명령어 생성 : int 21h와 int 20h와 같은 x86 명령어는 출력이 가능한 ASCII 문자로 표현할 수 없기 때문에,
  실행 중에 해당 명령어들을 실시간으로(on the fly) 생성(patch)하는 방법이 최선의 해결책이었습니다.

- 우회 기법의 재미 : 수십 년 동안 바이러스들은 안티바이러스 프로그램을 우회하기 위해(evasion technique) 자가 수정 코드를 사용해왔습니다.
  EICAR 테스트 파일은 안티바이러스 프로그램의 테스트를 위해 바이러스처럼 취급되어야 하므로,
  자기 수정 코드를 추가함으로써 이 간단하지만 영리한 68바이트 COM 프로그램에 약간의 재미 요소를 더한 것입니다.

## 탐지

EICAR 테스트 파일을 차단하도록 설정하려는 경우, 정확하게 감지하는 방법은 다음과 같습니다.

- EICAR 테스트 파일은 **반드시** 아래와 같은 68바이트로 시작해야 합니다:
    - `X5O!P%@AP[4\PZX54(P^)7CC)7}$EICAR-STANDARD-ANTIVIRUS-TEST-FILE!$H+H*`
    - COM 프로그램이기 때문에, 만약 이 68바이트 앞에 다른 문자가 존재한다면 프로그램은 정상 실행되지 않고 충돌하게 됩니다.
- **선택적으로**, 이 68바이트 뒤에 공백 문자가 올 수 있지만, 파일의 총 길이는 128바이트를 초과해서는 안 됩니다.
    - 허용되는 공백 문자는 다섯 가지입니다.
    - 탭(Tab, 0x09)
    - 줄 바꿈(Line Feed, 0x10)
    - 캐리지 리턴(Carriage Return, 0x13)
    - 스페이스(Space, 0x20)
    - Ctrl-Z(0x1A)

파일이 위의 모든 조건을 만족하면, 애플리케이션은 해당 파일을 바이러스로 간주하여 반드시 차단해야 합니다.  
그렇지 않은 경우에는 무시합니다.
