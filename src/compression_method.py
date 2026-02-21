import pandas as pd
import gzip
import shutil
import time
import os


def compress_file(file_path):
    compressed_path = "big_5gb.csv.gz"

    with open(file_path, 'rb') as f_in:
        with gzip.open(compressed_path, 'wb') as f_out:
            shutil.copyfileobj(f_in, f_out)

    return compressed_path


def read_compressed(compressed_path):
    start = time.time()

    df = pd.read_csv(compressed_path, compression='gzip')
    total_rows = len(df)

    end = time.time()

    execution_time = end - start

    return execution_time, total_rows