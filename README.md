# domain_inspector
A simple domain information gathering tool.
You'll be prompted to enter a domain, and the tool will display information about the domain.

# Features
Get IP address of the domain

Retrieve DNS records (A, AAAA, MX, NS, TXT)

Fetch WHOIS information

Find subdomains using Certificate Transparency logs

Scan for open ports using Nmap

# License

This project is licensed under the MIT License.

## Adding Path
Check your shell and with command 
```bash
echo $0

```
Edit .bashrc or zshrc 


```bash
nano ~/.bashrc

```

```bash
nano ~/.zshrc

```
Add path in the last of the file.

```bash
export PATH=$PATH:/home/(use your username here)/.local/bin

```
After adding the path and installation is done close the previous terminal and open new one to try this tool.


## How to Install

```bash
https://github.com/raven77654/domain_gathering_tool.git

```
Go to the same directory where you clone the tool and type

```bash
pip install . 

```
After completing the installtion you need to type in your terminal  

 
```bash
python3 -m projectdomain

```
Or You Can Type 

```bash
python3 -m projectdomain example.com
```


## How to uninstall the tool 
```bash
pip uninstall projectdomain

```

