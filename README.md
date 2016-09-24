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
