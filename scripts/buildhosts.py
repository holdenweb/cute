# buildhosts =.py - build hosts table for CUTE network

import glob
import json
import os

addr_by_name = {}
name_by_addr = {}

try:
    with open('templates/hosts.json') as f:
        addr_by_name.update(json.load(f))
    print("Added hosts from templates/hosts.json")
except FileNotFoundError:
    pass

for file_path in glob.glob('templates/*'):
    if not os.path.isdir(file_path):
        continue
    dir_name = os.path.basename(file_path)
    file_path = os.path.join(file_path, "config.json")
    print(f"Opening {file_path} as {dir_name}")
    with open(file_path) as inf:
        host = json.load(inf)
        addr_by_name[dir_name] = host['ip_address']

for name, addr in addr_by_name.items():
    if addr in name_by_addr:
        sys.exit(f"Conflicting names for IP address {addr}: {name_by_addr[addr]} and {name}")
    name_by_addr[addr] = name

with open('hosts.py', 'w') as outf:
    outf.write(f"""\
# hosts.py - automatically built, changes will be reverted

by_name = {addr_by_name}

by_addr = {name_by_addr}""")
