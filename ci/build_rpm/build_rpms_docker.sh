#!/bin/bash

OPNFV_ARTIFACT_VERSION=$1
rpm_build_dir=/opt/escalator
rpm_output_dir=$rpm_build_dir/build_output
tmp_rpm_build_dir=/root/escalator

cp -r $rpm_build_dir $tmp_rpm_build_dir
cd $tmp_rpm_build_dir

echo "#########################################################"
echo "               systemctl info:                   "
echo "#########################################################"
echo "###Uname: $(uname)"
echo "###Hostname: $(hostname)"

maxcount=3
cnt=0
rc=1
while [ $cnt -lt $maxcount ] && [ $rc -ne 0 ]
do
    cnt=$[cnt + 1]
    echo -e "\n\n\n*** Starting build attempt # $cnt"

    cd api
    python setup.py sdist

    cd ..
    cd client
    python setup.py sdist

    echo "######################################################"
    echo "          done              "
    echo "######################################################"
    if [ $rc -ne 0 ]; then
        echo "### Build failed with rc $rc ###"
    else
        echo "### Build successfully at attempt # $cnt"
    fi
done
cd $rpm_output_dir
mkdir upload_artifacts
cp api/dist/escalator-* $rpm_output_dir/upload_artifacts
cp client/dist/escalatorclient-* $rpm_output_dir/upload_artifacts
tar zcvf opnfv-$OPNFV_ARTIFACT_VERSION.tar.gz upload_artifacts
exit $rc
