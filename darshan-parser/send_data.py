import requests
import os
import time
from datetime import datetime

# Load environment variables (equivalent to source env.sh)
# You can either set these as environment variables or load from a file

INFLUX_HOST="http://localhost:8086"
INFLUX_ORG="epcc"
INFLUX_TOKEN="JTfObNAAjma5N0tNRFxI7NZIQO3VRLNxCq7dilnHOi43TXnMDmY2RLvgStLSnJ2hUTcsl49hrsJHu5UyfCQoDQ=="
BUCKET="darshan-explorer"

def send_trace_data():
    """
    Send trace data to InfluxDB equivalent to the curl command in send_data.sh
    """
    # Construct the URL
    url = f"{INFLUX_HOST}/api/v2/write"
    
    # Set up query parameters
    params = {
        'org': INFLUX_ORG,
        'bucket': BUCKET,
        'precision': 's'
    }
    
    # Set up headers
    headers = {
        'Authorization': f'Token {INFLUX_TOKEN}',
        'Content-Type': 'text/plain; charset=utf-8',
        'Accept': 'application/json'
    }
    
    # Create the data payload with current timestamp
    current_timestamp = int(time.time())  # Equivalent to $(date +%s)
    data = f'trace,module=MPIO filename="data.nc",size=678,duration=678 {current_timestamp}'
    
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

if __name__ == "__main__":
    
    print(f"Sending data to: {INFLUX_HOST}")
    print(f"Organization: {INFLUX_ORG}")
    print(f"Bucket: {BUCKET}")
    print(f"Timestamp: {int(time.time())}")
    
    # Send the data
    send_trace_data()
