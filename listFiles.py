#!/usr/bin/python3

import os
import sys
import subprocess
from datetime import datetime
import hashlib
#import magic


def listDir(dir, outFile):
    f = open(outFile, 'w')
    f.write(";".join(["file","type","md5"]) + "\n")

    os.chdir(dir)

    fileList = []

    for root, subDirs, files in os.walk("."):
        for file in subDirs + files:
            fileList.append([root + "/" + file])

    N = len(fileList)
    n = 0
    for line in fileList:
        n = n + 1
        if n % 1000 == 0:
            print(str(datetime.now()) + " " + str(n) + " / " + str(N))

        fullName = line[0]
        line.append(getFileInfos(fullName))
        try:
            line.append(md5(fullName))
        except:
            line.append("")

        f.write(";".join(line) + "\n")

    f.close()



def getFileInfos(fname):
    #return magic.from_file(fname)
    sp = subprocess.Popen(['file', fname], stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
    return sp.stdout.read().decode('utf-8').rstrip().split(": ")[1]

def md5(fname):
    hash_md5 = hashlib.md5()
    with open(fname, "rb") as f:
        for chunk in iter(lambda: f.read(4096), b""):
            hash_md5.update(chunk)
    return hash_md5.hexdigest()

if __name__ == "__main__":
    rootDir = sys.argv[1]
    outFile = sys.argv[2]
    listDir(rootDir, outFile)
