
from influxdb import InfluxDBClient
from parser import dxt_parser
from typing import List
import time 

def create_influx_db_record(record: dict, measurement: str, tags: List[str], fields: List[str] , start: int) -> dict:
    """
    Create a record for InfluxDB from the parsed Darshan trace data.
    
    Args:
        record (dict): Parsed record from Darshan trace.
        measurement (str): Measurement name for InfluxDB.
        tags (List[str]): List of tags to include in the record.
        fields (List[str]): List of fields to include in the record.
    
    Returns:
        dict: Formatted record for InfluxDB.
    """

    return {
        "measurement": measurement,
        "tags": {tag: record[tag] for tag in tags},
        "fields": {field: record[field] for field in fields},
        "start": record['start'] + start
    }

if __name__ == "__main__":

    # Create InfluxDB client instance
    client = InfluxDBClient(
    influx_host="http://localhost:8086",
    influx_org="epcc",
    influx_token="JTfObNAAjma5N0tNRFxI7NZIQO3VRLNxCq7dilnHOi43TXnMDmY2RLvgStLSnJ2hUTcsl49hrsJHu5UyfCQoDQ==",
    bucket="darshan-explorer"
    )

    parser = dxt_parser("example_darshan_trace.txt")

    influx_records = [ create_influx_db_record(
        record,
        measurement="darshan_trace",
        tags=[ "module", "operation"],
        fields=["rank", "offset", "length", "start", "end","file_name"],
        start=int((time.time() -  60*60*24)*1e+3)  # Adjust start time to be 1 hour ago
    ) for record in parser.records ]

    client.send(influx_records)
