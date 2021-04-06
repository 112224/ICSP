## reference
## https://github.com/aboul3la/Sublist3r
#### 해당 깃에서 port 옵션이 설정될 경우, 저장되는 파일에도 port에 대한 정보를 추가하였습니다.
#### if set the port option then output file has include the port option



## user guide
#### 기존의 Sublist3r 에서 port 옵션의 default = '80, 443' 으로 변경
#### 파일 저장 방식을 pandas를 이용하여 csv 형태의 파일을 저장할 수 있는 확장자 권장
##### 사용예시
domain	ports	ip_address	ip_class	ssl_infomation
0	www.at.dongguk.edu	NaN	NaN	NaN	NaN
1	as.dongguk.edu	NaN	NaN	NaN	NaN
2	www.dongguk.edu	[80, 443]	210.94.190.35	C	('GlobalSign RSA OV SSL CA 2018', 'Feb 3 00:2...
3	abc.dongguk.edu	[80, 443]	210.94.174.12	C	NaN
4	ace.dongguk.edu	[80, 443]	115.68.17.172	A	NaN
...	...	...	...	...	...
290	smartceo.dongguk.edu	NaN	210.94.222.162	C	NaN
291	scratch.dongguk.edu	NaN	210.94.185.242	C	NaN
292	smdlab.dongguk.edu	NaN	210.94.164.150	C	NaN
293	smtp.dongguk.edu	NaN	210.94.190.65	C	NaN
294	srl.dongguk.edu	NaN	210.94.162.93	C	NaN
