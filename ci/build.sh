#!/bin/bash

# TODO: Let JJB to pass $WORKDIR instead of $BUILD_OUTPUT
ESCALATORDIR=$1/../
OPNFV_ARTIFACT_VERSION=$2

cd ci/build_rpm
./build_rpms.sh $ESCALATORDIR $OPNFV_ARTIFACT_VERSION
