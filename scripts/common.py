# helper used by the three acquire scripts.
# it downloads one file, makes a sha-256 hash of it, and writes the hash down in data/raw/checksums.csv.
# run the acquire scripts from the main project folder so the data/raw path works.
import hashlib
import os
from datetime import datetime

import pandas as pd
import requests

CHECKSUMS = "data/raw/checksums.csv"


def sha256_of(path):
    # read the whole file as bytes and hash it, same idea as assignment 1
    with open(path, "rb") as f:
        return hashlib.sha256(f.read()).hexdigest()


def fetch(url, params, filename):
    # make the data/raw folder if it is not there yet (it will not be on the very first run)
    os.makedirs("data/raw", exist_ok=True)
    path = "data/raw/" + filename

    # open the list of hashes we already wrote down (empty the very first time)
    if os.path.exists(CHECKSUMS):
        record = pd.read_csv(CHECKSUMS)
    else:
        record = pd.DataFrame(columns=["file", "sha256", "bytes", "downloaded_at", "url"])

    # if we already have the file, don't download again (the crash data changes every day).
    # just hash the copy we have and make sure it still matches what we wrote down.
    if os.path.exists(path) and filename in record["file"].values:
        expected = record.loc[record["file"] == filename, "sha256"].iloc[0]
        actual = sha256_of(path)
        if actual != expected:
            raise ValueError("checksum mismatch for " + filename + ": expected " + expected + " but got " + actual)
        print("ok  ", filename, "matches its recorded sha-256")
        return

    # otherwise download it and save it exactly as it came
    response = requests.get(url, params=params, timeout=300)
    response.raise_for_status()
    with open(path, "wb") as f:
        f.write(response.content)

    # write down the hash, size, time and exact url so anyone can check the file later
    new_row = pd.DataFrame([{
        "file": filename,
        "sha256": sha256_of(path),
        "bytes": os.path.getsize(path),
        "downloaded_at": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        "url": response.url,
    }])
    record = record[record["file"] != filename]
    record = pd.concat([record, new_row]).sort_values("file")
    record.to_csv(CHECKSUMS, index=False)
    print("new ", filename, "sha256 =", new_row["sha256"].iloc[0])
