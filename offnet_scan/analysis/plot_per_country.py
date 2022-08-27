import geopandas as gpd
import matplotlib.pyplot as plt
import pandas as pd


def load_data(file_name):
    load_config = {
        "delim_whitespace": True,
        "engine":'c',
        "index_col":False,
    }
    return pd.read_csv(file_name, **load_config)

population = pd.read_csv('WPP2022_TotalPopulationBySex.csv')
population = population[population['Time'] == 2021]
population = population[pd.notna(population['ISO2_code'])]
population = population.filter(items=['ISO2_code', 'PopTotal'])

world = gpd.read_file(gpd.datasets.get_path('naturalearth_lowres')).filter(items=['iso_a3', 'geometry'])
mapping = pd.read_csv("country_code_mapping.csv").filter(items=['alpha-2', 'alpha-3'])
world = world.merge(mapping, left_on='iso_a3', right_on='alpha-3', how='outer', validate='one_to_one')
world = world[pd.notna(world['alpha-2'])]

hosts = load_data('hosts_per_country.csv')
ases = load_data('ASes_per_country.csv')
per_country = hosts.merge(ases, on='country', how='outer')
per_country = per_country.merge(population, left_on='country', right_on='ISO2_code')


per_country['hosts_per_thousand'] = per_country.apply(lambda row: min(row['hosts'] / (row['PopTotal'] / 1000), 15), axis=1)
per_country['hosts_per_as'] = per_country.apply(lambda row: row['hosts'] / row['ASes'], axis=1)

merged = world.merge(per_country, left_on='alpha-2', right_on='country', how='outer', validate='one_to_one')
merged = merged.filter(items=['country', 'geometry', 'hosts', 'ASes', 'hosts_per_as', 'hosts_per_thousand'])
merged = merged[merged['country'] != 'None']

# fig, ax = plt.subplots()
# divider = make_axes_locatable(ax)
# cax = divider.append_axes("right", size="2%", pad=0.1)

merged.plot(column='hosts', legend=True, legend_kwds={'label': '# of hosts', 'orientation': 'horizontal'}, missing_kwds={'color': 'lightgrey'})
plt.tight_layout()
plt.savefig("plots/hosts_per_country.png")

merged.plot(column='ASes', legend=True, legend_kwds={'label': '# of ASes per country', 'orientation': 'horizontal'}, missing_kwds={'color': 'lightgrey'})
plt.tight_layout()
plt.savefig("plots/ASes_per_country.png")

merged.plot(column='hosts_per_as', legend=True, legend_kwds={'label': '# hosts per AS', 'orientation': 'horizontal'}, missing_kwds={'color': 'lightgrey'})
plt.tight_layout()
plt.savefig("plots/hosts_per_as_per_country.png")

merged.plot(column='hosts_per_thousand', legend=True, legend_kwds={'label': '# hosts per 1,000 people (max 15)', 'orientation': 'horizontal'}, missing_kwds={'color': 'lightgrey'})
plt.tight_layout()
plt.savefig("plots/hosts_per_thousand_per_country.png")
