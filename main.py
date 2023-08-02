import os
from multiprocessing.pool import Pool
from settings import load_settings
from utils import transcribe_file
from settings import Settings


def main():
    settings: Settings = load_settings()

    if settings.FILENAME:
        transcribe_file(settings.FILENAME)
    else:
        files = os.listdir()
        pool = Pool(5)
        pool.map(transcribe_file, files)


if __name__ == '__main__':
    main()
