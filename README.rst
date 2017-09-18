==========
imagedupes
==========
--------------------------------------------------------
Python 3 application for finding visually similar images
--------------------------------------------------------
usage: imagedupes [-h] [-a ALGORITHM] [-d DIRECTORY] [-l] [-r] [-s HASH_SIZE]

Finds visually similar images and opens them in the default image file
handler, one group of matches at a time. If no options are specified, it
defaults to searching the current working directory non-recursively using a
perceptual image hash algorithm with a hash size of 8 and does not follow
symbolic links.

optional arguments:
  -h, --help            show this help message and exit
  -a ALGORITHM, --algorithm ALGORITHM
                        Specify a hash algorithm to use. Acceptable inputs:
                        'dhash' (horizontal difference hash),
                        'dhash_vertical', 'ahash' (average hash), 'phash'
                        (perceptual hash), 'phash_simple', 'whash_haar' (Haar
                        wavelet hash), 'whash_db4' (Debauchles wavelet hash).
                        Defaults to 'phash' if not specified.
  -d DIRECTORY, --directory DIRECTORY
                        Directory to search for images
  -l, --links           Follow symbolic links. Defaults to off if not
                        specified.
  -r, --recursive       Search through directories recursively. Defaults to
                        off if not specified.
  -s HASH_SIZE, --hash_size HASH_SIZE
                        Resolution of the hash; higher is more CPU intensive
                        and more sensitive to differences. Must be a power of
                        2 (2, 4, 8, 16...). Defaults to 8 if not specified.
