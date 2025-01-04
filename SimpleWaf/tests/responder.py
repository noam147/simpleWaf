import requests
def check():
    for i in range(5):
        yield i
a = check()
for i in a:
    print(i)
# Example of converting hexadecimal to an IP address (assuming it's an IP address)
hex_value = '0xc0a25b29a0'

# Remove '0x' prefix for conversion
hex_value = hex_value[2:]

# Convert the hex string to decimal
decimal_value = int(hex_value, 16)

# Convert to IP address format (if it's an IP address)
ip_address = ".".join([str((decimal_value >> (8 * i)) & 0xFF) for i in range(4)][::-1])
print(f"Converted IP address: {ip_address}")

url = "https://challenges.cyber.org.il/au/"
#response = requests.get(url)
#print(response.text)
#check wire  shark for addinial msgs that going from the server to client vice versa
import requests
from bs4 import BeautifulSoup, Comment
import re
# Send request to the website
url = "http://challenges.cyber.org.il/au"  # Replace with your target website
cookies = {
    'PHPSESSID': '85f83b380acc276f6025f49d8685e479'  # Replace with your PHP session ID
}
response = requests.get(url,cookies=cookies)
print(response.text)
# Parse the page content
soup = BeautifulSoup(response.text, 'html.parser')

comments = soup.find_all(string=lambda text: isinstance(text, Comment))

# Regex pattern to match the comment "Page generated in: <time> seconds!"
pattern = r"Page generated in: ([\d\.]+) seconds"

# Search each comment for the pattern
for comment in comments:
    # Try to match the pattern in the comment
    match = re.search(pattern, comment)
    if match:
        # Extract the time value (in seconds)
        generated_time = match.group(1)
        print(f"Page generation time: {generated_time} seconds")