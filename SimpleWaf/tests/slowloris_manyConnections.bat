@echo off
set NUM_OF_REQUESTS=20
set URL=http://mysite.com:5000/

for /l %%i in (1,1,%NUM_OF_REQUESTS%) do (
    start curl -v --header "Connection: keep-alive" %URL%
)