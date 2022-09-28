import gc

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd


def load_data(file_name):
    load_config = {
        "delim_whitespace": True,
        "engine":'c',
        "index_col":False,
    }
    return pd.read_csv(file_name, **load_config)

ases = load_data('hosts_per_AS.csv')
ases = ases[ases['asn']!='AS32934'].filter(items=['hosts', 'asn'])

# ax = plt.hist(ases['hosts'], cumulative=True, label='CDF',
#          histtype='step', alpha=0.8, bins=1000)
ases['hosts'].plot.line(legend=False, xlabel='Top AS by number of hosts', ylabel='# of hosts', grid=True)
# ax.set_ylabel("# of hosts")
# fig = ax.get_figure()
plt.savefig("plots/hosts_per_AS.png")

ax = ases.head(100).plot.bar(x='asn',y='hosts' )
ax.set_ylabel("# of hosts")
ax.set_xlabel("ASes")
ax.tick_params(axis='x')
fig = ax.get_figure()
plt.savefig("plots/host_distribution_top_100.png")

ax = ases[ases['hosts']>=100].plot.bar(x='asn',y='hosts',rot=35)
ax.set_ylabel("# of hosts")
ax.tick_params(axis='x')
fig = ax.get_figure()
plt.savefig("plots/hosts_per_AS_min_100.png")

