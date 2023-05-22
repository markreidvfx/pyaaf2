#!/usr/bin/env python
from __future__ import (
    unicode_literals,
    absolute_import,
    print_function,
    division,
    )

import os
import time
import argparse

import aaf2

def copy_mobs(a, b):
    for mob in a.content.mobs:
        if mob.mob_id not in b.content.mobs:
            # copy the mob from file a into file b
            mob_copy = mob.copy(root=b)
            b.content.mobs.append(mob_copy)

def copy_essence_data(a, b):
    for essence_data in a.content.essencedata:
        if essence_data.mob_id not in b.content.essencedata:
            # copy the essence data from file a into file b
            essence_data_copy = essence_data.copy(root=b)
            b.content.essencedata.append(essence_data_copy)

def merge_aafs(inputs, dest, mode=None):

    if not mode:
        mode = 'w'
        if os.path.exists(dest):
            mode = 'rw'

    start = time.time()
    with aaf2.open(dest, mode) as dst:
        for path in inputs:
            print("adding", path)
            with aaf2.open(path, 'r') as src:
                # copy dictionary definitions from src file
                dst.dictionary.update(src.dictionary)

                copy_mobs(src, dst)
                copy_essence_data(src, dst)

    dur = time.time() - start
    print("merged %d items in %f secs" % (len(inputs), dur))

def run_cli():
    parser = argparse.ArgumentParser(description="Combines multiple AAF files")
    parser.add_argument('aaf_files', default=[], nargs='+',
                        help="2 or more aaf files, last arg will be the output file, if the file exists it will be added to it")
    parser.add_argument("-f", '--force', dest='mode', default=False, action='store_true',
                        help="overwrite dest file if exists instead of appending it")

    args = parser.parse_args()

    if len(args.aaf_files) < 2:
        parser.error("not enough args")

    mode = None
    if args.mode:
        mode = "w"

    merge_aafs(args.aaf_files[:-1], args.aaf_files[-1], mode)

if __name__ == "__main__":
    run_cli()
