# Measuring the AS footprint of hypergiants' off-nets

## Mapping Prefix <-> ASN from BGP dump

```sh
cargo run -- -a -p
```

Rust client for obtaining route collection dump. 
See <https://ris.ripe.net/docs/20_raw_data_mrt.html#route-collection-raw-data-mrt-files>.  
Print announced Prefix-ASN pairs and writes mapping files:
- `data/asn_prefix_mapping.csv`: Prefixes announced by each ASN
- `data/prefix_asn_mapping.csv`: AS(es) that announce a prefix. Should usually just be one AS.

```sh
bgp-mapping 

USAGE:
    bgp-mapping [OPTIONS]

OPTIONS:
    -a, --asn-prefix-mapping    Write ASN -> prefixes mapping file.
        --date <YYYY-MM-DD>     
    -h, --help                  Print help information
    -p, --prefix-asn-mapping    Write prefix -> ASN mapping file.
        --prefix <PREFIX>       Filter for supernets of a prefix.
        --rrc <RRC>             Route collector no. [default: 00]
        --time <hh:MM>          [default: 00:00]
```

## Get all IPs of a domain's AS

```sh
get_ips.sh facebook.com
```

1. Resolves the domain to an IP address.
2. Queries for the origin AS of the IP.
3. Queries for all IPv4-Addresses that are originated in this AS.
