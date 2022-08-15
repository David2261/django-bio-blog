def application(env, start_response):
    start_response('200 OK', [('Content-Type','text/html')])
    return [b"Hello World"] # python3


"""
Feed Back

*** Starting uWSGI 2.0.20 (64bit) on [Mon Aug 15 15:39:34 2022] ***

compiled with version: 10.2.1 20210110 on 15 August 2022 12:36:31
os: Linux-5.10.16.3-microsoft-standard-WSL2 #1 SMP Fri Apr 2 22:23:49 UTC 2021
nodename: Lenovo-PC
machine: x86_64
clock source: unix
detected number of CPU cores: 2
current working directory: /mnt/d/Django/django-bio-blog/bioblog
detected binary path: /mnt/d/Django/django-bio-blog/venv_linux/bin/uwsgi
!!! no internal routing support, rebuild with pcre support !!!

*** WARNING: you are running uWSGI without its master process manager ***
your processes number limit is 5955
your memory page size is 4096 bytes
detected max file descriptor number: 1024
lock engine: pthread robust mutexes
thunder lock: disabled (you can enable it with --thunder-lock)
probably another instance of uWSGI is running on the same address (:8000).
bind(): Address already in use [core/socket.c line 769]

"""
