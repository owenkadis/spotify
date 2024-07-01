import requests
import base64
import json
import pandas as pd

# Replace these with your actual credentials
CLIENT_ID = '092abfb5ffb543429d75e1ee7ac8561b'
CLIENT_SECRET = ''
REDIRECT_URI = 'http://localhost:8888/callback'

def get_tokens(auth_code):
    auth_string = f"{CLIENT_ID}:{CLIENT_SECRET}"
    auth_bytes = auth_string.encode('ascii')
    auth_base64 = base64.b64encode(auth_bytes).decode('ascii')

    headers = {
        'Authorization': f'Basic {auth_base64}',
        'Content-Type': 'application/x-www-form-urlencoded'
    }

    data = {
        'grant_type': 'authorization_code',
        'code': auth_code,
        'redirect_uri': REDIRECT_URI
    }

    response = requests.post('https://accounts.spotify.com/api/token', headers=headers, data=data)
    
    if response.status_code != 200:
        print(f"Error: Received status code {response.status_code}")
        print(response.content)
        return None, None
    else:
        response_data = response.json()
        if 'access_token' in response_data and 'refresh_token' in response_data:
            access_token = response_data['access_token']
            refresh_token = response_data['refresh_token']
            return access_token, refresh_token
        else:
            print("Error: 'access_token' or 'refresh_token' not found in the response.")
            return None, None

def get_saved_tracks(access_token):
    headers = {
        'Authorization': f'Bearer {access_token}'
    }

    track_data = []
    url = 'https://api.spotify.com/v1/me/tracks'
    while url:
        response = requests.get(url, headers=headers)
        if response.status_code != 200:
            print(f"Error: Received status code {response.status_code} when fetching tracks")
            print(response.content)
            return None
        else:
            tracks = response.json()
            for item in tracks['items']:
                track = item['track']
                track_info = {
                    'track_name': track['name'],
                    'artist': track['artists'][0]['name'],
                    'album': track['album']['name'],
                    'release_date': track['album']['release_date'],
                    'popularity': track['popularity'],
                    'duration_ms': track['duration_ms']
                }
                track_data.append(track_info)
            url = tracks['next']

    return track_data

def main():
    # Read the authorization code from file
    with open('auth_code.txt', 'r') as f:
        auth_code = f.read().strip()

    access_token, refresh_token = get_tokens(auth_code)

    if access_token:
        track_data = get_saved_tracks(access_token)
        if track_data:
            df = pd.DataFrame(track_data)
            print(df.head())  # Display the first few rows of the DataFrame
            df.to_csv('saved_tracks.csv', index=False)  # Save the DataFrame to a CSV file

if __name__ == '__main__':
    main()
