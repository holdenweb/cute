# utils.py - CUTE network utilities.

import ipaddress


def get_addresses(st):
    "Returns the addresses defined in sequence of runs."
    ranges = []
    # Split string into individual runs
    runs = [s.strip() for s in st.split(",")]
    for run in runs:
        parts = run.split("-")
        if len(parts) == 1:
            first = last = parts[0]
        elif len(parts) == 2:
            first, last = parts
            # Number of dots in second part determines
            # how much of first part is used to infill
        else:
            raise ValueError(f"Too many parts in run '{run}'")
        last = ".".join(first.split(".")[: -len(last.split("."))] + [last])
        for address_range in ipaddress.summarize_address_range(
            ipaddress.IPv4Address(first), ipaddress.IPv4Address(last)
        ):
            for address in address_range:
                yield str(address)


if __name__ == "__main__":
    st = "192.168.1.50, 192.168.1.20-40, 192.168.1.64-2.63"
    for address in get_addresses(st):
        print(address)
