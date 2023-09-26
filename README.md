
```bash                                                                                 
         █████╗ ███████╗██████╗ ██╗██████╗ ███████╗██████╗ 
        ██╔══██╗██╔════╝██╔══██╗██║██╔══██╗██╔════╝██╔══██╗
        ███████║███████╗██████╔╝██║██║  ██║█████╗  ██████╔╝
        ██╔══██║╚════██║██╔═══╝ ██║██║  ██║██╔══╝  ██╔══██╗
        ██║  ██║███████║██║     ██║██████╔╝███████╗██║  ██║
        ╚═╝  ╚═╝╚══════╝╚═╝     ╚═╝╚═════╝ ╚══════╝╚═╝  ╚═╝                                                
```
# RESUME

**ASpider** The main task of this utility is to get the domains that have this IP in A records by IP address, the utility takes as input a file with an ASN list, CIDR, or a list of IPs from which you need to get domain names, as well as subdomains.

The script itself works through the securitytrails website (due to the death of the sonar.omnisint.io project), using selenium and undetected_chromedriver, bypassing the blocking of cloudflare service bots, this script has successfully collected 77,000 domains by ASN.

```bash

whois -h whois.cymru.com -- "-v 64.233.164.102"

# output command

AS      | IP               | BGP Prefix          | CC | Registry | Allocated  | AS Name
15169   | 64.233.164.102   | 64.233.164.0/24     | US | arin     | 2003-08-18 | GOOGLE, US

```

**AS numbers must be in the file in the form AS15169, each AS number must be on a new line.**

**Find lists of IP address ranges by ASN number**

```bash

whois -h whois.radb.net -- "-i origin AS32934" | grep 'route:'

route:      69.63.176.0/20
route:      66.220.144.0/20
route:      66.220.144.0/21
...

```
**get a list of subdomain domains by IP address**
```bash

curl https://sonar.omnisint.io/reverse/140.82.121.4

["git-api.com","lb-140-82-121-4-fra.github.com","ngahon.ga"]%  

```

# INSTALLATION:

```bash
git clone https://github.com/solo10010/ASpider
cd ASpider
pip3 install requirements.txt
pip install undetected-chromedriver -U
chmod +x *.py
python3 aspider.py --help
```
# OPTIONS:

| Flag | Description |
|------|-------------|
| -h, --help | show this help message and exit |
| --asn | ASN list file |
| --iplist | ip list file |
| --oneip | one ip address |
| --cidr | cidr list file |
| --cookie | cookie securitytrails |

# USAGE ASN LIST:

```bash
# asn list
cat asn.txt
AS15169
AS32934
# command to get domains and subdomains
python3 aspider.py --asn asn.txt --cookie "YOU_SECURITYTRAILS_COOKIE"
```

# USAGE CIDR LIST:

```bash
# cidr list
cat cidr.txt
185.116.192.0/24
185.125.88.0/24
194.146.41.0/24
# command to get domains and subdomains
python3 aspider.py --cidr cidr.txt --cookie "YOU_SECURITYTRAILS_COOKIE"
```

# USAGE IP LIST:

```bash
# ip list
cat iplist.txt
185.98.5.234
194.4.58.140
185.98.5.235
# command to get domains and subdomains
python3 aspider.py --iplist iplist.txt --cookie "YOU_SECURITYTRAILS_COOKIE"
```

# USAGE ONE IP:

```bash
python3 aspider.py --oneip 185.98.5.234 --cookie "YOU_SECURITYTRAILS_COOKIE"
```
