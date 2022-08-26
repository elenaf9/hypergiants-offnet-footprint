import geopandas as gpd
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import gc
from mpl_toolkits.axes_grid1 import make_axes_locatable


def load_data(file_name):
    load_config = {
        "delim_whitespace": True,
        "engine":'c',
        "index_col":False,
    }
    return pd.read_csv(file_name, **load_config)

world = gpd.read_file(gpd.datasets.get_path('naturalearth_lowres')).filter(items=['iso_a3', 'geometry'])
mapping = pd.read_csv("country_code_mapping.csv").filter(items=['alpha-2', 'alpha-3'])
world = world.merge(mapping, left_on='iso_a3', right_on='alpha-3', how='outer', validate='one_to_one')
world = world[pd.notna(world['alpha-2'])]

hosts = load_data('hosts_per_country.csv')
ases = load_data('ASes_per_country.csv')
per_country = hosts.merge(ases, on='country', how='outer')

merged = world.merge(per_country, left_on='alpha-2', right_on='country', how='outer', validate='one_to_one')
merged = merged.filter(items=['country', 'geometry', 'hosts', 'ASes'])

fig, ax = plt.subplots(1, 1)
divider = make_axes_locatable(ax)
cax = divider.append_axes("right", size="2%", pad=0.1)

merged.plot(column='hosts', ax=ax, legend=True, cax=cax, missing_kwds={'color': 'lightgrey'})
plt.savefig("plots/hosts_per_country.png")

merged.plot(column='ASes', ax=ax, legend=True, cax=cax, missing_kwds={'color': 'lightgrey'})
plt.savefig("plots/ASes_per_country.png")