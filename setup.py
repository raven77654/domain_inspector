from setuptools import setup, find_packages

setup(
    name="domain_inspector",
    version="0.1",
    packages=find_packages(),
    install_requires=[
        "dnspython",
        "python-whois",
        "python-nmap",
        "requests"
    ],
    entry_points={
        'console_scripts': [
            'domain_inspector=domain_inspector:main',
        ],
    },
    author="Sadia Kamal",
    author_email="sadiakamal2468@gmail.com",
    description="A tool to inspect domain information including IP address, DNS records, WHOIS information, subdomains, MAC addresses, and open ports",
    long_description=open('README.md').read(),
    long_description_content_type="text/markdown",
    url="https://github.com/raven77654/domain_gathering_too",
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
)
