#!/usr/bin/env python3

import json
import sys

input = open(sys.argv[1], 'r')
lines = input.readlines()

success_count = 0
fail_count = 0
headers = set()
unique_header_count = 0

occurrences = {}
common_names_without_x_fb_debug = set()
common_names_with_x_fb_debug = set()
common_names_without_proxy_status = set()
common_names_with_proxy_status = set()

for line in lines:
    parsed = json.loads(line)
    if parsed["data"]["http"]["status"] == "success" or parsed["data"]["http"]["status"] == "application-error":
        success_count += 1
        raw_headers = parsed["data"]["http"]["result"]["response"]["headers"]
        found_x_debug_header = False
        found_proxy_header = False
        if "unknown" in raw_headers:
            possible_headers = raw_headers["unknown"]
            for header in possible_headers:
                key = header["key"]
                if key == "proxy_status":
                    found_proxy_header = True
                    proxy_list = header["value"][0].split(';')
                    for h in [v.strip().split("=")[0] for v in proxy_list]:
                        possible_headers.append(
                            {"key": "proxy_status: " + h, "value": ""})
                if key == "x_fb_debug":
                    found_x_debug_header = True
                if key not in headers:
                    headers.add(key)
                    unique_header_count += 1
                if key not in occurrences:
                    occurrences[key] = 0
                occurrences[key] += 1
        for common_name in parsed["data"]["http"]["result"]["response"]["request"][
            "tls_log"]["handshake_log"]["server_certificates"]["certificate"]["parsed"]['subject']["common_name"]:
            if found_x_debug_header:
                common_names_with_x_fb_debug.add(common_name)
            else:
                common_names_without_x_fb_debug.add(common_name)
            if found_proxy_header:
                common_names_with_proxy_status.add(common_name)
            else:
                common_names_without_proxy_status.add(common_name)

    else:
        fail_count += 1

print(f'success: {success_count}  fail: {fail_count}')
print(f'unique headers: {unique_header_count}')
print(f'number of occurrences per header: {occurrences}')
print(f'common names without x_fb_debug: {common_names_without_x_fb_debug}')
print(f'common names with x_fb_debug: {common_names_with_x_fb_debug}')
print(f'common names without proxy_status: {common_names_without_proxy_status}')
print(f'common names with proxy_status: {common_names_with_proxy_status}')
