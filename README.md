annie
=====

* 2016 국어 정보 처리 시스템 - 지정 분야: 개체명 인식 시스템 개발 및 적용
* https://ithub.korean.go.kr/user/contest/contestIntroLastView.do


실행 방법
----

```
./cqasys_annie.bash -i dev.json
```

* -i 옵션으로 입력 파일(JSON 포맷)을 전달합니다. (필수 옵션)
* --output=result.json 형태로 출력 파일(JSON 포맷)을 지정합니다.
    - 지정하지 않으면 현재 디렉토리에 result.json 파일을 출력합니다.
* --rsc-dir=./rsc 형태로 리소스 디렉토리의 경로를 지정합니다.
    - 지정하지 않으면 cqasys_annie.bash 파일과 동일한 위치에서 rsc 디렉토리를 찾습니다.


사용자 설명서
----

[user_manual.md](user_manual.md)


발표 자료
----

[notebook/annie_presentation.ipynb](notebook/annie_presentation.ipynb)


라이센스
----

### Software

* 본 소스 코드에 대해 어떠한 라이센스 권리도 행사하지 않습니다.
* License disclaimer! Just copyleft!

### 말뭉치(Corpus)

* 본 프로그램에서 학습 및 평가에 사용하는 말뭉치는 ETRI 연구 결과물 중 기술이전 대상인 [한국어 세분류 개체명 태깅말뭉치 DB](https://itec.etri.re.kr/itec/sub02/sub02_01_1.do?t_id=1123-2015-00236#1)의 일부를 사용한 것으로 알고 있습니다.
* [2016년 한글 및 한국어 정보처리 학술대회](https://sites.google.com/site/2016hclt/)에서 해당 말뭉치를 "2016년 엑소브레인 V2.0 & 울산대학교 말뭉치"라는 명칭의 CD로 배포했으니 자세한 내용은 아래 두 파일을 참고하시기 바랍니다.
    - [소개자료](corpus/001.introduction.pdf)
    - [사용허가협약](corpus/002.license_agreement.pdf)
