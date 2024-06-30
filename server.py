# server.py

from flask import Flask, request, redirect

app = Flask(__name__)

CLIENT_ID = '092abfb5ffb543429d75e1ee7ac8561b'
REDIRECT_URI = 'http://localhost:8888/callback'
SCOPES = 'user-library-read'

@app.route('/')
def index():
    auth_url = (
        'https://accounts.spotify.com/authorize?'
        f'client_id={CLIENT_ID}&response_type=code&redirect_uri={REDIRECT_URI}&scope={SCOPES}'
    )
    return redirect(auth_url)

@app.route('/callback')
def callback():
    code = request.args.get('code')
    with open('auth_code.txt', 'w') as f:
        f.write(code)
    return 'Authorization code received. You can close this window.'

if __name__ == '__main__':
    app.run(port=8888)
