import base64
import hashlib
import os
import re
from http.server import BaseHTTPRequestHandler, HTTPServer
from urllib import parse
import webbrowser
import requests
import json

try:
    from dotenv import load_dotenv
    load_dotenv()
except ImportError:
    print("dotenv not found, ensure settings are properly set in the config dict")

#Instructions:
#Create a new application at https://dev.fitbit.com/apps/new
#Set OAuth 2.0 Application Type to Personal
#Set the redirect URL to: http://localhost:4444 (port can be changed)
#All other required fields can be arbitrarily filled in
#After creating the new application, find your client ID and enter it into the .env file or paste it below
#Change token_file as desired. Defaults to a file called "token" in the current directory

#HTTP server logic derrived from https://www.camiloterevinto.com/post/oauth-pkce-flow-from-python-desktop
config = {
    #Put your client ID here if running from a different environment
    "client_id": os.environ.get("CLIENT_ID", ""),
    "token_file": os.environ.get("TOKEN_FILE_PATH", "token"),
    "port": int(os.environ.get("REDIRECT_PORT", 4444)),
    "auth_uri": "https://www.fitbit.com/oauth2/authorize",
    "token_uri": "https://api.fitbit.com/oauth2/token",
    "scopes": "activity heartrate location nutrition oxygen_saturation profile respiratory_rate settings sleep social temperature weight"
}

class OAuthHttpServer(HTTPServer):
    def __init__(self, *args, **kwargs):
        HTTPServer.__init__(self, *args, **kwargs)
        self.authorization_code = ""


class OAuthHttpHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        self.send_response(200)
        self.send_header("Content-Type", "text/html")
        self.end_headers()
        self.wfile.write(("Done! The token has been saved to '" + config['token_file'] + "'<br>You can close this window.").encode("UTF-8"))
        
        parsed = parse.urlparse(self.path)
        qs = parse.parse_qs(parsed.query)
        
        self.server.authorization_code = qs["code"][0]

with OAuthHttpServer(('', config['port']), OAuthHttpHandler) as httpd:
    code_verifier = base64.urlsafe_b64encode(os.urandom(66)).decode('utf-8')
    code_verifier = re.sub('[^a-zA-Z0-9]+', '', code_verifier)

    code_challenge = base64.urlsafe_b64encode(hashlib.sha256(code_verifier.encode('utf-8')).digest()).decode('utf-8')
    code_challenge = code_challenge.replace('=', '')

    auth_params = {
        "client_id": config['client_id'],
        "response_type": "code",
        "code_challenge": code_challenge,
        "code_challenge_method": "S256",
        "scope": config['scopes']
    }

    formatted_auth_uri = config['auth_uri'] + "?" + parse.urlencode(auth_params)
    webbrowser.open_new(formatted_auth_uri)
    httpd.handle_request()

    token_data = {
        "code": httpd.authorization_code,
        "client_id": config["client_id"],
        "grant_type": "authorization_code",
        "code_verifier": code_verifier
    }

    response = requests.post(config["token_uri"], data=token_data, verify=True)
    with open(config['token_file'], "w") as file:
        json.dump({"access_token": response.json()["access_token"], "refresh_token": response.json()["refresh_token"]}, file)

    httpd.server_close()