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

ases = load_data('hosts_per_AS.csv').filter(items=['asn', 'hosts'])
ases = ases[ases['asn']!='AS32934']

ax = ases.plot.line(x='asn')
ax.set_ylabel("Hosts")
fig = ax.get_figure()
plt.savefig("plots/hosts_per_AS.png")

ax = ases.head(100).plot.bar(x='asn',y='hosts' )
ax.set_ylabel("Hosts")
ax.set_xlabel("ASes")
ax.tick_params(axis='x', labelsize=0)
fig = ax.get_figure()
plt.savefig("plots/host_distribution_top_100.png")

ax = ases[ases['hosts']>=100].plot.bar(x='asn',y='hosts',rot=35)
ax.set_ylabel("Hosts")
ax.tick_params(axis='x', labelsize=10)
fig = ax.get_figure()
plt.savefig("plots/hosts_per_AS_min_100.png")

