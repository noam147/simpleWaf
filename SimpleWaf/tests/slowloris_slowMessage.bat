@echo off

curl -X POST http://mysite.com:5000 -d "key1=value1&key2=value2" --limit-rate 1B
REM --limit-rate 1B means limiting the upload speed to 1 byte per second
pause
