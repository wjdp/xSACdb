import multiprocessing

bind = "0.0.0.0:5000"
workers = multiprocessing.cpu_count() * 2 + 1
# threads = ?

chdir = "src"
preload_app = True

accesslog = "/app/log/access.log"
errorlog = "/app/log/error.log"
capture_output = True
