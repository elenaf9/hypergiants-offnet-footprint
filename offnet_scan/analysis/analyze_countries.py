import pandas as pd
pd.options.display.max_rows = 200
import numpy as np
import matplotlib.pyplot as plt
import gc
import functools
import sys
import subprocess
import hashlib

def map(row):
    asn = row["asn"]
    hosts = row["hosts"]
    if asn == 'AS32934':
        return pd.Series([asn, 'ONNET', 0], index=['asn', 'country', 'hosts'])
    proc = subprocess.run(['sh', '../bgp-mapping/resolve.sh', 'whois_country', asn], capture_output=True)
    country = proc.stdout.decode('ascii')[:-1]
    return pd.Series([asn, country, hosts], index=['asn', 'country', 'hosts'])

def count(values):
    if values.name == 'cert':
        return values.nunique()
    else:
        return values.count()

# load bgp data from csv
def load_data(file_name):
    cnames = ["i","asn", "hosts"]

    load_config = {
        "delim_whitespace": True,
        "engine":'c',
        "index_col":False,
    }
    return pd.read_csv(file_name, **load_config).apply(map, axis=1, result_type='expand')

df = load_data('test.txt')
grouped = df.filter(items=['country', 'hosts']).groupby(["country"], sort=False)
print('\nASes per country:\n', grouped.count().sort_values(by=['hosts'], ascending=False))
print('\nhosts per country:\n', grouped.sum().sort_values(by=['hosts'], ascending=False))
print(df.to_string())