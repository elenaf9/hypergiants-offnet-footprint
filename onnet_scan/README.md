# On-net fingerprint scan for Meta ASN (32934) (16.08.2022 14:00)

### Used asn mapping

```
32934 | 31.13.24.0/21 31.13.64.0/18 31.13.65.0/24 31.13.66.0/24 31.13.67.0/24 31.13.68.0/24 31.13.69.0/24 31.13.70.0/24 31.13.71.0/24 31.13.72.0/24 31.13.73.0/24 31.13.74.0/24 31.13.75.0/24 31.13.76.0/24 31.13.77.0/24 31.13.78.0/24 31.13.80.0/24 31.13.81.0/24 31.13.82.0/24 31.13.83.0/24 31.13.84.0/24 31.13.85.0/24 31.13.86.0/24 31.13.87.0/24 31.13.88.0/24 31.13.89.0/24 31.13.92.0/24 31.13.93.0/24 31.13.94.0/24 31.13.96.0/19
```

### Commands

```
$ zgrab2 --input-file=zgrab_config/input_scan.txt --output-file=output.txt multiple -c zgrab_config/scan_config.ini
INFO[0000] started grab at 2022-08-16T13:19:42+02:00
INFO[0300] finished grab at 2022-08-16T13:24:42+02:00
{"statuses":{"http":{"successes":1456,"failures":32080}},"start":"2022-08-16T13:19:42+02:00","end":"2022-08-16T13:24:42+02:00","duration":"5m0.6399389s"}

$ ./extract_unique_certificates_from_scan.py 2022-08-16T13/output.txt
success: 2072  fail: 31464
unique certificates: 15

$ ./extract_unique_headers_from_scan.py 2022-08-16T13/output.txt
success: 2072  fail: 31464
unique headers: 11
```

Different in successes between `zgrab2` and
`extract_unique_X_from_scan.py` because `zgrab2` counts `TOO_MANY_REDIRECTS` as
`application-error` but reponse still contains usable certificate or headers.

### Usable fingerprints for Meta servers

#### Unique certificates

```
C=US, ST=California, L=Menlo Park, O=Facebook, Inc., CN=*.facebook.com
C=US, ST=California, L=Menlo Park, O=Facebook, Inc., CN=*.instagram.com
C=US, ST=California, L=Menlo Park, O=Facebook, Inc., CN=*.facebookvirtualassistant.com
C=US, ST=California, L=Menlo Park, O=Facebook, Inc., CN=*.bulletin.com
C=US, ST=California, L=Menlo Park, O=Facebook, Inc., CN=*.atlassolutions.com
C=US, ST=California, L=Menlo Park, O=Facebook, Inc., CN=*.wit.ai
C=US, ST=California, L=Menlo Park, O=Facebook, Inc., CN=*.fb.com
C=US, ST=California, L=Menlo Park, O=Facebook, Inc., CN=*.expresswifi.com
C=US, ST=California, L=Menlo Park, O=Facebook, Inc., CN=*.whatsapp.net
C=US, ST=California, L=Menlo Park, O=Facebook, Inc., CN=*.facebook-dns.com
C=US, ST=California, L=Menlo Park, O=Facebook, Inc., CN=*.fbe2e.com
C=US, ST=California, L=Menlo Park, O=Facebook, Inc., CN=*.oculus.com
C=US, ST=California, L=Menlo Park, O=Facebook, Inc., CN=*.extern.facebook.com
C=US, ST=California, L=Menlo Park, O=Facebook, Inc., CN=*.secure.latest.facebook.com
C=US, ST=California, L=Menlo Park, O=Facebook, Inc., CN=*.secure.facebook.com
```

#### Unique HTTP headers

```
proxy_status
    e_fb_vipaddr
    e_fb_builduser
    e_fb_binaryversion
    e_fb_canaryid
x_fb_debug
```