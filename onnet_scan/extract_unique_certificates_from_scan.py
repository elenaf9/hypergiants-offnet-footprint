#!/usr/bin/env python3

import sys
import json


def make_safe_filename(s):
    def safe_char(c):
        if c.isalnum():
            return c
        else:
            return "_"
    return "".join(safe_char(c) for c in s).rstrip("_")


input = open(sys.argv[1], 'r')
lines = input.readlines()

success_count = 0
fail_count = 0
certificates = set()
unique_certificate_count = 0

for line in lines:
    parsed = json.loads(line)
    if parsed["data"]["http"]["status"] == "success" or parsed["data"]["http"]["status"] == "application-error":
        success_count += 1
        certificate = parsed["data"]["http"]["result"]["response"]["request"][
            "tls_log"]["handshake_log"]["server_certificates"]["certificate"]
        if certificate["raw"] not in certificates:
            serial_number = certificate["parsed"]["serial_number"]
            subject_dn = certificate["parsed"]["subject_dn"]
            unique_certificate_count += 1
            certificates.add(certificate["raw"])
            filename = make_safe_filename(subject_dn + " " + serial_number)
            print(subject_dn)
            f = open(
                "certificates/" + filename + ".pem",
                "w")
            f.write("-----BEGIN CERTIFICATE-----\n")
            f.write(certificate["raw"])
            f.write("\n-----END CERTIFICATE-----")
            f.close()
    else:
        fail_count += 1

print(f'success: {success_count}  fail: {fail_count}')
print(f'unique certificates: {unique_certificate_count}')
