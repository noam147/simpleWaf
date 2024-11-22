
# function needs to be rewriten, used for testing
"""
the function fetches the websites ip from the DB
:param hostName: the websites domain name
:return: the websites ip as str | if the website isnt in the DB returns None
"""
def getWebsiteIp(hostName: str) -> str:
    hostNameToIp = {'mysite.com': '127.0.0.1'}
    if hostName not in hostNameToIp:
        return None
    return hostNameToIp[hostName]