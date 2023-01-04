import requests
import re

# Getting mirrors list 
r = requests.get('https://http.kali.org/README.mirrorlist').text
urls = re.findall(r'(?:href="http(?:s|))(.*)(?:/README")',r)[2:]
# print(urls)

hosts = []
# Getting Hostname of each of the url
for url in urls:
    hostname = url.split("//")[-1].split("/")[0].split('?')[0]
    # print(hostname)
    hosts.append(hostname)
print(hosts)

