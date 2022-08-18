#!/usr/bin/env python3

import sys
import json
from os import listdir
from os.path import isfile, join
from cryptography import x509

cert_path = "../onnet_scan/certificates"
cert_files = [f for f in listdir(cert_path) if isfile(join(cert_path, f))]

meta_certificates = set()

for file in cert_files:
    cert = open(join(cert_path, file), 'rb')
    pem_data = cert.read()
    cert = x509.load_pem_x509_certificate(pem_data)
    meta_certificates.add(cert.serial_number)
    print(cert.not_valid_after)

try:
    for line in iter(sys.stdin.readline, b''):
        parsed = json.loads(line)
        meta_certificate = False
        meta_header = False

        if parsed["data"]["http"]["status"] == "success" or parsed["data"]["http"]["status"] == "application-error":
            certificate = parsed["data"]["http"]["result"]["response"]["request"][
                "tls_log"]["handshake_log"]["server_certificates"]["certificate"]
            serial_number = certificate["parsed"]["serial_number"]
            if serial_number in meta_certificates or certificate["parsed"]["subject"]["organization"][0] == "Facebook, Inc.":
                meta_certificate = True

            raw_headers = parsed["data"]["http"]["result"]["response"]["headers"]
            if "unknown" in raw_headers:
                possible_headers = raw_headers["unknown"]
                for header in possible_headers:
                    if header["key"] == "x_fb_debug":
                        meta_header = True

        if meta_certificate and meta_header:
            print(parsed["ip"] + "|" "success-meta-header-cert" +
                  "|" + json.dumps(parsed))
        elif meta_header:
            print(parsed["ip"] + "|" "success-meta-header" +
                  "|" + json.dumps(parsed))
        elif meta_certificate:
            print(parsed["ip"] + "|" "success-meta-cert" +
                  "|" + json.dumps(parsed))
        else:
            print(parsed["ip"] + "|" + parsed["data"]["http"]["status"])

except KeyboardInterrupt:
    sys.stdout.flush()
    pass
