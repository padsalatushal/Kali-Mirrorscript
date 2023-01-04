import requests
import re
import subprocess

# Getting mirrors list 
r = requests.get('https://http.kali.org/README.mirrorlist').text
urls = re.findall(r'(?:href="http(?:s|))(.*)(?:/README")',r)[2:]
# print(urls)

hosts = []
mirrors = {}
# Getting Hostname of each of the url
for url in urls:
    hostname = url.split("//")[-1].split("/")[0].split('?')[0]
    # print(hostname)
    hosts.append(hostname)
print(hosts)

# Function for measure latency of host
def find_latency(hostname):
    # Ping the site 
    p = subprocess.Popen(['ping','-c 3', hostname], stderr=subprocess.PIPE, stdout=subprocess.PIPE).communicate()
    p = [str(x.decode('utf-8')) for x in p]
    # print(p[0])
    # Finding the latency
    if "100% packet loss" in p[0].strip():
        average = "[!] Unable to check " + hostname + " latency, potentially host block ICMP request."
    else:
        average = p[0].strip().splitlines()[-1].split('=')[1].split('/')[1]
    # print(hostname,average)
    mirrors[hostname] = str(average)

# Measuring each host latency
for i in hosts:
    find_latency(i)