#! /bin/bash
PORT=${PORT:-'8088'}
HOST=${HOST:-'0.0.0.0'}

UVICORN="uvicorn app:webapp --port ${PORT} --host ${HOST}"
COMMAND=$UVICORN

declare -a HOT_RELOAD_DIRS=(
    'app'
    'chassis'
    'domains'
    'infra'
)

RELOAD_ARGS='--reload'
for dirname in ${HOT_RELOAD_DIRS[@]}; do
    RELOAD_ARGS="${RELOAD_ARGS} --reload-dir ${dirname}"
done

if [ ${DEBUG} = 'True' ]; then
    echo "Starting server in DEBUG mode and RELOAD"
    COMMAND="PYTHONASYNCIODEBUG=1 PYTHONTRACEMALLOC=1 ${UVICORN} ${RELOAD_ARGS}"
fi
echo ${COMMAND}
eval ${COMMAND}
