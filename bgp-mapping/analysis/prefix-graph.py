import pandas as pd
pd.options.display.max_rows = 200
import numpy as np
import matplotlib.pyplot as plt
import gc
import functools

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
        addrs = int('111111111111111111111111111111', 2) >> mask
        allocated_addrs += addrs
    return allocated_addrs

# load bgp data from csv
def load_data(file_name):
    cnames = ["asn","prefixes"]

    load_config = {
        "sep":"|",
        "engine":'c',
        "header":None,
        "names":cnames,
        "index_col":False,
    }
    
    return pd.read_csv(file_name, **load_config)

df = load_data("../2022-08-11/asn_prefix_mapping.csv")
prefix_count = df.groupby(['asn'], sort=False).agg(count_prefixes)
print(prefix_count)
