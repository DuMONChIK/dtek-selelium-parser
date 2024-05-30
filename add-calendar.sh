#!/bin/bash

input_json="$1"

if [ ! -f "${input_json}" ]; then
 echo "ERROR: No json file"
 exit 1
fi

for days in today tomorrow; do
 day_name=`LC_ALL=C date --date ${days} "+%A"`
 delete_t1=`LC_ALL=C date --date "${days}" "+%F"`
 delete_t2=`LC_ALL=C date --date "${days} + 1 day" "+%F"`

 readarray -t SHUTDOWNS < <(jq ".${day_name}" ${input_json})

 if [ "${#SHUTDOWNS[@]}" -eq 26 ]; then

  # delete events from calendar
  gcalcli delete --military "DTEK" "${delete_t1}" "${delete_t2}" --iamaexpert

  for i in {1..24}; do
   s=${SHUTDOWNS[${i}]}
   s=${s//\"/}  # delete quotes
   s=${s//,/}   # delete commas
   s=${s/:\ / } # split time / state
   s=${s/-/ }   # split time start/end
   states=(${s/:\ / }) # split to array
   ss=${states[2]}
   t1=${states[0]}
   t2=${states[1]}
   if [ ${ss} == "Maybe" ]; then
    color="flamingo"
   else
    color="grape"
   fi
   if [ ${ss} == "Off" ] || [ ${ss} == "Maybe" ]; then
    gcalcli add \
     --calendar "DTEK" \
     --title "DTEK/${ss}" \
     --when "${day_name} ${t1}" \
     --duration "60" \
     --description "Power ${ss}" \
     --reminder 0 \
     --color ${color} \
     --noprompt
   fi
  done
 fi
done
