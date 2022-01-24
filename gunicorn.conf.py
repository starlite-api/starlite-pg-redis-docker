import os

# Only runnable on linux
cores = len(os.sched_getaffinity(0))

# Set workers dynamically
if web_concurrency := os.getenv("WEB_CONCURRENCY", None):
    web_concurrency = int(web_concurrency)
    assert web_concurrency > 0
else:
    web_concurrency = max(int(float(os.getenv("WORKERS_PER_CORE", "1")) * cores), 2)

if max_workers := os.getenv("MAX_WORKERS"):
    web_concurrency = min(web_concurrency, int(max_workers))

# Gunicorn config variables
workers = web_concurrency
bind = os.getenv("BIND", None) or f'{os.getenv("HOST", "0.0.0.0")}:{os.getenv("PORT", "80")}'
loglevel = os.getenv("LOG_LEVEL", "info")
errorlog = os.getenv("ERROR_LOG", None)
accesslog = os.getenv("ACCESS_LOG", None)
worker_tmp_dir = "/dev/shm"
keepalive = 5
max_requests = 1000
max_request_jitter = 100
graceful_timeout = 25
timeout = 30
