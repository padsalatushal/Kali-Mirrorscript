import requests
import time
import re
import subprocess
import threading

start = time.perf_counter()

# Getting mirrors list 
r = requests.get('https://http.kali.org/README.mirrorlist')

if r.status_code!=200:
    exit()

urls = re.findall(r'(?:href="http(?:s|))(.*)(?:/README")',r.text)[2:]
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
    # Ping the host
    p = subprocess.Popen(['ping','-c 3', hostname], stderr=subprocess.PIPE, stdout=subprocess.PIPE).communicate()
    p = [str(x.decode('utf-8')) for x in p]
    # print(p[0])
    # Finding the latency
    if "100% packet loss" in p[0].strip():
        # average = "[!] Unable to check " + hostname + " latency, potentially host block ICMP request."
        pass
        # average  = 99999
    else:
        average = p[0].strip().splitlines()[-1].split('=')[1].split('/')[1]
        print(hostname,average)
        mirrors[hostname] = float(average)

threads = []
# Measuring each host latency
# Create Thread for each host
for host in hosts:
    t = threading.Thread(target=find_latency,args=(host,))
    threads.append(t)
    t.start()

# wait for all threads to complete
for t in threads:
    t.join()


# Sorting the host by latency
sorted_dictionary = dict(sorted(mirrors.items(), key=lambda item: item[1]))
# print(sorted_dictionary)

# Selecting Best mirror with lowest latency
first_element = next(iter(sorted_dictionary))
# print(first_element)

end = time.perf_counter()
print(f"final time = {end-start}")