#!/usr/bin/env python3

import sys
import json

input = open(sys.argv[1], 'r')
lines = input.readlines()

success_count = 0
fail_count = 0
headers = set()
unique_header_count = 0

for line in lines:
    parsed = json.loads(line)
    if parsed["data"]["http"]["status"] == "success" or parsed["data"]["http"]["status"] == "application-error":
        success_count += 1
        raw_headers = parsed["data"]["http"]["result"]["response"]["headers"]
        if "unknown" in raw_headers:
            possible_headers = raw_headers["unknown"]
            for header in possible_headers:
                if header["key"] == "proxy_status":
                    proxy_list = header["value"][0].split(';')
                    for h in [v.strip().split("=")[0] for v in proxy_list]:
                        possible_headers.append(
                            {"key": "proxy_status: " + h, "value": ""})
                if header["key"] not in headers:
                    print(header["key"])
                    headers.add(header["key"])
                    unique_header_count += 1

    else:
        fail_count += 1

print(f'success: {success_count}  fail: {fail_count}')
print(f'unique headers: {unique_header_count}')
