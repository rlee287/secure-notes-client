import requests
from urllib.parse import urljoin
import posixpath # Url slashes match POSIX directory separators

import thread_pool
import filesystem
def construct_token_header(token):
    request_header={"Authorization":"Bearer "+token}
    return request_header

def get_login_token(base_url,auth_tuple):
    login_url=urljoin(base_url,"login")
    try:
        login_request=thread_pool.async_run_await_result(requests.post,
                login_url,auth=auth_tuple)
        if login_request.status_code!=200:
            return None
        return login_request.json()["token"]
    except requests.exceptions.ConnectionError:
        return None

def send_logout_request(config_obj):
    logout_url=urljoin(config_obj.url,"logout")
    logout_headers=construct_token_header(config_obj.token)
    try:
        logout_request=thread_pool.async_run_await_result(requests.post,
                logout_url,headers=logout_headers)
        if logout_request.status_code!=204:
            return False
        return True
    except requests.exceptions.ConnectionError:
        return False

def get_list(config_obj):
    list_url=urljoin(config_obj.url,posixpath.join(config_obj.username,"notes"))
    auth_header=construct_token_header(config_obj.token)
    try:
        list_request=thread_pool.async_run_await_result(requests.get,
                list_url,headers=auth_header)
        if list_request.status_code!=200:
            return None
        return list_request.json()
    except requests.exceptions.ConnectionError:
        return None

def get_note(config_obj,note_id):
    note_url=urljoin(config_obj.url,posixpath.join(config_obj.username,"notes",note_id))
    auth_header=construct_token_header(config_obj.token)
    try:
        note_request=thread_pool.async_run_await_result(requests.get,
                note_url,headers=auth_header)
        if note_request.status_code==304:
            return filesystem.read_noteobj(config_obj,note_id)
        if note_request.status_code!=200:
            return None
        return {"note":note_request.json(),
                "ETag":note_request.headers["ETag"],
                "Last-Modified":note_request.headers["Last-Modified"]}
    except requests.exceptions.ConnectionError:
        return None

def make_note(config_obj,title,storage_method):
    make_note_url=urljoin(config_obj.url,posixpath.join(config_obj.username,"notes"))
    auth_header=construct_token_header(config_obj.token)
    param_dict={"title":title,
                "storage_format":storage_method}
    try:
        creation_request=thread_pool.async_run_await_result(requests.post,
                make_note_url,headers=auth_header,json=param_dict)
        if creation_request.status_code!=201:
            return None
        return {"id":creation_request.json()["id"],
                "ETag":creation_request.headers["ETag"],
                "Last-Modified":creation_request.headers["Last-Modified"]}
    except requests.exceptions.ConnectionError:
        return None
