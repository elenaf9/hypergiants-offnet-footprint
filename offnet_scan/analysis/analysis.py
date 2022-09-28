import json

import pandas as pd

pd.options.display.max_rows = 200
import functools
import gc
import hashlib
import subprocess
import sys

import matplotlib.pyplot as plt
import numpy as np


def map(row):
    ip = row["ip"]
    cert = row["cert"].split('"certificate": {"raw": "')[1].split('", ')[0]
    proc = subprocess.run(['sh', '../../bgp-mapping/resolve.sh', 'whois', ip], capture_output=True)
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
    # mapped = df.apply(map, axis=1, result_type='expand')
    return df

file = './2022-08-21/scans_ready/output_global.txt'
df = load_data(file)
print(df.describe())
print(df['status'].unique())
print(df['status'].value_counts())
print(df[df['status'] == 'success-meta-header'])
for cert in df[df['status'] == 'success-meta-header']['cert']:
    parsed = json.loads(cert)
    print(parsed["data"]["http"]["result"]["response"]["request"][
            "tls_log"]["handshake_log"]["server_certificates"]["certificate"]["parsed"]['subject']["common_name"])
# per_asn = df.groupby(["asn"], sort=False).aggregate(count).sort_values(by=['ip'], ascending=False)
# print(per_asn.to_string())
# per_cert = df.groupby(["cert"], sort=False).size().reset_index().sort_values(by=[0], ascending=False)
# print(per_cert.head(1000))
