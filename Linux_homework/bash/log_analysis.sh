#! /bin/bash

CUR_DIR="$(cd -- "$(dirname -- "${BASH_SOURCE[0]}")" &> /dev/null && pwd)"
LOG="$CUR_DIR"/access.log
RES="$CUR_DIR"/results/bash_res.txt

echo -n "Total number of requests: " > "$RES"
wc -l "$LOG" | awk '{print $1}' >> "$RES"


echo -e "\nTotal number of requests by type: " >> "$RES"
cat "$LOG" | awk '{print $6}' | sort | uniq -c | sort -rnk1 | \
awk '{printf "%d -- %s\n", $1, $2}' | sed s/\"// >> "$RES"


echo -e "\nTop 10 most frequent requests: " >> "$RES"
cat "$LOG" | awk '{print $7}' | sort | uniq -c | sort -rnk1 | head | \
awk '{printf "=====\nURL: %s\nRequests number: %d.\n", $2, $1}' >> "$RES"
echo -e "=====" >> "$RES"


echo -e "\n\nTop 5 largest requests with (4XX) response:" >> "$RES"
cat "$LOG" | awk '{if ($9 ~ /4../) printf "%s %d %d %s\n", $7, $9, $10, $1}' | \
sort -rnk3 | head -n 5| awk '{printf "=====\nURL: %s\nResponse: %d\nSize: %d\n\
IP: %s\n", $1, $2, $3, $4}' >> "$RES"
echo -e "=====" >> "$RES"


echo -e "\n Top 5 users by the number of requests that ended with (5XX)
response:" >> "$RES"
cat "$LOG" | awk '{if ($9 ~ /5../) print $1}' | sort -t "." -rnk1 | uniq -c | \
sort -rnk1 | head -n 5 | awk '{printf "=====\nIP: %s\nRequests number: %d\n", $2, $1}' >> "$RES"
echo -e "=====" >> "$RES"
