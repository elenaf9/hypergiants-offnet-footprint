import pandas as pd
pd.options.display.max_rows = 200
import numpy as np
import matplotlib.pyplot as plt
import gc
import functools
import sys

def count_prefixes(x):
    x = functools.reduce(lambda acc, curr: acc + curr, x, '')
    allocated_addrs = 0
    last = ''
    prefixes = x.split(' ')
    prefixes.sort()
    for prefix in prefixes:
        if prefix == '':
            continue
        [ip, mask] = prefix.split('/')
        if last == ip:
            # Skip if the ip already appeared
            # Because the list is sorted same Ip appear directly after each other.
            # The one with the lower mask appears first.
            continue
        last = ip
        mask = int(mask, 10)
        addrs = (int('11111111'+'11111111'+'11111111'+'11111111', 2) >> mask) + 1 
        # Subtract 2 because 2 addresses are unusable per IP-range:
        # 1 is the network address and 1 is the broadcast address
        allocated_addrs += (addrs -2)
    return allocated_addrs

# load bgp data from csv
def load_data(file_name):
    cnames = ["asn","allocated addresses"]

    load_config = {
        "sep":"|",
        "engine":'c',
        "header":None,
        "names":cnames,
        "index_col":False,
        "compression":"zip"
    }
    return pd.read_csv(file_name, **load_config)

for date in ['2022-08-11', '2022-08-25']:
    print("\n" + date + ":\n")
    df = load_data("./" + date + "/asn_prefix_mapping.zip")
    df["asn"] = df["asn"].map(lambda x: x.strip())
    if len(sys.argv) > 1:
        df = df[df["asn"] == sys.argv[1]]
    prefix_count = df.groupby(['asn'], sort=False).agg(count_prefixes)
    print(prefix_count)
