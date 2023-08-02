import os
from multiprocessing.pool import Pool
from utils import transcribe_file


def main():
    files = os.listdir()
    pool = Pool(5)
    pool.map(transcribe_file, files)


if __name__ == '__main__':
    main()
