import requests
import json
import argparse, re, socket
import ipaddress as ip

parser = argparse.ArgumentParser()

parser.add_argument('-a', '--asn' , help='list ASN.txt')
parser.add_argument('-s', '--server' , help='server ip', action="store_true")

argumets = parser.parse_args()



def ip_domain(target):
    # check server
    if argumets.server:
        conn = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        socket.timeout('300')
        host = str(target)
        port = 80
        try:
            conn.connect((host, port))
        except:
            pass
        print(str(target))
    # resul domain
    getdom = requests.get("https://sonar.omnisint.io/reverse/" + str(target))
    if "null" != getdom.text:
        result = json.loads(getdom.text)
        for domain in result:
            if domain != "error":
                print(domain)

def cidr_to_ip(cidr):
    a = ip.ip_network(cidr)
    for target in a.hosts():
        ip_domain(target)
        

def asn_to_cidr_list():
    for line in open(argumets.asn, 'r'):  
        cidr = requests.get('https://api.hackertarget.com/aslookup/?q=' + line)
        if cidr.text == "API count exceeded - Increase Quota with Membership":
            print("API count exceeded - Increase Quota with Membership")
            exit()
        strong = cidr.text.split("\n")
        for i in range(cidr.text.count('\n')):
            a = re.search("^[\d]+.[\d]+.[\d]+.[\d]+[/][0-9]+", strong[i])
            if a != None:
                cidr_to_ip(a.group(0))
                    
if argumets.asn != "":
    asn_to_cidr_list()

