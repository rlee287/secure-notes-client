import requests
from urllib.parse import urljoin
import posixpath # Url slashes match POSIX directory separators
import thread_pool

def construct_token_header(token):
    request_header={"Authorization":"Bearer "+token}
    return request_header

def get_login_token(base_url,username,password):
    login_url=urljoin(base_url,"login")
    try:
        login_request=thread_pool.async_run_await_result(requests.post,
                login_url,auth=(username,password))
        if login_request.status_code!=200:
            return None
        return login_request.json()["token"]
    except requests.exceptions.ConnectionError:
        return None

def send_logout_request(base_url,token):
    logout_url=urljoin(base_url,"logout")
    logout_headers=construct_token_header(token)
    try:
        logout_request=thread_pool.async_run_await_result(requests.post,
                logout_url,headers=logout_headers)
        if logout_request.status_code!=204:
            return False
        return True
    except requests.exceptions.ConnectionError:
        return False

