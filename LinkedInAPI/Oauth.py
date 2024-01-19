import requests

# Replace with your actual LinkedIn app credentials
CLIENT_ID = ''
CLIENT_SECRET = ''
REDIRECT_URI = 'https://oauth.pstmn.io/v1/browser-callback'

# Step 1: Redirect the user to the LinkedIn authorization URL
authorization_url = f'https://www.linkedin.com/oauth/v2/authorization?response_type=code&client_id={CLIENT_ID}&redirect_uri={REDIRECT_URI}&scope=r_liteprofile&state=12345'

print(f'Please go to the following URL to authorize your application: {authorization_url}')

# After the user grants permission, LinkedIn will redirect them to your specified redirect URI with an authorization code

# Step 2: Retrieve the authorization code from the user's redirected URL

# For example, you can manually input the code from the redirected URL for testing
authorization_code = input('Enter the authorization code from the redirected URL: ')

# Step 3: Exchange the authorization code for an access token
token_url = 'https://www.linkedin.com/oauth/v2/accessToken'

token_params = {
    'grant_type': 'authorization_code',
    'code': authorization_code,
    #'redirect_uri': REDIRECT_URI,
    'client_id': CLIENT_ID,
    'client_secret': CLIENT_SECRET,
}

response = requests.post(token_url, data=token_params)

# Step 4: Extract the access token from the response
access_token = response.json().get('access_token')

print(f'Access Token: {access_token}')
