import random
import string
import requests
cookies = {
    'PHPSESSID': '85f83b380acc276f6025f49d8685e479'  # Replace with your PHP session ID
}
def generate_random_string(length=25):
    characters = string.ascii_letters + string.digits  # 'a-z', 'A-Z', '0-9'
    return ''.join(random.choices(characters, k=length))

def get_new_bracod():
    url = "https://challenges.cyber.org.il/ke/"
    requests.get(url,cookies=cookies)
def send_req():
    url = "https://challenges.cyber.org.il/ke/"
    headers = {
        "Host": "challenges.cyber.org.il",
        "Cache-Control": "max-age=0",
        "Accept-Language": "he-IL,he;q=0.9",
        "Origin": "http://challenges.cyber.org.il",
        "Content-Type": "application/x-www-form-urlencoded",
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/131.0.6778.86 Safari/537.36",
        "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7",
        "Referer": "http://challenges.cyber.org.il/ke/",
        "Accept-Encoding": "gzip, deflate, br",
        "Connection": "keep-alive"
    }
    cookies = {"PHPSESSID": "85f83b380acc276f6025f49d8685e479"}  # Use your actual PHPSESSID

    # Generate random CAPTCHA
    random_captcha = generate_random_string(25)  # Adjust length as needed
    data = {
        "captcha": random_captcha,
        "submit": "שליחה",  # URL-decoded Hebrew "Submit"
        "token": "NRosiJhw0qiNhx5OnSkQiKRUXBbFhNy1"  # Use actual token from response if dynamic
    }

    response = requests.post(url, headers=headers, cookies=cookies, data=data)

    if response.status_code == 200:
        print("POST successful!")
        print(response.text)  # Print or process the response
    else:
        print(f"POST failed with status code {response.status_code}")
get_new_bracod()
