국어 정보 처리 시스템 경진대회 사용자 설명서


Annie
=====

```





               AAA                                                   iiii                      
              A:::A                                                 i::::i                     
             A:::::A                                                 iiii                      
            A:::::::A                                                                          
           A:::::::::A         nnnn  nnnnnnnn    nnnn  nnnnnnnn    iiiiiii     eeeeeeeeeeee    
          A:::::A:::::A        n:::nn::::::::nn  n:::nn::::::::nn  i:::::i   ee::::::::::::ee  
         A:::::A A:::::A       n::::::::::::::nn n::::::::::::::nn  i::::i  e::::::eeeee:::::ee
        A:::::A   A:::::A      nn:::::::::::::::nnn:::::::::::::::n i::::i e::::::e     e:::::e
       A:::::A     A:::::A       n:::::nnnn:::::n  n:::::nnnn:::::n i::::i e:::::::eeeee::::::e
      A:::::AAAAAAAAA:::::A      n::::n    n::::n  n::::n    n::::n i::::i e:::::::::::::::::e
     A:::::::::::::::::::::A     n::::n    n::::n  n::::n    n::::n i::::i e::::::eeeeeeeeeee  
    A:::::AAAAAAAAAAAAA:::::A    n::::n    n::::n  n::::n    n::::n i::::i e:::::::e           
   A:::::A             A:::::A   n::::n    n::::n  n::::n    n::::ni::::::ie::::::::e          
  A:::::A               A:::::A  n::::n    n::::n  n::::n    n::::ni::::::i e::::::::eeeeeeee  
 A:::::A                 A:::::A n::::n    n::::n  n::::n    n::::ni::::::i  ee:::::::::::::e  
AAAAAAA                   AAAAAAAnnnnnn    nnnnnn  nnnnnn    nnnnnniiiiiiii    eeeeeeeeeeeeee  





```

* 2016년 9월
* 참가팀명: Anything
* 참가자: 임재수
* 소속: 개인 참가


차례
----

1. 소프트웨어 소개
    1. 소프트웨어 명칭
    2. 소프트웨어 사용 환경
    3. 소프트웨어 특징
2. 소프트웨어 설치 및 실행
    1. 소프트웨어 설치 방법
        1. 다운로드에 의한 방법
        2. git clone에 의한 방법
    2. 소프트웨어 파일 구조
        1. 주요 파일 설명
        2. 전체 구조
    3. 소프트웨어 실행 방법
3. 소프트웨어 기능
    1. 프로그램 기능
        1. 성능 평가
        2. 모델 학습
    2. 프로그램 기능 제약
4. 기타


1. 소프트웨어 소개
----

### 1.1 소프트웨어 명칭

* __Annie__는 개체명을 뜻하는 Named Entity, 줄여서 NE라고 부르는 발음 유사성을 이용한 일종의 유희적 이름입니다.
* _(제 옆자리에 앉아 있는 사람의 이름이라고 절대 밝힐 수 없습니다.)_
* 본 소프트웨어를 개발하게 된 동기는 오픈소스 시대에 걸맞게 기존의 소프트웨어를 조합하여 빠르게 아이디어를 실현하는 것이 가능한 지를 실험해 보는 것이었습니다.

### 1.2 소프트웨어 사용 환경

* 지원 OS: Linux, Mac OS
* 권장 메모리: 4GB 이상
* 사용 언어: Python
* 실행 환경: Python 2.6 혹은 2.7
* 텍스트 인코딩: UTF-8
* 의존 패키지
    - `CRFsuite`
        * author: Naoaki Okazaki
        * title: CRFsuite: a fast implementation of Conditional Random Fields (CRFs)
        * year: 2007
        * url: http://www.chokkan.org/software/crfsuite/
    - `libsvm`
        * author: Chang, Chih-Chung and Lin, Chih-Jen
        * title: LIBSVM: A library for support vector machines
        * journal: ACM Transactions on Intelligent Systems and Technology
        * volume: 2
        * issue: 3
        * pages: 27:1--27:27
        * year: 2011
        * url: http://www.csie.ntu.edu.tw/~cjlin/libsvm
    - `scikit-learn`
        * title: Machine Learning in Python
        * url: http://scikit-learn.org

### 1.3 소프트웨어 특징

