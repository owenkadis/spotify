import requests
import base64
import json

# Replace these with your actual credentials
CLIENT_ID = '092abfb5ffb543429d75e1ee7ac8561b'
CLIENT_SECRET = '5349afbff5a649b1adc72a210008538d'
REDIRECT_URI = 'http://localhost:8888/callback'
AUTH_CODE = 'AQAhUdI_8ztPeepdV1v22L8yF5JkITEFz_NeKaLH74Q5BXhpiWpOYylSb11V3U5NwPfxxsPnb6H7bSRmMa4bWJUj4eJ7G7v0Dur5_Lju31aTaG8qYsPXDLWxSKyuf_BdxRUkVtsKfdLioCZ765nFdsvxGdCyrMPc2NjGMJSnLnU3JcLOYhS8a_VP7Vc9iglcbmVTl0I'

auth_string = f"{CLIENT_ID}:{CLIENT_SECRET}"
auth_bytes = auth_string.encode('ascii')
auth_base64 = base64.b64encode(auth_bytes).decode('ascii')

headers = {
    'Authorization': f'Basic {auth_base64}',
    'Content-Type': 'application/x-www-form-urlencoded'
}

data = {
    'grant_type': 'authorization_code',
    'code': AUTH_CODE,
    'redirect_uri': REDIRECT_URI
}

response = requests.post('https://accounts.spotify.com/api/token', headers=headers, data=data)
response_data = response.json()

access_token = response_data['access_token']
refresh_token = response_data['refresh_token']

print(f"Access Token: {access_token}")
print(f"Refresh Token: {refresh_token}")

headers = {
    'Authorization': f'Bearer {access_token}'
}

response = requests.get('https://api.spotify.com/v1/me/tracks', headers=headers)
tracks = response.json()

for idx, item in enumerate(tracks['items']):
    track = item['track']
    print(f"{idx + 1}. {track['artists'][0]['name']} - {track['name']}")
