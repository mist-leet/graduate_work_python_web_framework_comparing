#!/usr/bin/env bash
BASEDIR=$(dirname "$0")
echo "Executing App in '$BASEDIR'"
PORT=$1
source $BASEDIR/../venv/bin/activate

for port in $(seq 8889 8900);
do
  python3 $BASEDIR/app.py $port
done


