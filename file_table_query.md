# Queries

## File statistics panel


```python
import "join"

data= from(bucket: "darshan-explorer")
    |> range(start: -2d)
    |> filter(fn: (r) => (r.operation == "read") )
    |> pivot(rowKey: ["_time"], columnKey: ["_field"], valueColumn: "_value")
    |> group(columns: ["file_name"])

duration = data
         |>  group(columns: ["file_name","rank"]) |> keep(columns: ["file_name","rank","duration"]) |> sum(column: "duration") |> group(columns: ["file_name"]) |> max(column: "duration") |> keep(columns: ["duration","file_name"])

length = data
        |>  group(columns: ["file_name","rank"]) |> keep(columns: ["file_name","length"]) |> sum(column: "length") 

fileTableRaw = join.inner(left: duration, right: length, on: (l,r) => (l.file_name == r.file_name),as: (l, r) => ({l with length: r.length}) )

fileTable= fileTableRaw |> group()  |> map(fn: (r) => ({r with length:r.length/1000000.})) |> map(fn: (r) => ({r with duration:r.duration/1000.})) |> map(fn: (r) => ({ r with bandwidth: r.length / (r.duration) }))

fileTable |> sort(columns: ["duration"], desc: true)
```
