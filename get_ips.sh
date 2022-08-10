#!/bin/bash

# Apologies for this awful hacky script.

ipv4_reqex="\d+\.\d+\.\d+\.\d+"

WhoIs() {
    whois -h riswhois.ripe.net $1
}

GetASNforIP() {
    WhoIs $1  | grep -P -o "AS\d+" -m 1
}

GetAllIpv4sForASN() {
    WhoIs $1 | grep -P "route[^6]" | grep -P -o "\d+\.\d+\.\d+\.\d+/\d{1,2}"
}

export -f WhoIs
export -f GetASNforIP
export -f GetAllIpv4sForASN

host $1 | grep -P -o $ipv4_reqex \
| xargs -I {} bash -c 'GetASNforIP "{}"'\
| xargs -I {} bash -c 'GetAllIpv4sForASN "{}"'