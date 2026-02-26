import pandas as pd
import dask.dataframe as dd
import gzip
import shutil
import time
import os
import psutil

FILE = "../data/big_5gb.csv"
COMPRESSED_FILE = "../data/big_5gb.csv.gz"



def get_file_size_gb(path):
    return os.path.getsize(path) / (1024 ** 3)


def get_ram_usage_mb():
    process = psutil.Process(os.getpid())
    return process.memory_info().rss / (1024 ** 2)



def run_pandas_chunk(file_path):
    start_ram = get_ram_usage_mb()
    start_time = time.time()

    total_rows = 0
    for chunk in pd.read_csv(file_path, chunksize=100000):
        total_rows += len(chunk)

    end_time = time.time()
    end_ram = get_ram_usage_mb()

    return {
        "Method": "Pandas Chunk",
        "Time (s)": round(end_time - start_time, 2),
        "RAM Used (MB)": round(end_ram - start_ram, 2),
        "File Size (GB)": round(get_file_size_gb(file_path), 2),
        "Rows": total_rows
    }



def run_dask(file_path):
    start_ram = get_ram_usage_mb()
    start_time = time.time()

    df = dd.read_csv(
        file_path,
        dtype={'sku': 'str'},
        assume_missing=True
    )

    total_rows = df.shape[0].compute()

    end_time = time.time()
    end_ram = get_ram_usage_mb()

    return {
        "Method": "Dask",
        "Time (s)": round(end_time - start_time, 2),
        "RAM Used (MB)": round(end_ram - start_ram, 2),
        "File Size (GB)": round(get_file_size_gb(file_path), 2),
        "Rows": total_rows
    }



def compress_file(file_path):
    with open(file_path, 'rb') as f_in:
        with gzip.open(COMPRESSED_FILE, 'wb') as f_out:
            shutil.copyfileobj(f_in, f_out)


def run_compressed(file_path):
    compress_file(file_path)

    start_ram = get_ram_usage_mb()
    start_time = time.time()

    df = pd.read_csv(COMPRESSED_FILE, compression="gzip")
    total_rows = len(df)

    end_time = time.time()
    end_ram = get_ram_usage_mb()

    return {
        "Method": "Compressed (gzip)",
        "Time (s)": round(end_time - start_time, 2),
        "RAM Used (MB)": round(end_ram - start_ram, 2),
        "File Size (GB)": round(get_file_size_gb(COMPRESSED_FILE), 2),
        "Rows": total_rows
    }



def main():

    results = []

    print("Running Pandas Chunk...")
    results.append(run_pandas_chunk(FILE))

    print("Running Dask...")
    results.append(run_dask(FILE))

    print("Running Compression...")
    results.append(run_compressed(FILE))

    df_results = pd.DataFrame(results)

    df_results.to_csv("benchmark_results.csv", index=False)

    print("\n=== Final Results ===")
    print(df_results)

    fastest = df_results.loc[df_results["Time (s)"].idxmin()]
    lowest_ram = df_results.loc[df_results["RAM Used (MB)"].idxmin()]
    smallest_storage = df_results.loc[df_results["File Size (GB)"].idxmin()]

    print("\n=== Best Methods ===")
    print("Fastest Method:", fastest["Method"])
    print("Lowest RAM Usage:", lowest_ram["Method"])
    print("Smallest Storage:", smallest_storage["Method"])


if __name__ == "__main__":
    main()