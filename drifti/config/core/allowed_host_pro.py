import os

# It is required to avoid allowed hosts error in EC2 runtime
public_ip = os.getenv('PUBLIC_IPV4')
private_ip = os.getenv('PRIVATE_IPV4')
public_dns = os.getenv('PUBLIC_DNS')


ALLOWED_HOSTS = [
    'driftibot.com',
    '.driftibot.com',
    'lb-pro-driftibot-asg-1033146035.us-east-1.elb.amazonaws.com',
    '.lb-pro-driftibot-asg-1033146035.us-east-1.elb.amazonaws.com',
    '54.243.99.74',  # Loadbalancer
    '34.233.52.55',  # Loadbalancer
    '54.80.234.228',  # LoadBalancer
    '34.202.23.160',  # Loadbalancer
    '52.23.92.243',  # Loadbalancer
    '52.2.195.127',  # Loadbalancer
    '.aitopstaff.com',
    'aitopstaff.com',
    public_ip,
    private_ip,
    public_dns,
]

CSRF_TRUSTED_ORIGINS = [
    'https://driftibot.com/*',
    'https://*.driftibot.com/*',
    'https://driftibot.web.app',
    'http://lb-pro-driftibot-asg-1033146035.us-east-1.elb.amazonaws.com/*',  # Loadbalancer
    'http://*.lb-pro-driftibot-asg-1033146035.us-east-1.elb.amazonaws.com/*', # Loadbalancer
    'http://54.243.99.74',  # Loadbalancer
    'http://34.233.52.55',  # Loadbalancer
    'http://54.80.234.228',  # Loadbalancer
    'http://34.202.23.160',  # Loadbalancer
    'http://52.23.92.243',  # Loadbalancer
    'http://52.2.195.127',  # Loadbalancer
    'https://aitopstaff.com/*',
    'https://*.aitopstaff.com/*',
    f'http://{public_ip}/',
    f'http://{private_ip}/',
    f'http://{public_dns}/',
]

CORS_ALLOWED_ORIGIN_REGEXES = [
    r"^https://\w+\.driftibot\.com$",
    r"^https://\w+\.aitopstaff\.com$",
]
