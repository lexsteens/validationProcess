#!/usr/bin/python3

# pip install virustotal-api

from virus_total_apis import PublicApi as VirusTotalPublicApi
import json
import hashlib
import sys
import csv
import time

API_KEY = "743f3685e1f13447c53e3d000709e904b302d8984fb769a979acc6d2dedece01"
vt = VirusTotalPublicApi(API_KEY)

def md5(fname):
    hash_md5 = hashlib.md5()
    with open(fname, "rb") as f:
        for chunk in iter(lambda: f.read(4096), b""):
            hash_md5.update(chunk)
    return hash_md5.hexdigest()

def scanFile(file):
    response = vt.get_file_report(md5(file))
    #print(json.dumps(response, sort_keys=False, indent=4))
    stats = {}
    try:
        for scan in response['results']['scans']:
            #print(response['results']['scans'][scan])
            if response['results']['scans'][scan]['detected'] not in stats:
                stats[response['results']['scans'][scan]['detected']] = 1
            else:
                stats[response['results']['scans'][scan]['detected']] += 1
    except:
        stats['verbose_msg'] = response['results']['verbose_msg']
        #print(json.dumps(response, sort_keys=False, indent=4))
    return stats

def scanFiles(fileListCsv, prefix):
	f_in = open(fileListCsv, 'r')
	f_out = open(fileListCsv.replace(".csv", "") + "_scan_results.csv", 'w', 1)

	input = csv.reader(f_in, delimiter=";")
	for row in input:
		fullPath = (prefix + row[0][1:]).replace("//", "/")
		print("Scanning " + fullPath)
		res = scanFile(fullPath)
		print(str(res))
		f_out.write(fullPath + "\t" + str(res) + "\n")
		time.sleep(20)
	f_in.close()
	f_out.close()

if __name__ == "__main__":
	scanFiles(sys.argv[1], sys.argv[2])
