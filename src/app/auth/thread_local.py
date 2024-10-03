import threading

thread_local = threading.local()

def set_current_user(user_id):
    thread_local.user_id = user_id

def get_current_user():
    return getattr(thread_local, 'user_id', None)