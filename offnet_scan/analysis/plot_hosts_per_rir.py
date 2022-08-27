import matplotlib.pyplot as plt
import pandas as pd


def load_data(file_name):
    load_config = {
        "delim_whitespace": True,
        "engine":'c',
        "index_col":False,
    }
    return pd.read_csv(file_name, **load_config)

ases = load_data('hosts_per_AS.csv').filter(items=['asn', 'hosts'])

numbers = pd.read_csv('iana_as_number_assignments.csv', index_col=False)

hosts_by_rir = {}

for i, row in ases.iterrows():
    asn = int(row['asn'][2:])
    rir_found = False
    for i, assignment in numbers.iterrows():
        if asn >= int(assignment['NumberLow']) and asn <= int(assignment['NumberHigh']):
            rir_found=True
            rir = assignment['RIR']
            if rir not in hosts_by_rir:
                hosts_by_rir[rir] = 0
            hosts_by_rir[rir] += 1
            break
    if not rir_found:
        print('no rir found for AS{}'.format(asn))
        pass

print(hosts_by_rir)

total = sum(hosts_by_rir.values())

fig1, ax1 = plt.subplots()
p, tx, autotexts = ax1.pie(hosts_by_rir.values(), labels=hosts_by_rir.keys(), autopct='%1.1f%%')
for i, a in enumerate(autotexts):
    value = list(hosts_by_rir.values())[i]
    a.set_text("{} ({:.1f}%)".format(value, value/total * 100))

ax1.axis('equal')

plt.savefig('plots/hosts_per_rir')

