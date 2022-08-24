#!/bin/bash

# Apologies for this awful hacky script.

invalid_cmd="Invalid command\nExpect
  \n\t$ ./resolve.sh whois <ip-address>\nor
  \n\t$ ./resolve.sh whois <asn>\nor
  \n\t$ ./resolve.sh domain <domain>\n"

WhoIs() {
    whois -h riswhois.ripe.net $1
}

GetASNforIP() {
    WhoIs $1  | grep -P -o "AS\d+" -m 1
}

GetAllIpv4sForASN() {
    WhoIs $1 | grep -P "route[^6]" | grep -P -o "\d+\.\d+\.\d+\.\d+/\d{1,2}"
}

GetIps() {
    host $1 | grep -P -o "\d+\.\d+\.\d+\.\d+" \
    | xargs -I {} bash -c 'GetASNforIP "{}"'\
    | xargs -I {} bash -c 'GetAllIpv4sForASN "{}"'
}


export -f WhoIs
export -f GetASNforIP
export -f GetAllIpv4sForASN
export -f GetIps

test="AS3333"

if [ "$#" -ne 2 ]; then
    echo -e $invalid_cmd
elif [ $1 = "domain" ]; then
    GetIps $2
elif [ $1 = "whois" ] && [[ $2 =~ AS[0-9]+ ]]; then
    GetAllIpv4sForASN $2
elif [ $1 = "whois" ]; then
    GetASNforIP $2
else 
    echo -e $invalid_cmd
fi