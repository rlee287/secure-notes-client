from concurrent.futures import ThreadPoolExecutor
import time

from PySide2.QtCore import QCoreApplication

thread_pool=None

def init_thread_pool():
    global thread_pool
    thread_pool=ThreadPoolExecutor()

def deinit_thread_pool():
    global thread_pool
    thread_pool.shutdown()

def submit_task(function,*args,**kwargs):
    global thread_pool
    return thread_pool.submit(function,*args,**kwargs)

#TODO: find a less hacky way to keep events processed
def async_run_await_result(function,*args,**kwargs):
    future_obj=thread_pool.submit(function,*args,**kwargs)
    while not future_obj.done():
        QCoreApplication.processEvents()
        time.sleep(0.1)
    future_result=future_obj.result()
    return future_result
