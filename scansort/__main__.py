#!/usr/bin/env python3

import os
import subprocess
import tempfile
import shutil
import yaml
from enum import Enum
from typing import Dict, Tuple


file_actions = {
    'move': shutil.move,
    'copy': shutil.copy
}


class Reviewer:
    def __init__(self, mapping: Dict) -> None:
        self.mapping = mapping

    @staticmethod
    def _readable_to_map(text: str) -> Dict:
        return yaml.load(text)

    @staticmethod
    def _map_to_readable(data: Dict) -> str:
        max_page = max(data.values())
        padding = len(str(max_page))
        fmt = '%%s:%% %dd' % (padding+1)

        content = "\n".join(fmt % (repr(f), p) for f, p in
                            sorted(data.items(), key=lambda x: x[1]))
        return content

    def review(self) -> Dict:
        json_map = self._map_to_readable(self.mapping)

        with tempfile.NamedTemporaryFile(mode='w+', delete=False) as f:
            f.write("# Please review the correspondence "
                    "between files and book pages\n")
            f.write(json_map)
            tmp_file = f.name

        subprocess.run(['vi', tmp_file])

        with open(tmp_file, 'r') as f:
            lines = (line.strip() for line in f)
            edited_json = "\n".join(l for l in lines if not l.startswith('#'))
        os.unlink(tmp_file)

        return self._readable_to_map(edited_json)


class Page(Enum):
    odd = 1
    even = 2

    @staticmethod
    def test(type_: Enum):
        return lambda n: (n % 2) == (type_.value % 2)

    @staticmethod
    def range(n: int, type_: Enum):
        return range(type_.value, n+1, 2)


class Book:
    def __init__(self):
        self.files = {}
        self.missing = {}

    @property
    def n_all(self):
        return sum(self.n(t) for t in Page)

    @property
    def is_valid(self):
        return self.n(Page.odd) - self.n(Page.even) == self.n_all % 2

    def n(self, type_: Page):
        return len(self.files[type_]) + len(self.missing[type_])

    def add_files_from(self, type_, directory):
        self.files[type_] = sorted(e.path for e in os.scandir(directory)
                                   if e.is_file())

    def add_missing(self, missing: Tuple):
        for type_ in Page:
            self.missing[type_] = list(filter(Page.test(type_), missing))

    def map_files_to_pages(self) -> Dict:
        mapping = {}

        for type_, files in self.files.items():
            missing = self.missing[type_]
            pages = filter(lambda x: x not in missing,
                           Page.range(self.n_all, type_))
            mapping.update({files[i]: p for i, p in enumerate(pages)})

        return mapping


def main(work_dir: str, odd_dir: str, even_dir: str, missing: tuple,
         output_dir: str, action: str, fmt: str):

    book = Book()

    book.add_missing(missing)

    for type_, dir_ in ((Page.odd, odd_dir), (Page.even, even_dir)):
        book.add_files_from(type_, os.path.join(work_dir, dir_))

    if not book.is_valid:
        raise ValueError('Page numbers does not correspond')

    rev = Reviewer(book.map_files_to_pages())
    files_to_pages = rev.review()

    if not files_to_pages:
        print("Nothing to do, sorting is cancelled.")
        return

    output_path = os.path.join(work_dir, output_dir)
    os.makedirs(output_path, exist_ok=True)

    act = file_actions[action]
    output_fmt = os.path.join(output_path, fmt)

    for file_, page in files_to_pages.items():
        act(file_, output_fmt % page)

    print('%d files have been processed.' % len(files_to_pages))


if __name__ == '__main__':

    from argparse import ArgumentParser

    def cs_split(s):
        if not s:
            return ()
        else:
            return tuple(map(int, s.split(',')))


    parser = ArgumentParser(description='Scan Sorting Utility')

    parser.add_argument('workdir', default='.',
                        help='working directory for input and output files')
    parser.add_argument('-odd', required=True, help='directory with odd-numbered pages')
    parser.add_argument('-even', required=True, help='directory with even-numbered pages')

    parser.add_argument('-missing', default='', type=cs_split,
                        help='comma-separated list of pages numbers (e.g. 1,24,35)')
    parser.add_argument('-action', default='copy', choices=file_actions.keys(),
                        help='action performed to the selected files (default: %(default)s)')
    parser.add_argument('-o', default='out', dest='output',
                        help='output directory (default: %(default)s)')

    args = parser.parse_args()

    main(
        work_dir=args.workdir,
        odd_dir=args.odd,
        even_dir=args.even,
        missing=args.missing,
        action=args.action,
        output_dir=args.output,
        fmt='scan%04d.tif'
    )
