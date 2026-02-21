import dask.dataframe as dd
import time

def run_dask(file_path):
    start = time.time()

    df = dd.read_csv(
        file_path,
        dtype={'sku': 'str'},
        assume_missing=True
    )

    total_rows = df.shape[0].compute()

    end = time.time()

    execution_time = end - start

    return execution_time, total_rows