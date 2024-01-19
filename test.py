import requests

access_token = 'uinRra1UsxEs2Q59'
url = 'https://api.linkedin.com/v2/me'

headers = {
    'Authorization': f'Bearer {access_token}',
    'Connection': 'Keep-Alive',
}

response = requests.get(url, headers=headers)
data = response.json()

# Extract basic information
if 'localizedFirstName' in data and 'localizedLastName' in data:
    full_name = f"{data['localizedFirstName']} {data['localizedLastName']}"
    print(f'Full Name: {full_name}')
else:
    print('Basic information not found.')
