## reference
## https://github.com/aboul3la/Sublist3r
#### 해당 깃에서 port 옵션이 설정될 경우, 저장되는 파일에도 port에 대한 정보를 추가하였습니다.
#### if set the port option then output file has include the port option



## user guide
#### 기존의 Sublist3r 에서 port 옵션의 default = '80, 443' 으로 변경
#### 파일 저장 방식을 pandas를 이용하여 csv 형태의 파일을 저장할 수 있는 확장자 권장
##### 사용예시
![image](https://user-images.githubusercontent.com/34308156/113734551-6432a180-9736-11eb-8bdb-40e1720241d9.png)
##### domain : 서브 도메인 이름을 저장하는 컬럼
##### ports : 기본 80, 443에 대하여 해당 도메인에 접속 가능한 포트 정보 (-p 원하는포트 로 변경 가능), 없을 경우 NaN
##### ip_address : 해당 도메인의 ip 주소를 나타내는 컬럼, 없을 경우 NaN
##### ip_class : ip address 가 존재하는 경우에 한하여, 해당 ip의 class를 나타내는 컬럼
##### ssl_information : 인증서가 존재할 경우 (발급기관, 시작일, 만료일)을 나타내는 컬럼, 없을 경우 NaN 
