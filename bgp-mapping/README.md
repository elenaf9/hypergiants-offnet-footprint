# Mapping Prefix <-> ASN from BGP dump

Rust client for obtaining route collection dump.
See <https://ris.ripe.net/docs/20_raw_data_mrt.html#route-collection-raw-data-mrt-files>.  
Print announced Prefix-ASN pairs and writes mapping files:
- `data/asn_prefix_mapping.csv`: Prefixes announced by each ASN.  
  **Note:** we write the mapping to file in batches (i.e. we write the current mapping to the file for each new /8 prefix), thus ASN may appear multiple times.
- `data/prefix_asn_mapping.csv`: AS(es) that announce a prefix. Should usually just be one AS.

```sh
bgp-mapping 

USAGE:
    bgp-mapping [OPTIONS]

OPTIONS:
    -a, --asn-prefix-mapping    Write ASN -> prefixes mapping file.
        --date <YYYY-MM-DD>     [default: date today]
    -h, --help                  Print help information
    -p, --prefix-asn-mapping    Write prefix -> ASN mapping file.
        --prefix <PREFIX>       Filter for super-/ subnets of a specific prefix.
        --rrc <RRC>             Route collector no. [default: 00]
        --time <hh:MM>          [default: 00:00]
```

```sh
$ cargo run --release -- -p -a
    Finished release [optimized] target(s) in 0.11s
     Running `target/release/bgp-mapping`
Prefix: 1.0.0.0/24| ASN: 13335
Prefix: 1.0.4.0/22| ASN: 38803
...
Prefix: 223.255.253.0/24| ASN: 58519
Prefix: 223.255.254.0/24| ASN: 55415
Time elapsed: 490s
```

Note: this parses the **whole** bgp dump into readable csv files. For simply resolving IP to ASN or ASN to IPS use the script described below.

## Resolve IPs / AS Numbers / domains

*Only tested on linux.*

Pre-requisite:
- `whois` Client  
  Install e.g. on Debian with `apt install whois`

### Get all IPs of a domain's AS

```sh
./resolve.sh domain facebook.com
```

1. Resolves the domain to an IP address.
2. Queries for the origin AS of the IP.
3. Queries for all ddresses that are originated in this AS.

### Resolve IP -> ASN or ASN -> IPs

**ASN -> IPS:**

```sh
$ ./resolve.sh whois AS3333
193.0.0.0/21
193.0.10.0/23
193.0.12.0/23
193.0.18.0/23
193.0.20.0/23
193.0.22.0/23
```

**IP -> ASN:**

```sh
$ ./resolve.sh whois 193.0.10.0/23
AS3333
```

## Number of allocated IP addresses per AS

Code: [asn_prefixes_analysis.py](./analysis/asn_prefixes_analysis.py)

```sh
$ python3 asn_prefixes_analysis.py 32934

2022-08-11:

asn    allocated addresses
32934               190454

2022-08-25:

asn    allocated addresses        
32934               190708
```