* 본 소프트웨어는 순수하게 Python 언어로 구현되어 있어 구현이 간단하고 이해하기 쉬워 수정이 용이합니다.
    - Python 프로그램의 소스코드는 [PEP8](https://www.python.org/dev/peps/pep-0008/) 스타일 가이드를 준수합니다. ;)
* 또한 처음 개발을 시작할 때부터 GitHub에 소스 및 개발 과정(이슈)이 공개되어 누구나 재현해 볼 수 있습니다.


2. 소프트웨어 설치 및 실행
----

### 2.1 소프트웨어 설치 방법

#### 2.1.1 다운로드에 의한 방법

* 배포 페이지( https://github.com/krikit/annie/releases )에서 원하는 버전을 다운로드 받습니다.

```
$ wget https://github.com/krikit/annie/archive/0.4.tar.gz
```

* 압축을 풀면 annie-$VERSION 디렉토리가 생성됩니다. (문서를 작성하는 시점의 최신 버전은 0.4입니다.)

```
$ tar -xzf 0.4.tar.gz
```

#### 2.1.2 git clone에 의한 방법

* 최신 소스코드를 설치하고자 한다면 다음과 같이 `git clone` 명령을 수행합니다.

```
$ git clone https://github.com/krikit/annie.git
```

### 2.2 소프트웨어 파일 구조

#### 2.2.1 주요 파일 설명

* JSON 포맷의 입력 파일을 받아들여 역시 JSON 포맷으로 개체명을 인식하는 일련의 과정을 한번에 진행하는 스크립트와, 이 스크립트의 실행에 필요한 디렉토리는 다음과 같습니다.
    - `cqasys_annie.bash`: 일괄 실행 스크립트
    - `bin/`: 각종 단계별 실행 스크립트/바이너리 프로그램
        * `json2feat.py`: JSON 포맷으로부터 CRF 자질을 추출하는 프로그램
        * `crfsuite.Linux`: CRFsuite 태깅 및 학습을 위한 실행 바이너리
        * `iob2json.py`: IBO2 태깅된 결과로부터 JSON 포맷을 생성하는 프로그램
        * `tag_ps.py`: 3음절 인명을 추가적으로 태깅하는 프로그램
    - `env/`: Python 의존 패키지
        * `venv_annie.tar.gz`: Python virtualenv 환경 (Cent OS 6.6 x64)
    - `lib/`: 실행 스크립트가 참조하는 라이브러리
    - `rsc/`: 실행에 필요한 리소스
        * `crf.model.gz`: CRF 모델
            - 최초 실행 시 `crf.model` 파일로 압축 해제
        * `gazette.annie`: train 코퍼스와 기 배포된 gazette를 병합해 구축한 개체명 사전
        * `nusvc_model.pkl`: SVM 모델 파일
        * `word2vec.pkl.gz`: 기 배포된 wikiCorpus_word2vector.hr 파일을 가공한 파일
            - 최초 실행 시 `word2vec.pkl` 파일로 압축 해제

#### 2.2.2 전체 구조

```
annie/
├── bin/
│   ├── baseline.py
│   ├── build_gazette.py
│   ├── crfsuite.Darwin
│   ├── crfsuite.Linux
│   ├── eval.py
│   ├── index_word2vec.py
│   ├── iob2json.py
│   ├── json2feat.py
│   └── tag_ps.py
├── env/
│   ├── requirements.txt
│   └── venv_annie.tar.gz
├── lib/
│   ├── feature.py
│   ├── gazette.py
│   ├── getopts.py
│   ├── sentence.py
│   └── word2vec.py
├── notebook/
│   ├── NNP+NNG_2+3.ipynb
│   ├── README.md
│   ├── ps_classifier.ipynb
│   └── ps_histogram.ipynb
├── rsc/
│   ├── crf.model.gz
│   ├── gazette.annie
│   ├── nusvc_model.pkl
│   └── word2vec.pkl.gz
├── README.md
├── cqasys_annie.bash
└── user_manual.md
```

### 2.3 소프트웨어 실행 방법

* 아래와 같이 스크립트를 실행합니다.

```
$ ./cqasys_annie.bash -i dev.json
0) setting environments
1) convert JSON input to CRF feature
2) tag with CRF model
3) convert IOB2 to JSON
WARNING:root:I- category is different from B-
WARNING:root:I- category is different from B-
WARNING:root:I- category is different from B-
4) tag PS NEs
```

* 출력 파일을 따로 지정하지 않으면 `result.json` 파일이 출력됩니다.
* `cqasys_annie.bash` 스크립트의 사용법은 아래와 같습니다.

```
$ ./cqasys_annie.bash --help
Usage: cqasys_annie.bash [options]
Options:
  -h, --help     show this help message and exit
  -i FILE        input file
  --rsc-dir=DIR  resource dir <default: ./rsc>
  --output=FILE  output file <default: result.json>
```

* 스크립트 내부적으로 다음 절차에 따라 진행됩니다.

1. python 의존 패키지(가상 환경)를 `/tmp/venv_annie`에 압축을 풉니다. (최초에 한번만 수행됩니다.)
2. JSON 입력 파일로부터 CRF 자질을 추출합니다.
3. CRFsuite 실행 파일과 CRF 모델을 이용하여 개체명 인식을 수행합니다.
4. 개체명을 태깅한 IOB2 출력과 입력 JSON 파일을 이용해 출력 형태를 JSON 포맷으로 만듭니다.
5. scikit-learn 패키지와 SVM 모델을 이용해 3음절 인명을 추가로 태깅합니다.


3. 소프트웨어 기능
----

### 3.1 프로그램 기능

* 이하 Python 프로그램을 개별적으로 실행하려면 먼저 다음과 같이 환경 변수를 지정해 라이브러리의 위치를 설정해 줍니다.

```
$ export PYTHONPATH=`pwd`/lib
```

#### 3.1.1 성능 평가

* 시스템에 의해 자동으로 태깅한 JSON 파일과 정답 JSON 파일을 비교하여 다음과 같이 precision/recall을 측정할 수 있습니다.

```
$ bin/eval.py -g dev.json --input=result.json
```

#### 3.1.2 모델 학습

* 기 배포된 `gazzete` 파일과 `train.json` 파일을 병합해 새로운 사전 파일을 생성합니다.

```
$ bin/build_gazette.py -g gazette -c train.json --output=./rsc/gazette.annie
```

* `train.json` 파일을 이용해 CRF 모델 학습을 위한 자질 포맷으로 출력합니다.

```
$ bin/json2feat.py -g ./rsc/gazzete.annie --input=train.json --output=train.crffeat
```

* 자질로 표현된 파일을 이용해 CRF 모델을 학습합니다.

```
$ bin/crfsuite.`uname` learn -m ./rsc/crf.model train.crffeat
```

* 기 배포된 word2vec 파일 `wikiCorpus_word2vector.hr`를 인덱싱 합니다.

```
$ bin/index_word2vec.py -o ./rsc/wod2vec.pkl --input=wikiCorpus_word2vector.hr
```

* scikit-learn 사용을 위해 아래 패키지를 설치합니다.
    - scikit-learn: v0.17.1
    - numpy: v1.6.1
    - scipy: v0.9.0

* Python 패키지 설치 프로그램인 `pip`를 이용해 아래와 같이 한번에 설치합니다.

```
$ pip install -r env/requirements.txt
```

* 혹은 `virtualenv`가 설치되어 있는 Cent OS 6.6 x86 리눅스 시스템에서는 아래와 같이 압축을 풀고 가상 환경에 진입합니다.

```
$ tar -C /tmp -xzf /path/to/annie/env/venv_annie.tar.gz
$ source /tmp/venv_annie/bin/activate
```

* scikit-learn 패키지가 설치되었다면, 마지막으로 `notebook/ps_classifier.ipynb` 파일을 [Jupyter Notebook](http://jupyter.org/)을  이용해 실행합니다. `rsc/` 디렉토리 아래 SVM 모델 파일 `nusvc_model.pkl`이 생성됩니다.

### 3.2 프로그램 기능 제약

* 본 프로그램은 Cent OS 6.6 x64 리눅스 환경에 맞춰져 있습니다.


4. 기타
----

### 4.1 CRF 자질

* CRF 학습을 위해 -2 ~ +2 위치의 5개 형태소를 기반으로 아래의 자질을 사용했습니다.
    - lemma, lemma bigram
    - pos tag, tag bigram, tag trigran
    - gazzete 사전 매칭 IOB2 태그 및 그 bigram, trigram
    - 1, 2음절 prefix/suffix
    - 형태소의 길이는 단독이 아니라 아래의 조합만 사용했습니다.
        * gazette 사전 매칭 + 길이
        * 1, 2음절 prefix/suffix + 길이
    - lexical form(pattern)
        * 한글 -> '가', 한자 -> '漢', 영문 -> 'A', 숫자 -> '0', 기호 -> '.'
    - begin/end of sentence
    - begin/middle/end of word(어절)
    - 이전 어절의 마지막 형태소, 다음 어절의 첫 형태소 및 그 결합

### 4.2 SVM 자질

* CRF 학습 후 인명의 재현율이 다소 떨어지는 데 착안하여 3음절 NNP 품사를 갖는 단일 형태소에 대해 별도의 인명 분류기를 학습했습니다.
* SVM 학습을 위해 -2 ~ +2 위치의 기 배포된 형태소 embedding 벡터(50 x 5 = 250차원)를 사용했습니다.

### 4.3 성능 평가

* `train.json` 파일을 이용해 학습한 후 `dev.json` 파일에 측정한 최종 성능은 아래와 같습니다.

```
======== OG ========
# of NEs in gold standard: 412
# of NEs in test file    : 327
# of NEs in both(matched): 285
Precision: 0.8716
Recall:    0.6917
F1-score:  0.7713

======== PS ========
# of NEs in gold standard: 581
# of NEs in test file    : 502
# of NEs in both(matched): 463
Precision: 0.9223
Recall:    0.7969
F1-score:  0.8550

======== TI ========
# of NEs in gold standard: 42
# of NEs in test file    : 42
# of NEs in both(matched): 38
Precision: 0.9048
Recall:    0.9048
F1-score:  0.9048

======== TOTAL ========
# of NEs in gold standard: 1589
# of NEs in test file    : 1460
# of NEs in both(matched): 1278
Precision: 0.8753
Recall:    0.8043
F1-score:  0.8383
```
