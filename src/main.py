from pandas_chunk import run_pandas_chunk
from dask_method import run_dask
from compression_method import compress_file, read_compressed
import os

FILE = "../data/big_5gb.csv"

def get_size(file):
    return os.path.getsize(file) / (1024**3)

def main():
    print("File size (GB):", get_size(FILE))

    # Pandas Chunk
    t1, rows1 = run_pandas_chunk(FILE)
    print("Pandas Chunk Time:", t1)

    # Dask
    t2, rows2 = run_dask(FILE)
    print("Dask Time:", t2)

    # Compression
    compressed = compress_file(FILE)
    print("Compressed size (GB):", get_size(compressed))

    t3, rows3 = read_compressed(compressed)
    print("Compressed Read Time:", t3)

if __name__ == "__main__":
    main()