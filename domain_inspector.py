import socket
import requests
import whois
import ssl
import subprocess
import tldextract
from OpenSSL import crypto
import dns.resolver

def resolve_domain_ip(domain):
    try:
        ip_address = socket.gethostbyname(domain)
        return ip_address
    except socket.gaierror:
        return None

def query_dns_records(domain):
    records = {}
    resolver = dns.resolver.Resolver()
    resolver.nameservers = ['8.8.8.8', '8.8.4.4']  # Google Public DNS
    for qtype in ['A', 'AAAA', 'MX', 'NS', 'TXT']:
        try:
            answers = resolver.resolve(domain, qtype, raise_on_no_answer=False)
            records[qtype] = [answer.to_text() for answer in answers]
        except dns.resolver.NoAnswer:
            records[qtype] = []
        except dns.resolver.NXDOMAIN:
            return f"No {qtype} records found."
        except dns.resolver.Timeout:
            return "DNS resolution timed out."
        except dns.exception.DNSException as e:
            return f"DNS error: {str(e)}"
    return records

def fetch_server_info(ip):
    try:
        response = requests.get(f"https://ipinfo.io/{ip}/json")
        if response.status_code == 200:
            return response.json()
        else:
            return f"Failed to retrieve server info: {response.status_code}"
    except requests.RequestException as e:
        return f"Error fetching server info: {str(e)}"

def retrieve_whois_info(domain):
    try:
        return whois.whois(domain)
    except Exception as e:
        return f"WHOIS lookup failed: {str(e)}"

def get_ssl_certificate_info(domain):
    try:
        cert = ssl.get_server_certificate((domain, 443))
        x509 = crypto.load_certificate(crypto.FILETYPE_PEM, cert)
        return {
            'Issuer': dict(x509.get_issuer().get_components()),
            'Subject': dict(x509.get_subject().get_components()),
            'Serial Number': x509.get_serial_number(),
            'Valid From': x509.get_notBefore().decode('utf-8'),
            'Valid Until': x509.get_notAfter().decode('utf-8')
        }
    except Exception as e:
        return f"SSL certificate retrieval failed: {str(e)}"

def perform_port_scan(ip):
    try:
        cmd = f"nmap -F {ip}"
        result = subprocess.run(cmd, shell=True, capture_output=True, text=True)
        if result.returncode == 0:
            return result.stdout
        else:
            return f"Port scanning failed: {result.stderr}"
    except Exception as e:
        return f"Port scanning error: {str(e)}"

def enumerate_subdomains(domain):
    try:
        subdomains = []
        ext = tldextract.extract(domain)
        base_domain = f"{ext.domain}.{ext.suffix}"
        url = f"https://crt.sh/?q=%25.{base_domain}&output=json"
        response = requests.get(url)
        if response.status_code == 200:
            data = response.json()
            subdomains = [entry['name_value'].strip() for entry in data]
        else:
            return f"Subdomain enumeration failed: {response.status_code}"
    except Exception as e:
        return f"Subdomain enumeration error: {str(e)}"
    return subdomains

def main():
    domain = input("Enter domain name: ")

    print(f"\nDomain Information for '{domain}':\n")

    ip_address = resolve_domain_ip(domain)
    if ip_address:
        print(f"IP Address: {ip_address}")

        print("\nDNS Records:")
        dns_records = query_dns_records(domain)
        if isinstance(dns_records, dict):
            for qtype, records in dns_records.items():
                if records:
                    print(f"{qtype}:")
                    for record in records:
                        print(f"  {record}")
                else:
                    print(f"No {qtype} records found.")
        else:
            print(dns_records)

        print("\nServer Information:")
        server_info = fetch_server_info(ip_address)
        if isinstance(server_info, dict):
            for key, value in server_info.items():
                print(f"{key}: {value}")
        else:
            print(server_info)

        print("\nWHOIS Information:")
        whois_info = retrieve_whois_info(domain)
        print(whois_info)

        print("\nSSL Certificate Details:")
        ssl_info = get_ssl_certificate_info(domain)
        if isinstance(ssl_info, dict):
            for key, value in ssl_info.items():
                print(f"{key}: {value}")
        else:
            print(ssl_info)

        print("\nPort Scanning:")
        port_scan_result = perform_port_scan(ip_address)
        print(port_scan_result)

        print("\nSubdomain Enumeration:")
        subdomains = enumerate_subdomains(domain)
        if isinstance(subdomains, list):
            for subdomain in subdomains:
                print(subdomain)
        else:
            print(subdomains)

    else:
        print(f"Unable to resolve IP address for '{domain}'")

if __name__ == "__main__":
    main()
