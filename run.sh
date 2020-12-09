LOGS=pythonProject1/nlu/logs
MODELS=pythonProject1/nlu/models

if [[ ! -d "$LOGS" ]]; then 
    mkdir $LOGS
fi
if [[ ! -d "$MODELS" ]]; then 
    mkdir $MODELS
fi
if [[ -z "$(ls -A -- "$MODELS")" ]]; then 
    docker-compose up train
fi
if  find "$MODELS" -mindepth 1 -print -quit 2>/dev/null | grep -q . ; then
    docker-compose up start
fi
