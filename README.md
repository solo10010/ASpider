
```bash                                                                                 
         █████╗ ███████╗██████╗ ██╗██████╗ ███████╗██████╗ 
        ██╔══██╗██╔════╝██╔══██╗██║██╔══██╗██╔════╝██╔══██╗
        ███████║███████╗██████╔╝██║██║  ██║█████╗  ██████╔╝
        ██╔══██║╚════██║██╔═══╝ ██║██║  ██║██╔══╝  ██╔══██╗
        ██║  ██║███████║██║     ██║██████╔╝███████╗██║  ██║
        ╚═╝  ╚═╝╚══════╝╚═╝     ╚═╝╚═════╝ ╚══════╝╚═╝  ╚═╝                                                
```
# RESUME

**ASpider** this is a utility for reconnaissance of the assets of organizations by their autonomous system number (AS, ASN), the utility requires a file with a list of organizations ASN, you can get the AS number by IP address with the following command 

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
chmod +x *.py
python3 aspider.py
```

# USAGE:

```bash
# asn list
cat asn.txt
AS15169
AS32934
# command to get domains and subdomains
python3 aspider.py -a asn.txt
# command to get domains and subdomains and live servers
python3 aspider.py -a asn.txt -s
```

# OPTIONS:

| Flag | Description |
|------|-------------|
| -h, --help | show this help message and exit |
| -a, --asn | file list of autonomous systems (AS ,ASN ) |
| -s, --server | Check IP for live servers |