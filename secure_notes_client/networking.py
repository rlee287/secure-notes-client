import requests
from urllib.parse import urljoin

def construct_token_header(token):
    request_header={"Authorization":"Bearer "+token}
    return request_header

def get_login_token(base_url,username,password):
    login_url=urljoin(base_url,"login")
    print(login_url)
    try:
        login_request=requests.post(login_url,auth=(username,password))
        if login_request.status_code!=200:
            return None
        return login_request.json()["token"]
    except requests.exceptions.ConnectionError:
        return None

def send_logout_request(base_url,token):
    logout_url=urljoin(base_url,"logout")
    print(logout_url)
    try:
        logout_headers=construct_token_header(token)
        logout_request=requests.post(logout_url,headers=logout_headers)
        if logout_request.status_code!=204:
            return False
        return True
    except requests.exceptions.ConnectionError:
        return False

