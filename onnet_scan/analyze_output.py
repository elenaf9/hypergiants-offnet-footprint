import pandas as pd
pd.options.display.max_rows = 200
import numpy as np
import matplotlib.pyplot as plt
import gc
import functools
import json


def select(row):
    mapped_columns = {
        'ip': 'ip',
        'http.status': 'status', 
        'http.result.response.request.tls_log.handshake_log.server_certificates.certificate.raw':'certificate',
        'http.result.response.request.tls_log.handshake_log.server_certificates.certificate.parsed.issuer.common_name':'issuer',
        'http.result.response.request.tls_log.handshake_log.server_certificates.certificate.parsed.subject.common_name':'subject',
        'http.result.response.headers.unknown':'header_key',
    }
    data = pd.json_normalize(row['data'])
    data['ip'] = row['ip']
    include = []
    for key in mapped_columns.keys():
        if key in data.columns:
            if key == 'http.result.response.headers.unknown':
                keys = list(map(lambda x: x['key'], data[key][0]))
                keys.sort()
                keys = functools.reduce(lambda acc, curr: acc + ' ' + curr, keys, '')
                include.append(keys)
            else:
                value = data[key][0]
                if isinstance(value, list):
                    value.sort()
                    value = functools.reduce(lambda acc, curr: acc + ' ' + curr, value, '')
                include.append(value)
        else:
            include.append("")
    return pd.Series(include, index=mapped_columns.values())


# load bgp data from csv
def load_data(file_name):
    cnames = ["asn","prefixes"]

    load_config = {
        "orient":"records",
        "typ":"frame",
        "lines":True,
        "compression":"zip"
    }
    df = pd.read_json(file_name, **load_config)
    df = df.apply(select, axis=1, result_type='expand')
    return df

df = load_data("./2022-08-16T13/output.zip")

# Different status
status = df.groupby(["status"]).size().reset_index()
print("\nstatus:\n", status)

success = df[df['certificate'].str.len() > 0]

# Unique issuer sn
print("\nUnique issuer sns:\n", success[["issuer"]].nunique().to_frame(name="issuer nunique"))
# Analyze certificates
certs = success.groupby(["subject", "certificate"]).size().reset_index()
# Unique certificates per subject cn
print("\nUnique subjects and certificates:\n", certs.nunique().to_frame(name="nunique"))
# Print certificates
print("\ncertificates:\n", certs)

# Analyze http header keys
header_keys = success.groupby(["header_key"]).size().reset_index()
print("\nheader_keys:\n", header_keys)





