#!/bin/bash

input_json="$1"

# Minutes before remind of event
# less zero - disable
# zero and bigger - enable reminder
CALENDAR_REMIND_MINUTES=-1


###############################

if [ ! -f "${input_json}" ]; then
 echo "ERROR: No json file"
 exit 1
fi

if [ ${CALENDAR_REMIND_MINUTES} -ge 0 ]; then
 reminder=${CALENDAR_REMIND_MINUTES}
else
 reminder=""
fi

for days in today tomorrow; do
 day_name=`LC_ALL=C date --date ${days} "+%A"`
 delete_t1=`LC_ALL=C date --date "${days}" "+%F"`
 delete_t2=`LC_ALL=C date --date "${days} + 1 day" "+%F"`

 echo "day_name=${day_name}"

 # fix DTEK day names
 day_name_dtek=${day_name}
 if [ ${day_name} == "Wednesday" ]; then
       day_name_dtek="Wedndesday"
 fi

 readarray -t SHUTDOWNS < <(jq ".${day_name_dtek}" ${input_json})

 if [ "${#SHUTDOWNS[@]}" -eq 26 ]; then

  # delete events from calendar
  gcalcli --nocolor delete \
   --military "DTEK" \
   "${delete_t1}" "${delete_t2}" \
   --iamaexpert

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
    color="grape"
   else
    color="flamingo"
   fi
   if [ ${ss} == "Off" ] || [ ${ss} == "Maybe" ]; then
    gcalcli --nocolor add \
     --calendar "DTEK" \
     --title "DTEK/${ss}" \
     --when "${day_name} ${t1}" \
     --duration "60" \
     ${reminder} \
     --description "Power ${ss}" \
     --color ${color} \
     --noprompt
   fi
  done
 fi
done
