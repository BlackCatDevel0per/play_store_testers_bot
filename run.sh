#!/bin/bash
source .env

if [ -d "$WORKDIR" ]; then
    echo Running prod..
    cd $WORKDIR
    PYTHONPATH=src/pst_bot:. python src/pst_bot/bot.py
    # poetry export --without-hashes --with performance,tg_bot,tg_bot_db,other > requirements.txt
    # pip install -r requirements.txt
else
    echo Running debug..
    # WORKDIR=$(pwd)
    PYTHONPATH=src/pst_bot:. poetry run python src/pst_bot/bot.py
fi
