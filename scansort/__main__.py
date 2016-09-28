#!/usr/bin/env python2

from itertools import chain
from os.path import join
import shutil


def map_fidx2page(page_range, missing):
    return list(enumerate(filter(lambda page: page not in missing, page_range)))


def main(odd_dir, even_dir, missing, fname_format, output_dir, **kwargs):

    odd_n = 100
    even_n = 98
    all_n = odd_n + even_n + len(missing)

    odd_all_n = odd_n + sum(map(lambda x: x % 2, missing))
    even_all_n = even_n + sum(map(lambda x: not x % 2, missing))

    if odd_all_n - even_all_n != all_n % 2:
        raise ValueError('Page numbers do not correspond')

    even_pages = map_fidx2page(range(2, all_n + 1, 2), missing)
    assert len(even_pages) == even_n

    odd_pages = map_fidx2page(range(1, all_n + 1, 2), missing)
    assert len(odd_pages) == odd_n

    dirs = (even_dir, odd_dir)
    for fidx, page in chain(even_pages, odd_pages):
        src = join(dirs[page % 2], fname_format % fidx)
        dst = join(output_dir, fname_format % page)

        print('%s -> %s' % (src, dst))
        #shutil.copy(src, dst)


if __name__ == '__main__':
    args = {
        'odd_dir': 'lside',
        'even_dir': 'rside',
        'output_dir': 'out',
        'missing': {10, 12},
        'fname_format': 'scan%04d.tif',
    }

    main(**args)
