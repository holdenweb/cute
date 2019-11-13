# buildhosts =.py - build hosts table for CUTE network

import glob
import json
import os
import sys

from utils import get_addresses

verbose = True
allocating = True


def sprint(*args, **kwargs):
    if verbose:
        print(*args, **kwargs)


# Currently hardwired to the holdenwebs network. DO NOT CHECK IN!
with open("networks/holdenwebs.json") as netf:
    network = json.load(netf)
addresses = get_addresses(network["ip_addresses"])
err_ct = 0

# Prime hosts with provided data if present
try:
    with open("config/hosts.json") as f:
        addr_by_name = json.load(f)
    print("Added hosts from config/hosts.json")
except FileNotFoundError:
    addr_by_name = {}

# Iterate over hosts in config directory, either
# reading or allocating addresses as appropriate.
# Ignore directories that do not have simple names.
for file_path in glob.glob("config/*"):
    host_name = os.path.basename(file_path)
    if not os.path.isdir(file_path) or '.' in host_name:
        continue
    try:
        file_path = os.path.join(file_path, "config.json")
        with open(file_path) as inf:
            sprint(f"Processing config file for {host_name}")
            host = json.load(inf)
            if allocating:
                ip = host["ip_address"] = next(addresses)
                print(f"Allocated address {ip} to {host_name}")
                with open(file_path, "w") as outf:
                    json.dump(host, outf, indent=2)
            addr_by_name[host_name] = host["ip_address"]
    except FileNotFoundError:
        err_ct += 1
        sprint(f"%No config file for host {host_name}")

name_by_addr = {}
for name, addr in addr_by_name.items():
    if addr in name_by_addr:
        err_ct += 1
        sprint(
            f"%Conflicting names for IP address {addr}: {name_by_addr[addr]} and {name}"
        )
    name_by_addr[addr] = name

if err_ct:
    sys.exit(f"Detected {err_ct} error(s) - No hosts.py written.")

with open("hosts.py", "w") as outf:
    outf.write(
        f"""\
# hosts.py - automatically built, changes will revert on regeneration

by_name = {addr_by_name}

by_addr = {name_by_addr}"""
    )
