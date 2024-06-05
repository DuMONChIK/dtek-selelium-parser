#!/bin/bash


ADDRESS_STREET="my street"
ADDRESS_HOUSE="my house number"
JSON_NAME="my-data.json"


######################

cd `dirname $0`

LOG=./log

exec 1>>${LOG}
exec 2>>${LOG}

# randomize start time
sleep_time=$[RANDOM%120]
sleep ${sleep_time}s

for i in {1..3}; do
 ./dtek-kem-env/bin/python3 ./dtek-selelium-parser/dtek.py -f ${JSON_NAME} --street ${ADDRESS_STREET} --house ${ADDRESS_HOUSE}
 res=$?
 if [ ${res} -eq 0 ]; then
  break
 else
  sleep 30s
  sleep_time2=$[RANDOM%120]
  sleep ${sleep_time2}s
 fi
done

./add-calendar.sh ${JSON_NAME}
