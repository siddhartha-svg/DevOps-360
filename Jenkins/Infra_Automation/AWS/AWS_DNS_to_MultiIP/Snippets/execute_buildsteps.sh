#!/usr/bin/bash

export http_proxy=http://proxy.ebiz.horizon.com:80
export https_proxy=http://proxy.ebiz.horizon.com:80
export NO_PROXY=169.254.169.254

echo "Script to Convert DNS into IPAddress"

DNS_Names_list=($DNS_Names)
for i in "${DNS_Names_list[@]}"
do
IPAddress=`nslookup $i | awk '/^Address: / { print $2 }'`

echo "$i : $IPAddress"
echo -e "\n$i = $IPAddress" >> IPAddress.txt

done

echo "End of Script"
