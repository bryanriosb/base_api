import sys
import os
from dotenv import set_key, load_dotenv


env_file_path = os.path.join('.envs', '.pro', '.django')
load_dotenv(dotenv_path=env_file_path)

print('sys.argv', sys.argv)
public_ip = sys.argv[1]
private_ip = sys.argv[2]

public_dns = f"ec2-{public_ip.replace('.', '-')}.compute-1.amazonaws.com"
print('Public IP address:', public_ip)
print('Private IP address:', private_ip)
print('Public DNS:', public_dns)

set_key(dotenv_path=env_file_path, key_to_set="PUBLIC_IPV4", value_to_set=public_ip)
set_key(dotenv_path=env_file_path, key_to_set="PRIVATE_IPV4", value_to_set=private_ip)
set_key(dotenv_path=env_file_path, key_to_set="PUBLIC_DNS", value_to_set=public_dns)
