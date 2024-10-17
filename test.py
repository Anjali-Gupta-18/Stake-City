import requests

access_key = 'eefbce10f0cfe1f24406cf8e8352342c'  # Replace with your Userstack API access key

def get_device_details(user_agent_string):
    url = 'http://api.userstack.com/detect'
    params = {
        'access_key': access_key,
        'ua': user_agent_string
    }

    try:
        response = requests.get(url, params=params)
        if response.status_code == 200:
            data = response.json()
            print(f"Userstack response: {data}")  # Log the full response for debugging

            # Capture device name and device type from the 'device' key
            device_name = data.get('device', {}).get('name', None)
            device_type = data.get('device', {}).get('type', 'Unknown')

            # If device name is None (common for desktops), fallback to OS name
            if device_name is None:
                device_name = data.get('os', {}).get('name', 'Unknown')

            print(f"Device Name: {device_name}, Device Type: {device_type}")
            return device_name, device_type
        else:
            print(f"Userstack API returned status code {response.status_code}")
            return 'Unknown', 'Unknown'
    except Exception as e:
        print(f"Error getting device details from Userstack: {e}")
        return 'Unknown', 'Unknown'

# Example test with a sample user-agent string
user_agent_string = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/85.0.4183.121 Safari/537.36"
device_name, device_type = get_device_details(user_agent_string)
print(f"Device Name: {device_name}, Device Type: {device_type}")
