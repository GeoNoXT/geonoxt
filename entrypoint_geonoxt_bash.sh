#!/bin/bash

# Exit script in case of error
set -e

INVOKE_LOG_STDOUT=${INVOKE_LOG_STDOUT:-FALSE}
invoke () {
    if [ "${INVOKE_LOG_STDOUT}" = 'true' ] || [ "${INVOKE_LOG_STDOUT}" = 'True' ]
    then
        # shellcheck disable=SC2068
        /usr/local/bin/invoke -c geonoxt_tasks $@
    else
        # shellcheck disable=SC2068
        /usr/local/bin/invoke -c geonoxt_tasks $@ > /tmp/invoke.log 2>&1
    fi
    # shellcheck disable=SC2145
    echo "$@ tasks done"
}

# shellcheck disable=SC2028
echo $"\n\n\n"
echo "-----------------------------------------------------"
echo "STARTING BASH ENTRYPOINT $(date)"
echo "-----------------------------------------------------"

invoke update

source $HOME/.bashrc
source $HOME/.override_env

echo DOCKER_API_VERSION=$DOCKER_API_VERSION
echo POSTGRES_USER=$POSTGRES_USER
echo POSTGRES_PASSWORD=$POSTGRES_PASSWORD
echo DATABASE_URL=$DATABASE_URL
echo GEODATABASE_URL=$GEODATABASE_URL
echo SITEURL=$SITEURL
echo ALLOWED_HOSTS=$ALLOWED_HOSTS
echo GEOSERVER_PUBLIC_LOCATION=$GEOSERVER_PUBLIC_LOCATION
echo MONITORING_ENABLED=$MONITORING_ENABLED
echo MONITORING_HOST_NAME=$MONITORING_HOST_NAME
echo MONITORING_SERVICE_NAME=$MONITORING_SERVICE_NAME
echo MONITORING_DATA_TTL=$MONITORING_DATA_TTL


# invoke waitfordbs

# shellcheck disable=SC2124
cmd="$*"

echo "-----------------------------------------------------"
echo "BASH ENTRYPOINT -------------------------------------"
echo "-----------------------------------------------------"

# Run the CMD
echo "got command $cmd"
exec /bin/bash -c "$cmd"
