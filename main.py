from github import Github 
import os,socket,json,pywifi,time

git = Github('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')

gitRepo = git.get_repo('violencedev/tubitak-project')
jsonFile = gitRepo.get_contents('main.json')
contentJSON = jsonFile.decoded_content.decode()
jsoned = json.loads(contentJSON)
coms = jsoned['main']['computers']

current_Host = socket.gethostname()

def timer(func):
    def wrapper(*args, **kwargs):
        start = time.time()
        returned = func(*args, **kwargs)
        end = time.time()
        print(f'Process finished in just {end - start} scs')
        return returned 
    return wrapper 

@timer
def updateUser(host: str) -> bool:
    global jsoned
    adaptor, nw, ip = getNetworkStats(host)
    jsoned['main']['computers'] = {'hostname': host, 'username': os.getlogin(), 'ip': ip, 'network': nw, 'adaptor': adaptor}
    return gitRepo.update_file(jsonFile.path, f"created user: {host}", json.dumps(jsoned), jsonFile.sha, branch="main")

    
def getNetworkStats(host):
    wifi = pywifi.PyWiFi()
    Iface = wifi.interfaces()[0]
    Name = Iface.name()
    Iface.scan()
    results = Iface.scan_results()
    while len(results) == 0:
        results = Iface.scan_results()
    nwName = results[0].ssid
    local_ip = socket.gethostbyname(host)
    return Name, nwName, local_ip

if current_Host in coms:
    updateUser(current_Host)
    print('Update succesfully')
else:
    updateUser(current_Host)
    print('Update succesfully')


