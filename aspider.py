import requests
import json
import time
import argparse, re, socket
import ipaddress as ip
import itertools
import undetected_chromedriver as uc
from selenium.webdriver.common.by import By
from selenium.common.exceptions import NoSuchElementException
from selenium.common.exceptions import WebDriverException
from selenium import webdriver

# define global variables
# our cookies in securitytrails session securitytrails.com
session_cookie = 'YOU_SECURITYTRAILS_COOKIE'

# parse arguments
parser = argparse.ArgumentParser()
parser.add_argument('--asn', help='ASN list file')
parser.add_argument('--iplist', help='ip list file')
parser.add_argument('--oneip', help='one ip address')
parser.add_argument('--cidr', help='cidr list file')
parser.add_argument('--cookie', help='cookie securitytrails')
argumets = parser.parse_args()

# if the cookie argument is passed, override the variable otherwise leave as is
if argumets.cookie is not None:
    session_cookie = argumets.cookie

# global variable to store driver state
global driver

def auth_browser():
    # Authorization
    options = uc.ChromeOptions()
    options.add_argument( '--headless' )
    options.add_argument( '--auto-open-devtools-for-tabs' )
    options.add_argument( '--disable-popup-blocking' )
    driver = uc.Chrome(options = options)
    driver.get('https://securitytrails.com/app/auth/login?return=/app/account')
    driver.maximize_window()
    driver.add_cookie({
                'name': 'SecurityTrails',
                'value': session_cookie
    })
    return driver



def ip_domain(target):

    page = 1

    while True:
        
        # Open a new tab with JavaScript:
        url_variable = "https://securitytrails.com/list/ip/"+str(target)+"?page="+str(page)
        script = '''window.open("{url}","_blank");'''.format(url=url_variable)
        driver.execute_script(script)
        time.sleep(5) # wait until page has loaded

        # Switch to the last open tab:

        driver.switch_to.window(driver.window_handles[-1])
        
        # Close the previous tab:
        driver.switch_to.window(driver.window_handles[-2])


        try:
            driver.close()
            # if window close error then restart our browser driver
            # fix unknown error: failed to close window in 20 seconds
        except WebDriverException as e:
            driver.quit()
            auth_browser()
            time.sleep(10)

        # Switch to a new tab again:
        driver.switch_to.window(driver.window_handles[-1])
        time.sleep(2)
        driver.get('https://securitytrails.com/list/ip/'+str(target)+'?page='+ str(page))
        
        # check for an error on the page if the ip is empty or the results are over
        no_results = driver.find_elements(By.CSS_SELECTOR, "p.text-center.py-4.px-0.text-black.dark\\:text-white.loading-text")
        if len(no_results) > 0:
            return
        
        # parse domain results
        # fix looping the result if we have only one page in the results
        try:
            # Поиск элемента с помощью CSS-селектора
            element = driver.find_element(By.CSS_SELECTOR, 'ul.tooltip.relative.flex.ml-4')
            # If the element is found, perform actions
            # parse domains from the page
            links = driver.find_elements(By.CSS_SELECTOR, "a.link")
            num_links = len(links)
            for link in links:
                domain_name = link.text
                print(domain_name)
        # if not found, parse once and exit the function parsing will already be the next ip in the list
        except NoSuchElementException:
            links = driver.find_elements(By.CSS_SELECTOR, "a.link")
            num_links = len(links)
            for link in links:
                domain_name = link.text
                print(domain_name)  
            return

        page += 1

def cidr_to_ip(cidr):
    a = ip.ip_network(cidr)
    for target in a.hosts():
        ip_domain(target)
        

def asn_to_cidr_list():
    for line in open(argumets.asn, 'r'):  
        cidr = requests.get('https://api.hackertarget.com/aslookup/?q=' + line)
        if cidr.text == "API hackertarget count exceeded - Increase Quota with Membership":
            print("API hackertarget count exceeded - Increase Quota with Membership")
            exit()
        strong = cidr.text.split("\n")
        for i in range(cidr.text.count('\n')):
            a = re.search("^[\d]+.[\d]+.[\d]+.[\d]+[/][0-9]+", strong[i])
            if a != None:
                cidr_to_ip(a.group(0))

# запускаем драйвер
driver = auth_browser()

if argumets.asn is not None:
    asn_to_cidr_list()

elif argumets.oneip is not None:
    ip_domain(argumets.oneip)

elif argumets.iplist is not None:
    with open(argumets.iplist, 'r') as file:
        for lineip in file:
            ip_domain(lineip.strip())

elif argumets.cidr is not None:
    with open(argumets.cidr, 'r') as file:
        for linecidr in file:
            ip_domain(linecidr.strip())


