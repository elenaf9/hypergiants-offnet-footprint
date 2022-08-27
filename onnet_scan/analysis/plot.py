import matplotlib.pyplot as plt
import numpy as np
import pandas as pd


def load_data(file_name):
    return pd.read_csv(file_name, sep='\t', engine='c')

subject_certs = load_data('subject_cert_count.csv').filter(['subject', 'count']).rename(columns={'count': 'count_cert_found'})

headers = load_data('header_per_subject.csv')
headers = headers[headers['header_key']=='x_fb_debug'].filter(['subject', 'count']).groupby('subject').sum().rename(columns={'count': 'count_header_found'})

data = subject_certs.merge(headers, on='subject', how='outer', validate='one_to_one')
data.rename(columns = {'count_header_found':'x_fb_debug header found', 'count_cert_found': 'TLS certificate found'}, inplace = True)


ax = data.plot.barh(x='subject', xlabel='Certificate Common Name')
ax.tick_params(axis='x')
plt.xlabel('Number of hosts')
plt.tight_layout()
plt.savefig("plots/onnet_certs_headers.png")

