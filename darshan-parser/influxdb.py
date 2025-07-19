import requests
import os
import time
from datetime import datetime
import parserlogs
from typing import List

logger = parserlogs.logging.getLogger(__name__)

class InfluxDBClient:
    """
    InfluxDB client for sending trace data
    """

    def __init__(self, influx_host : str, influx_org : str, influx_token : str, bucket : str):
        """
        Initialize the InfluxDB client with connection parameters
        
        Args:
            influx_host : InfluxDB host URL
            influx_org : InfluxDB organization
            influx_token : InfluxDB authentication token
            bucket : InfluxDB bucket name
        """

        # Use provided parameters
        self.influx_host = influx_host 
        self.influx_org = influx_org 
        self.influx_token = influx_token 
        self.bucket = bucket
        logger.info(f"Created connection to InfluxDB with the following parameters:")
        logger.info(f"Influx Host: {self.influx_host}")
        logger.info(f"Organization: {self.influx_org}")
        logger.info(f"Bucket: {self.bucket}")

    

    def send(self, records : List[dict] ):
        """
        Send trace data to InfluxDB equivalent to the curl command in send_data.sh
        
        Args:
            records : List of dictionaries containing trace data. Each record should contain:
            - measurement (str): Measurement name
            - tags (Dict): Tags associated with the measurement
            - fields (Dict): Fields containing the measurement data
        Returns:
            requests.Response or None: Response object if successful, None if failed
        """
        # Construct the URL
        url = f"{self.influx_host}/api/v2/write"
        
        # Set up query parameters
        params = {
            'org': self.influx_org,
            'bucket': self.bucket,
            'precision': 'ms'
        }
        
        # Set up headers
        headers = {
            'Authorization': f'Token {self.influx_token}',
            'Content-Type': 'text/plain; charset=utf-8',
            'Accept': 'application/json'
        }
        
        def field_value(value):
            """
            Convert field value to string format for InfluxDB
            """
            if isinstance(value, str):
                return f'"{value}"'
            else:
                return value

        data=""
        for record in records:
            measurement = record["measurement"]
            tags = record["tags"]
            fields = record["fields"]
            timestamp = record["start"]  # Assuming 'start' is the timestamp in milliseconds
            data += f'{measurement},{",".join([f"{k}={v}" for k, v in tags.items()])} {",".join([f"{k}={field_value(v)}" for k, v in fields.items()])} {timestamp}\n'

        try:
            # Make the POST request
            response = requests.post(
                url=url,
                params=params,
                headers=headers,
                data=data
            )
            
            # Check the response
            response.raise_for_status()  # Raises an exception for bad status codes

            logger.debug(f"Data sent successfully!")
            logger.debug(f"Status code: {response.status_code}")
            logger.debug(f"N records sent: {len(records)}")

            return response
        
        except requests.exceptions.RequestException as e:
            logger.error(f"Error sending data: {e}")
            if hasattr(e, 'response') and e.response is not None:
                logger.error(f"Response status code: {e.response.status_code}")
                logger.error(f"Response text: {e.response.text}")
            return None
    
    def get_connection_info(self):
        """
        Get connection information for debugging
        
        Returns:
            dict: Connection parameters
        """
        return {
            'host': self.influx_host,
            'org': self.influx_org,
            'bucket': self.bucket,
            'token_preview': f"{self.influx_token[:10]}..." if self.influx_token else None
        }


if __name__ == "__main__":
    # Create InfluxDB client instance
    client = InfluxDBClient(
        influx_host="http://localhost:8086",
        influx_org="epcc",
        influx_token="JTfObNAAjma5N0tNRFxI7NZIQO3VRLNxCq7dilnHOi43TXnMDmY2RLvgStLSnJ2hUTcsl49hrsJHu5UyfCQoDQ==",
        bucket="darshan-explorer"
    )


    # Send the data
    client.send(records=[
        {"measurement": "trace", "tags": {"module": "MPIO"}, "fields": {"size": 678, "duration": 678, "filename": "data.nc"}, "start": int(time.time())},
        {"measurement": "trace", "tags": {"module": "MPIO"}, "fields": {"filename": "data.nc", "size": 6897, "duration": 678}, "start": int(time.time())}
    ])
