import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import gc


def load_data(file_name):
    load_config = {
        "delim_whitespace": True,
        "engine":'c',
        "index_col":False,
    }
    return pd.read_csv(file_name, **load_config)

subject_certs = load_data('subject_cert_count.csv')

headers = load_data('header_per_subject.csv')
headers = headers[headers['header_key']=='x_fb_debug'].filter(items=['subject', '0']).groupby('subject').sum()
print(headers.to_string())


data = subject_certs.merge(headers, on='subject', how='outer', validate='one_to_one')
data.rename(columns = {'0':'x_fb_debug header', 'count': 'TLS hosts'}, inplace = True)

ax = data.plot.bar(x='subject')
ax.tick_params(axis='x', labelsize=8)
plt.tight_layout()
plt.savefig("plots/onnet_certs_headers.png")

