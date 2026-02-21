import pandas as pd
import time


def run_pandas_chunk(file_path):
    start = time.time()

    total_rows = 0

    for chunk in pd.read_csv(file_path, chunksize=100000):
        total_rows += len(chunk)

    end = time.time()

    execution_time = end - start

    return execution_time, total_rows