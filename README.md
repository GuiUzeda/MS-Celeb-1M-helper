# MS-Celeb-1M Helpers

### Some helpers to the MS-Celeb-1M database

## download.py:
A download script for the MS-Celeb-1M's croped DB. It will downalod all the db's parts parallelized in 10 threads

    optional arguments:
    -h, --help         show this help message and exit
    -d DIR, --dir DIR  Directory to save the data


## extract.py:
A extractor script for the MS-Celeb-1M's croped DB

    optional arguments:
    -h, --help            show this help message and exit
    -p PATH, --path PATH  Path to the downloaded data data
    -d DIR, --dir DIR     Directory where the images will be saved
