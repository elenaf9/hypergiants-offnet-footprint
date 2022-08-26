# Measuring the AS footprint of hypergiants' off-nets

**Research Question:**  
What is the AS footprint of hypergiants' off-nets today?  
*We limit this research question to only target the hypergiant Meta / Facebook.*

**Methodology:**  
*Inspired by [Gigis et al.].*
1. [./bgp-mapping](./bgp-mapping/): Aggregate the IPv4 addresses announced by the hypergiants AS  
2. [./onnet_scan](./onnet_scan/): Perform an on-net scan on the aggregated IPv4 space to collect all TLS certificates from this hypergiants  
    - use zgrab2 to perform https handshake with each online host
    - collect unique TLS certificates and unique HTTP headers
3. [./offnet_scan](./offnet_scan/): Perform off-net scan on the whole IPv4 address space
    - scan with zmap for hosts online on port 443
    - scan with zgrab2 for meta related certificates and headers

## Results

Unique TLS Certificates: 15  
Off-net host count: 16172  
Off-net AS count: 2339  

Scan | Analysis | Plots
-|-|-
On-net | [onnet_scan#Analysis](./onnet_scan/README.md#analysis) | [onnet_scan/analysis/plots](onnet_scan/analysis/plots)
Off-net | [offnet_scan#Analysis](./offnet_scan/README.md#analysis) | [offnet_scan/analysis/plots](offnet_scan/analysis/plots)


## Ressources

- [Gigis et al.]  
  Petros Gigis, Matt Calder, Lefteris Manassakis, George Nomikos, Vasileios Kotronis, Xenofontas Dimitropoulos, Ethan Katz-Bassett, and Georgios Smaragdakis. 2021. Seven years in the life of Hypergiants' off-nets. In *Proceedings of the 2021 ACM SIGCOMM 2021 Conference (SIGCOMM '21)*. Association for Computing Machinery, New York, NY, USA, 516–533. <https://doi.org/10.1145/3452296.3472928>
