#!/bin/bash

BASEDIR="/home/csam/fed2011"
KMLDIR="${BASEDIR}/kml"

if [ $# -lt 1 ]
then
    echo "missing option..."
    exit
elif [ $# -lt 2 ]
then
    echo "missing year..."
    exit
fi

opt=$1
year=$2
args=""

dir=${KMLDIR}/${year}/${opt}
mkdir -p ${dir}

case ${opt} in
    conservative|liberal|ndp|bloc|green)	args="-p $opt";;
    turnout)					args="-tn";;
esac

fednums="kmlall"

if [ ${opt} == "bloc" ]
then
    fednums="kmlquebec"
fi

echo "fedpolls.py <id> -el $year $args"
while read i
do
    if [ `grep $i ${BASEDIR}/kmlbig.txt | wc -l` -eq 1 ]
    then
	ww="-ww"
	tol="-tol 0.0001"
    else
	ww=""
	tol="-tol 0.0001"
    fi
    CMD="${BASEDIR}/fedpolls.py $i -el ${year} $ww $tol $args > ${dir}/$i.kml"
    ${BASEDIR}/fedpolls.py $i -el ${year} $ww $tol $args > ${dir}/$i.kml
    echo $CMD
    cd ${dir}
    zip $i.kmz $i.kml
    rm $i.kml
    cd -
done < ${BASEDIR}/${fednums}.txt
