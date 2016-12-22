#!/bin/bash

set -eux
ESCALATORDIR=$1
OPNFV_ARTIFACT_VERSION=$2

function build_rpm_pkg {
        # Cleanup prev build resutls
        rm -rf $ESCALATORDIR/build_output
        mkdir -p $ESCALATORDIR/build_output

        sudo docker build -t escalator_rpm ../../docker
        sudo docker run --rm -v $ESCALATORDIR:/opt/escalator -v $CACHE_DIRECTORY:/home/cache -t  escalator_rpm \
                      /opt/escalator/ci/build_rpm/build_rpms_docker.sh $OPNFV_ARTIFACT_VERSION

	# Here to collect build result from $ESCALATORDIR/build_output
}

function cleanup_container {
        containers_to_kill=$(sudo docker ps --filter "label=escalator_image_version" \
                --format "{{.Names}}" -a)

        if [[ -z "$containers_to_kill" ]]; then
                echo "No containers to cleanup."
        else
                volumes_to_remove=$(sudo docker inspect -f \
                        '{{range .Mounts}} {{printf "%s\n" .Name }}{{end}}' \
                        ${containers_to_kill} | egrep -v '(^\s*$)' | sort | uniq)
                echo "Stopping containers... $containers_to_kill"
                sudo docker stop -t 2 ${containers_to_kill} >/dev/null 2>&1

                echo "Removing containers... $containers_to_kill"
                sudo docker rm -v -f ${containers_to_kill} >/dev/null 2>&1

                if [[ -z "$volumes_to_remove" ]]; then
                        echo "No volumes to cleanup."
                else
                        echo "Removing volumes... $volumes_to_remove"
                        sudo docker volume rm ${volumes_to_remove} >/dev/null 2>&1
                fi
        fi
}

function cleanup_docker_image {
        images_to_delete=$(sudo docker images -a --filter "label=escalator_image_version" \
                --format "{{.ID}}")

        echo "Removing images... $images_to_delete"
        if [[ -z "$images_to_delete" ]]; then
                echo "No images to cleanup"
        else
                sudo docker rmi -f ${images_to_delete} >/dev/null 2>&1
        fi
}

cleanup_container
cleanup_docker_image
build_rpm_pkg
