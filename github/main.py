import time
from turtle import update 
from bs4 import BeautifulSoup
from selenium import *
import pywifi
import requests 
import socket
import json
import os

username = 'violencedev'
password = 'furkan2005F'



def getNetworkName(): 
    wifi = pywifi.PyWiFi()
    Iface = wifi.interfaces()[0]
    Name = Iface.name()
    Iface.scan()
    results = Iface.scan_results()
    while len(results) == 0:
        results = Iface.scan_results()
    nwName = results[0].ssid
    host = socket.gethostname()
    local_ip = socket.gethostbyname(host)
    return Name, nwName, local_ip, host 

def getData():
    request = requests.get('https://github.com/violencedev/tubitak-project/blob/main/main.json', 'html.parser', verify=False)
    soup = BeautifulSoup(request.text)
    tablebody = soup.find('tr')
    tabledatas = tablebody.find_all('td')
    jsonFILE = tabledatas[-1].text
    return jsonFILE

JSON_DATA = json.loads(getData())

def addData() -> None:
    from selenium import webdriver
    from selenium.webdriver.common.keys import Keys
    driverPath = os.path.dirname(os.path.realpath(__file__)) + '\chromedriver.exe'
    browser = webdriver.Chrome(driverPath)

    browser.get(r'https://github.com/login')

    usernameBox = browser.find_element_by_xpath('//*[@id="login_field"]')
    usernameBox.send_keys(username)

    passwordBox = browser.find_element_by_xpath('//*[@id="password"]')
    passwordBox.send_keys(password)

    submitBtn = browser.find_element_by_xpath('//*[@id="login"]/div[4]/form/div/input[12]')
    submitBtn.click()
    time.sleep(3)

    browser.get('https://github.com/violencedev/tubitak-project/blob/main/main.json')

    tablebody = browser.find_elements_by_css_selector('tr td')
    content = tablebody[-1].text

    editBtn = browser.find_element_by_xpath('//*[@id="repo-content-pjax-container"]/div/div[4]/div[1]/div[2]/div[2]/form[1]/button')
    editBtn.click()

    time.sleep(1)
    body = browser.find_element_by_css_selector('body')
    input_ = browser.find_element_by_xpath('//*[@id="code-editor"]/div[1]/pre/span')
    body.send_keys(Keys.TAB)
    input_.send_keys(Keys.CONTROL + 'a')
    input_.send_keys(Keys.DELETE + update_datas())
    time.sleep(2)

    commitBtn = browser.find_element_by_xpath('//*[@id="submit-file"]')
    commitBtn.click()

    browser.get('https://github.com/violencedev/tubitak-project/blob/main/main.json')
    time.sleep(5)
def update_datas():
    global JSON_DATA
    adaptor, network, ip, host = getNetworkName()
    JSON_DATA['computers'][host] = {'adaptor': adaptor, 'network': network, 'ip': ip, 'host': host}
    return json.dumps(JSON_DATA)

addData()
