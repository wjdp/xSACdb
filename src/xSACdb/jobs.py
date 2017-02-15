import time

def hello_world():
    """Job to test the operation of the worker pool"""
    time.sleep(3)
    print("Test Job")
    return 123

import datetime
def write_to_test_log():
    time.sleep(3)
    with open("log/worker-test.log", "a") as file:
        file.write(str(datetime.datetime.now())+"\n")
    return 456

def raise_exception():
    raise Exception("Hello, I'm an error")
