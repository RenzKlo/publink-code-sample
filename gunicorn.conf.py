"""
Gunicorn configuration file for production deployment.
"""

import os
import multiprocessing

# Server socket
bind = f"0.0.0.0:{os.getenv('PORT', '5000')}"
backlog = 2048

# Worker processes
workers = int(os.getenv('WEB_CONCURRENCY', multiprocessing.cpu_count() * 2 + 1))
worker_class = 'sync'
worker_connections = 1000
timeout = 30
keepalive = 2

# Restart workers after this many requests, to help prevent memory leaks
max_requests = 1000
max_requests_jitter = 100

# Load application code before the worker processes are forked
preload_app = True

# Application
wsgi_module = 'app_new:app'

# Logging
accesslog = '-'
errorlog = '-'
loglevel = os.getenv('LOG_LEVEL', 'info').lower()
access_log_format = '%(h)s %(l)s %(u)s %(t)s "%(r)s" %(s)s %(b)s "%(f)s" "%(a)s" %(D)s'

# Process naming
proc_name = 'publink_server'

# Server mechanics
daemon = False
pidfile = '/tmp/gunicorn.pid'
tmp_upload_dir = None

# SSL (if needed)
# keyfile = '/path/to/keyfile'
# certfile = '/path/to/certfile'

# Worker process configuration
def when_ready(server):
    """Called just after the server is started."""
    server.log.info("PubLink server is ready. Listening on: %s", server.address)

def worker_int(worker):
    """Called just after a worker has been interrupted by SIGINT."""
    worker.log.info("Worker received INT or QUIT signal")

def on_exit(server):
    """Called just before the master process is initialized."""
    server.log.info("PubLink server is shutting down")

def post_fork(server, worker):
    """Called just after a worker has been forked."""
    server.log.info("Worker spawned (pid: %s)", worker.pid)

def pre_fork(server, worker):
    """Called just before a worker is forked."""
    pass

def worker_abort(worker):
    """Called when a worker received the SIGABRT signal."""
    worker.log.info("Worker received SIGABRT signal")
