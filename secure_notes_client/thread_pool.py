from concurrent.futures import ThreadPoolExecutor

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
