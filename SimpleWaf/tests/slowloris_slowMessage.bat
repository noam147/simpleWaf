@echo off

curl -X POST http://mysite.com:5000 -d "key1=value1&key2=value2" --limit-rate 1B

pause
