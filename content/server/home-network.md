Title: Building a Home Network
Subtitle: 홈 네트워크 구축기
Category: server
Date: 2022-01-01 00:00
Tags: home-network, synology, mesh-wifi


### 1. 구축 동기 및 목표

기존 홈 네트워크는 SKB에서 제공한 기본 공유기 한 대로 운영되고 있었다. 이는 아래와 같은 명확한 한계를 가지고 있었다.

* **Wi-Fi 음영 지역:** 공유기 위치로 인해 특정 공간에서 Wi-Fi 신호가 매우 약하거나 끊겼다.
* **성능 저하:** 연결된 기기가 많아질수록 속도 저하 및 연결 불안정 문제가 발생했다.
* **분산된 데이터:** 다수의 IoT 기기에서 생성되는 로그나 데이터가 중앙에서 관리되지 않았다.

이러한 문제 해결을 위해, 아래 세 가지를 핵심 목표로 홈 네트워크 전체를 재설계 및 구축했다.

1.  **안정적인 네트워크 커버리지 확보:** 메시 와이파이(Mesh Wi-Fi)를 도입하여 집안 전체에 일관된 속도와 안정성을 제공한다.
2.  **중앙화된 데이터 관리:** 모든 IoT 기기와 개인 데이터를 NAS에서 통합 관리하고, 이를 기반으로 자동화 및 모니터링 환경을 구축한다.
3.  **독립적인 개발 환경 구축:** 가상화 서버를 운영하여 외부 서비스에 의존하지 않는 개인 프로젝트 개발 및 테스트 환경을 확보한다.

### 2. 홈 네트워크 아키텍처

목표 달성을 위해 설계한 네트워크 아키텍처는 다음과 같다.

```mermaid
flowchart TD
    subgraph "외부망 (WAN)"
        internet[SKB Giga Internet]
    end

    subgraph "내부망 (LAN - 192.168.1.0/24)"
        internet --> modem[SKB 모뎀 (Bridge Mode)]
        modem --> router[Netgear Orbi Router<br>Gateway: 192.168.1.1]

        subgraph "Core Infrastructure"
            router --> hub[Netgear 7-Port Unmanaged Switch]
            hub --> server[XenServer Host<br>Static IP: 192.168.1.10]
            hub --> nas[Synology DS920+<br>Static IP: 192.168.1.11]
            server <-->|NFS for VM Storage| nas
        end

        subgraph "Wired Clients"
            hub --> PC[Desktop<br>Static IP: 192.168.1.20]
            hub --> iMac[iMac<br>Static IP: 192.168.1.21]
            hub --> MacBook[MacBook Pro<br>Static IP: 192.168.1.22]
        end

        subgraph "Wireless Mesh Network"
            router --> sat[Orbi Satellite]
            router -->|Wireless & Wired Backhaul| sat
            sat --> wireless_devices[DHCP Clients: Laptops, Mobiles, etc.]
            router --> wireless_devices
        end

        subgraph "IoT Devices"
            style IoT fill:#f9f,stroke:#333,stroke-width:2px
            iot_devices[Smart Plugs, Sensors, Lights]
            wireless_devices --> iot_devices
            iot_devices -->|Syslog to 192.168.1.11| nas
        end
    end
```

**아키텍처의 핵심 원칙:**

* **Gateway 일원화:** SKB 모뎀은 브리지 모드로 전환하여 공인 IP를 라우터로 직접 전달하는 역할만 수행한다. 모든 내부 네트워크의 DHCP, NAT, 방화벽 정책은 Netgear Orbi 라우터가 전담하여 관리 복잡성을 줄였다.
* **고정 IP 할당:** 서버, NAS, 주요 워크스테이션 등 핵심 인프라는 MAC 주소 기반으로 IP를 고정 할당하여 서비스의 안정적인 참조를 보장했다. (DHCP Range: `192.168.1.100` ~ `192.168.1.254`)
* **유선 백홀(Wired Backhaul):** Orbi 라우터와 새틀라이트 간의 연결을 유선으로 구성하여, 무선 대역폭을 백홀 통신에 사용하지 않고 오롯이 클라이언트 통신에만 사용하도록 하여 메시 네트워크 성능을 극대화했다.

### 3. 주요 하드웨어 구성

* **Router/AP:** **Netgear Orbi RBR50 (Router + Satellite)**
    * Tri-band Wi-Fi 기술을 통해 클라이언트 통신용 채널과 백홀 통신용 전용 채널을 분리하여 안정적인 메시 네트워크를 구성하는 데 유리했다.
* **Server:** **Custom Built PC**
    * **CPU:** AMD Ryzen 9 3950X (16C/32T)
    * **RAM:** 128GB DDR4
    * **Hypervisor:** XenServer (Citrix Hypervisor)
    * **Rationale:** 다수의 VM을 동시에 운영하고, 컴파일 등 CPU 집약적인 작업을 수행하기에 충분한 리소스를 확보하는 것을 목표로 했다.
