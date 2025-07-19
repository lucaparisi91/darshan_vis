source env.sh

curl --request POST \
"$INFLUX_HOST/api/v2/write?org=$INFLUX_ORG&bucket=$BUCKET&precision=s" \
  --header "Authorization: Token $INFLUX_TOKEN" \
  --header "Content-Type: text/plain; charset=utf-8" \
  --header "Accept: application/json" \
  --data-binary "
trace,module=MPIO filename=\"data.nc\",size=320,duration=678 $(date +%s)
"