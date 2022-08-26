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
    ip = row["ip"]
    cert = row["cert"].split('"certificate": {"raw": "')[1].split('", ')[0]
    proc = subprocess.run(['sh', '../bgp-mapping/resolve.sh', 'whois', ip], capture_output=True)
    asn = proc.stdout.decode('ascii')[:-1]
    return pd.Series([ip, asn, cert], index=['ip', 'asn', 'cert'])

def count(values):
    if values.name == 'cert':
        return values.nunique()
    else:
        return values.count()

# load bgp data from csv
def load_data(file_name):
    cnames = ["ip","status", "cert"]

    load_config = {
        "sep":"|",
        "engine":'c',
        "header":None,
        "names":cnames,
        "index_col":False,
    }
    df = pd.read_csv(file_name, **load_config)
    df = df[pd.notna(df["cert"])]
    mapped = df.apply(map, axis=1, result_type='expand')
    return mapped

dfs = []
for i in range(0, 10):
    file = './2022-08-21/scans_ready/output_global_0' + str(i) +'.txt'
    df = load_data(file)
    dfs.append(df)
for i in range(10, 20):
    file = './2022-08-21/scans_ready/output_global_' + str(i) +'.txt'
    df = load_data(file)
    dfs.append(df)
df = pd.concat(dfs)
per_asn = df.groupby(["asn"], sort=False).aggregate(count).sort_values(by=['ip'], ascending=False)
print(per_asn.to_string())
per_cert = df.groupby(["cert"], sort=False).size().reset_index().sort_values(by=[0], ascending=False)
print(per_cert.head(1000))