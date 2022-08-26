# Off-net fingerprint scan  (21.08.2022 14:00)

### Commands

First global scan with zmap for TCP SYN 443 then scan for specific meta related
certificates and headers from on-net scan

```
$ zmap --rate=1000000 --target-port=443 --source-port=50000-60000 --output-file=zmap_results.csv
Aug 20 09:17:28.021 [INFO] zmap: output module: cs
[...]
14:57:37 100% (1s left); send: 3702258432 done (68.8 Kp/s avg); recv: 54291955 0 p/s (1.01 Kp/s avg); drops: 0 p/s (0 p/s avg); hitrate: 1.47%
Aug 21 00:35:08.878 [INFO] zmap: completed


$ zgrab2 --input-file=zgrab_config/zmap_results_global_tcp_443 multiple -c zgrab_config/scan_config.ini | ./filter_scan_output.py > output_global" &
[...]
time="2022-08-21T18:30:28Z" level=info msg="finished grab at 2022-08-21T18:30:28Z"
```

### Scan results format

zmap
```
{IP}
```

zgrab2
```
{IP}| {STATUS}| {JSON HTTPS result with cert (only if STATUS=sucess-meta-*)}
```

`STATUS`
* success-meta-{header-cert, header, cert} or default zgrab2 status like unknown-error, success
  * `success-meta-header-cert` (both meta header and cert found)
  * `success-meta-header` (meta header  found)
  * `success-meta-cert` (meta cert found)

### Analysis

**Total host count**: 16172
**Total AS count**: 2339

File | Description
-|-
[hosts_per_AS.csv](./analysis/hosts_per_AS.csv) | Hosts per ASN
[hosts_certs_per_AS.csv](./analysis/hosts_certs_per_AS.csv) | Unique Certificates per ASN
[hosts_countries_per_AS.csv](./analysis/hosts_countries_per_AS.csv) | Host and Country per ASN
[ASes_per_country.csv](./analysis/ASes_per_country.csv) | ASes per country
[hosts_per_country.csv](./analysis/hosts_per_country.csv) | Hosts per country
