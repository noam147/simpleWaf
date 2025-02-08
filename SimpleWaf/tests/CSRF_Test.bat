@echo off
setlocal enabledelayedexpansion

:: Define the target server
set TARGET_URL=http://mysite.com:5000/

:: Step 1: Send GET request to fetch CSRF token and save cookies
echo Sending GET request to fetch CSRF token...
curl -s -D headers.txt -c cookies.txt "%TARGET_URL%" > get_response.txt

:: Print GET response body
echo GET Response Body:
type get_response.txt

:: Print GET response status code
for /f "tokens=2 delims= " %%a in ('findstr /r "^HTTP/" headers.txt') do set STATUS_CODE_GET=%%a
echo GET Response Status Code: %STATUS_CODE_GET%

:: Extract CSRF token from cookies
set XSRF_TOKEN=
for /f "tokens=7" %%a in ('findstr _xsrf cookies.txt 2^>nul') do set XSRF_TOKEN=%%a
echo Extracted CSRF Token: "%XSRF_TOKEN%"

:: Step 2: Send POST request WITHOUT CSRF token
echo Sending POST request WITHOUT CSRF token...
curl -s -D post_headers_no_token.txt -X POST "%TARGET_URL%/protected" -d "test=data" > post_no_token.txt

:: Print POST response body (without CSRF token)
echo POST Response without CSRF token:
type post_no_token.txt

:: Print POST response status code
for /f "tokens=2 delims= " %%a in ('findstr /r "^HTTP/" post_headers_no_token.txt') do set STATUS_CODE_POST_NO_TOKEN=%%a
echo POST Response Status Code (without CSRF token): %STATUS_CODE_POST_NO_TOKEN%

:: Step 3: Send POST request WITH CSRF token
echo Sending POST request WITH CSRF token...
curl -s -D post_headers_with_token.txt -b cookies.txt -X POST "%TARGET_URL%/protected" ^
  -H "X-XSRFToken: %XSRF_TOKEN%" -d "test=data" > post_with_token.txt

:: Print POST response body (with CSRF token)
echo POST Response with CSRF token:
type post_with_token.txt

:: Print POST response status code
for /f "tokens=2 delims= " %%a in ('findstr /r "^HTTP/" post_headers_with_token.txt') do set STATUS_CODE_POST_WITH_TOKEN=%%a
echo POST Response Status Code (with CSRF token): %STATUS_CODE_POST_WITH_TOKEN%

endlocal
pause
