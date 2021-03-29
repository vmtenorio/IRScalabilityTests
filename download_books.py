from gutenberg.acquire import load_etext
from gutenberg.cleanup import strip_headers
from gutenberg._domain_model.exceptions import UnknownDownloadUriException

import shutil
import os

DATA_PATH = os.path.expanduser("~/gutenberg_data/")
N_BOOKS = 400000
TARGET_BOOKS = 200000
LARGE_BOOK = 1e7

if not os.path.exists(DATA_PATH):
    os.mkdir(DATA_PATH)

skipped = 0
for i in range(1,N_BOOKS):
    if i % 100 == 0:
        print("Processing book {} - ".format(i), end="")
    try:
        text = strip_headers(load_etext(i)).strip()
    except UnknownDownloadUriException:
        if i % 100 == 0:
            print("Skipped. Used: {:.2f} GB, Free: {:.2f} GB, Skipped: {}".format(used / (2**30), free / (2**30), skipped))
        skipped += 1
        continue
    if len(text) > LARGE_BOOK:
        print("Large book: " + str(i))
        skipped += 1
        continue
    with open(DATA_PATH + "{}.txt".format(i), 'w') as f:
        f.write(text)
    total, used, free = shutil.disk_usage("/")
    if i % 100 == 0:
        print("DONE. Used: {:.2f} GB, Free: {:.2f} GB, Skipped: {}".format(used / (2**30), free / (2**30), skipped))
    if free / (2**30) < 100 or (i - skipped) == TARGET_BOOKS:
        print("END. Downloaded {} documents".format(i - skipped))
        break





