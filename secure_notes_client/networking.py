from PySide2.QtCore import QCoreApplication

import requests
from urllib.parse import urljoin
import thread_pool
import time

def construct_token_header(token):
    request_header={"Authorization":"Bearer "+token}
    return request_header

#TODO: find a less hacky way to get intermediate dialogs to show
def get_login_token(base_url,username,password):
    login_url=urljoin(base_url,"login")
    print(login_url)
    try:
        login_future=thread_pool.submit_task(requests.post,
                login_url,auth=(username,password))
        while not login_future.done():
            QCoreApplication.processEvents()
        login_request=login_future.result()
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
        logout_future=thread_pool.submit_task(requests.post,
                logout_url,headers=logout_headers)
        while not logout_future.done():
            QCoreApplication.processEvents()
        logout_request=logout_future.result()
        if logout_request.status_code!=204:
            return False
        return True
    except requests.exceptions.ConnectionError:
        return False

