#!/bin/sh
if test -z $1 ;then
	echo usage: $0 CLASSNUM
        echo "        for voc the classnum is 21"
	exit 1
fi
echo $1 |grep '^[0-9]*$' >/dev/null 2>&1
if [ $? != 0 ];then
	echo usage: $0 CLASSNUM
        echo "        for voc the classnum is 21"
	exit 1
fi
cls_num=$1
cls_num4=$(expr $1 \* 4)
cls_num6=$(expr $1 \* 6)
trainfile=example/squeezenet_ssd_train.prototxt
testfile=example/squeezenet_ssd_test.prototxt
deploybnfile=example/squeezenet_ssd_deploy_merge_bn.prototxt
deployfile=example/squeezenet_ssd_deploy.prototxt

mkdir -p example

cp template/squeezenet_ssd_train_template.prototxt $trainfile
sed -i "s/CLASSESx6/${cls_num6}/g" $trainfile
sed -i "s/CLASSESx4/${cls_num4}/g" $trainfile
sed -i "s/CLASSES/${cls_num}/g" $trainfile

cp template/squeezenet_ssd_test_template.prototxt $testfile
sed -i "s/CLASSESx6/${cls_num6}/g" $testfile
sed -i "s/CLASSESx4/${cls_num4}/g" $testfile
sed -i "s/CLASSES/${cls_num}/g" $testfile

cp template/squeezenet_ssd_deploy_merge_bn_template.prototxt $deploybnfile
sed -i "s/CLASSESx6/${cls_num6}/g" $deploybnfile
sed -i "s/CLASSESx4/${cls_num4}/g" $deploybnfile
sed -i "s/CLASSES/${cls_num}/g" $deploybnfile

cp template/squeezenet_ssd_deploy_template.prototxt $deployfile
sed -i "s/CLASSESx6/${cls_num6}/g" $deployfile
sed -i "s/CLASSESx4/${cls_num4}/g" $deployfile
sed -i "s/CLASSES/${cls_num}/g" $deployfile