* **Storage (NAS):** **Synology DS920+**
    * **HDD:** 12TB x 3 (Synology Hybrid RAID, SHR)
    * **SSD Cache:** 500GB NVMe x 2 (Read/Write Cache)
    * **Rationale:** 가상머신들의 주 스토리지(NFS) 역할과 잦은 로그 파일 기록을 감당하기 위해 SSD 캐시를 구성하여 I/O 성능을 보강했다.
* **UPS:** **EATON Ellipse ECO 650 USB**
    * NAS 및 서버에 연결. 정전 시 제어 신호를 보내 시스템을 안전하게 자동 종료시켜 데이터 무결성을 확보하는 역할을 한다.

### 4. 가상화 서버 및 서비스 운영

XenServer와 Synology NAS의 Docker를 활용하여 다음과 같은 서비스를 운영한다.

#### 4.1. Synology Native & Docker
* **Plex Media Server:** 로컬 미디어 파일 스트리밍. 하드웨어 트랜스코딩을 활용한다.
* **Log Center:** 각 IoT 기기에서 전송되는 Syslog를 수신하여 중앙에서 로그를 집계 및 검색한다.
* **Docker: Home Assistant:** 분산된 IoT 기기(조명, 플러그, 센서 등)를 통합 제어하고 자동화 규칙을 실행하는 허브.

#### 4.2. XenServer (VMs)
XenServer 위에는 목적에 따라 여러 개의 VM을 생성하여 네트워크를 논리적으로 분리했다.

* **VM 1: `docker-services` (Ubuntu 22.04)**
    * 컨테이너 기반의 주요 유틸리티 서비스를 운영한다.
    * **Uptime Kuma:** 내부 서비스(Plex, Gitea) 및 외부 웹사이트의 상태를 주기적으로 확인하는 모니터링 도구.
    * **Gitea:** 개인 프로젝트 및 스터디용 코드 관리를 위한 경량 Git 서버. NAS에 마운트된 볼륨에 데이터를 저장한다.
* **VM 2: `dev-box` (Ubuntu 22.04)**
    * 실제 프로젝트의 개발 및 테스트 환경. 외부 라이브러리 설치나 시스템 설정 변경이 자유로워 주력 개발 머신의 환경을 오염시키지 않는다.

### 5. 문제 해결 과정 (Troubleshooting)

네트워크 지식이 부족한 상태에서 구축을 진행하며 몇 가지 기본적인 문제에 직면했다.

* **Issue 1: 외부 접속 불가 (Port Forwarding)**
    * **Problem:** 외부 네트워크에서 내부 서비스(Plex, Gitea)에 접근할 수 없었다.
    * **Root Cause:** 공인 IP를 가진 SKB 모뎀이 1차 NAT, 내부 IP를 할당하는 Orbi 라우터가 2차 NAT 역할을 하는 이중(Double) NAT 환경이 원인이었다.
    * **Solution:** SKB 모뎀을 브리지(Bridge) 모드로 변경하여 NAT 기능을 비활성화하고, 공인 IP를 Orbi 라우터가 직접 받도록 구조를 변경했다. 이후 Orbi 라우터에서 필요한 서비스 포트를 내부 서버의 고정 IP로 포트 포워딩하여 문제를 해결했다.

* **Issue 2: IP 주소 충돌 및 변경**
    * **Problem:** 기기를 재부팅하면 내부 IP 주소가 변경되어 서비스 간 통신에 장애가 발생했다.
    * **Root Cause:** DHCP 서버의 동적 IP 할당 정책.
    * **Solution:** Orbi 라우터의 '주소 예약(Address Reservation)' 기능에서 서버, NAS 등 주요 기기의 MAC 주소를 찾아 사전에 계획한 고정 IP와 1:1로 매핑했다.

### 6. 구축 결과 및 효용

네트워크 재구축을 통해 초기 목표를 모두 달성할 수 있었다.

* **성능:** 집안 모든 곳에서 평균 400~500Mbps 이상의 안정적인 Wi-Fi 속도를 확보했으며, 유선 기기는 Giga-bit 속도를 완전하게 활용하게 되었다.
* **자동화:** Home Assistant를 중심으로 조도, 온도, 움직임 센서와 연동된 조명 및 가전제품 자동화가 가능해졌다.
* **개발 환경:** 물리적 위치에 구애받지 않고 SSH를 통해 서버에 접속하여 일관된 개발 환경에서 작업할 수 있게 되었다. 신규 프로젝트 테스트를 위한 VM 생성/삭제가 자유로워져 생산성이 향상되었다.

결론적으로, 이번 프로젝트는 단순히 생활의 편의성을 높인 것을 넘어, 개발자로서 인프라의 기초적인 동작 원리를 깊이 이해하는 계기가 되었다.
