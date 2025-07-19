source env.sh

curl --request POST \
"$INFLUX_HOST/api/v2/query?org=$INFLUX_ORG&bucket=$BUCKET" \
  --header "Authorization: Token $INFLUX_TOKEN" \
  --header "Content-Type: application/vnd.flux" \
  --header "Accept: application/csv" \
  --data 'from(bucket: "darshan-explorer")
    |> range(start: 2022-01-01T08:00:00Z, stop: 2026-01-01T20:00:01Z)
    |> filter(fn: (r) => r._measurement == "home")
    |> filter(fn: (r) => r._field== "co" or r._field == "hum" or r._field == "temp")'
