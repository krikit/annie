#!/usr/bin/env bash


################
# environments #
################
base_dir=`dirname $0`
if [ "`uname`" = "Linux" ]; then
    if [ ! -d /tmp/venv_annie ]; then
        (>&2 echo "0) setting environments")
        tar -C /tmp -xzf ${base_dir}/env/venv_annie.tar.gz
    fi
    source /tmp/venv_annie/bin/activate
fi


#############
# arguments #
#############
function print_usage() {
    echo "Usage: `basename $0` [options]"
    echo "Options:"
    echo "  -h, --help     show this help message and exit"
    echo "  -i FILE        input file"
    echo "  --rsc-dir=DIR  resource dir <default: ${base_dir}/rsc>"
    echo "  --output=FILE  output file <default: result.json>"
    if [ -z "$1" ]; then
        exit 0
    else
        echo
        echo $1
        exit -1
    fi
}

OPTS=`python ${base_dir}/lib/getopts.py "hi:" "help,rsc-dir=,output=" $@`
if [[ $? -ne 0 ]]; then
    print_usage "option parse error"
    exit -1
else
    eval set -- "$OPTS"
fi


while [[ $# -ge 1 ]]; do
    case $1 in
        -h|--help)
            print_usage
            ;;
        -i)
            input="$2"
            shift
            ;;
        --rsc-dir)
            rsc_dir="$2"
            shift
            ;;
        --output)
            output="$2"
            shift
            ;;
        --) break ;;
    esac
    shift
done


# resource dir
if [ "${rsc_dir}" = "" ]; then
    rsc_dir=${base_dir}/rsc
fi
if [ ! -d ${rsc_dir} ]; then
    echo "${rsc_dir} not found"
    exit 1
fi

# input
if [ "${input}" = "" ]; then
    print_usage "-i option is required"
    exit 2
fi

# output
if [ "${output}" = "" ]; then
    output=result.json
fi


############
# settings #
############
export LANG=ko_KR.UTF-8
export PYTHONIOENCODING=UTF-8
export PYTHONPATH=${base_dir}/lib

crf_model=${rsc_dir}/crf.model
if [ ! -f ${crf_model} ]; then
    if [ -f ${crf_model}.gz ]; then
        gzip -c -d ${crf_model}.gz > ${crf_model}
    else
        echo "CRF model file not found"
        exit 3
    fi
fi

w2v_dic=${rsc_dir}/word2vec.pkl
if [ ! -f {w2v_dic} ]; then
    if [ -f ${w2v_dic}.gz ]; then
        gzip -c -d ${w2v_dic}.gz > ${w2v_dic}
    else
        echo "word2vec file not found"
        exit 4
    fi
fi


#######
# run #
#######
bin_dir=${base_dir}/bin


# 1) JSON 코퍼스를 CRF 자질 파일로 변환
(>&2 echo "1) convert JSON input to CRF feature")
feat_file=${output}.crffeat
python ${bin_dir}/json2feat.py -g ${rsc_dir}/gazette.annie \
                                --input=${input} \
                                --output=${feat_file}
if [ $? -ne 0 ]; then
    echo "fail to extract features from ${input}"
    exit 5
fi


# 2) crfsuite를 이용해 태깅
(>&2 echo "2) tag with CRF model")
crfsuite_bin=${bin_dir}/crfsuite.`uname`
tag_file=${output}.crftag
${crfsuite_bin} tag -m ${crf_model} ${feat_file} > ${tag_file}
if [ $? -eq 0 ]; then
    rm -f ${feat_file}
else
    echo "fail to tag with CRF model"
    exit 6
fi


# 3) 태깅한 파일을 JSON 포맷으로 변환
(>&2 echo "3) convert IOB2 to JSON")
crf_predict=${output}.crf
python ${bin_dir}/iob2json.py -j ${input} \
                              --input=${tag_file} \
                              --output=${crf_predict}
if [ $? -eq 0 ]; then
    rm -f ${tag_file}
else
    echo "fail to make JSON with tagged file"
    exit 7
fi


# 4) CRF 결과에 SVM 모델으 이용해 인명 추가 태깅
(>&2 echo "4) tag PS NEs")
python ${bin_dir}/tag_ps.py -w ${w2v_dic} \
                            -m ${rsc_dir}/nusvc_model.pkl \
                            --input=${crf_predict} \
                            --output=${output}
if [ $? -eq 0 ]; then
    rm -f ${crf_predict}
else
    echo "fail to make JSON with tagged file"
    exit 8
fi
