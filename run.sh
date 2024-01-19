#!/bin/bash
source .env

PYTHONPATH=src/pst_bot:. poetry run python src/pst_bot/bot.py
