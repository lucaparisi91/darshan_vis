import requests
import os
import time
from datetime import datetime

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
    
    def send_trace_data(self, module : str, filename : str, size : int, duration : int):
        """
        Send trace data to InfluxDB equivalent to the curl command in send_data.sh
        
        Args:
            module (str): Module name for the trace
            filename (str): Filename being traced
            size (int): File size
            duration (int): Operation duration
            
        Returns:
            requests.Response or None: Response object if successful, None if failed
        """
        # Construct the URL
        url = f"{self.influx_host}/api/v2/write"
        
        # Set up query parameters
        params = {
            'org': self.influx_org,
            'bucket': self.bucket,
            'precision': 's'
        }
        
        # Set up headers
        headers = {
            'Authorization': f'Token {self.influx_token}',
            'Content-Type': 'text/plain; charset=utf-8',
            'Accept': 'application/json'
        }
        
        # Create the data payload with current timestamp
        current_timestamp = int(time.time())  # Equivalent to $(date +%s)
        data = f'trace,module={module} filename="{filename}",size={size},duration={duration} {current_timestamp}'
        
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
            
            print(f"Data sent successfully!")
            print(f"Status code: {response.status_code}")
            print(f"Response: {response.text}")
            
            return response
            
        except requests.exceptions.RequestException as e:
            print(f"Error sending data: {e}")
            if hasattr(e, 'response') and e.response is not None:
                print(f"Response status code: {e.response.status_code}")
                print(f"Response text: {e.response.text}")
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

    # Print connection info
    conn_info = client.get_connection_info()
    print(f"Sending data to: {conn_info['host']}")
    print(f"Organization: {conn_info['org']}")
    print(f"Bucket: {conn_info['bucket']}")
    print(f"Timestamp: {int(time.time())}")
    
    # Send the data
    client.send_trace_data(module="MPIO", filename="data.nc", size=678, duration=678)
