--------
Scansort
--------

**Scansort** helps to collate and rename book scan images

============
Installation
============

.. code-block::

    pip install scansort

========
Synopsis
========

.. code-block::

    scansort [-h] [-v]
             -odd ODD -even EVEN [-missing MISSING]
             [-action {move,copy}] [-o OUTPUT] workdir

===========
Desctiption
===========

When using a book-edge scanner (such as Plustek OpticBook),
it is handy to scan two sides of a book separately.
This way you do not need to rotate the book to scan the next page.
Scanned images from different sides normally
make their way into separate directories.

**Scansort** helps one to collate these directories
and rename images accodring to the actual page numbers.

The utility assumes that:

* The collection of images covers
  a monotonically increasing range of page numbers
  (with known missing numbers possible).
  This implies that front-, body-, and (possibly) back-matter
  must be scanned and processed separately.
* Even- and odd-numbered pages are put into separate directories.

Also, see an example_ of the indented workflow.

=======
Options
=======

``workdir`` argument defines a working directory
relative to which all other directory names and paths are interpreted.
By default the current directory is used.

All page numbers must correspond to
the actual "physical" page numbering in the book.

``-odd, -even`` *directory name/path*
    Source directories with scanned images of odd- and even-numbered pages.

``-missing`` *num[,num]\**
    Comma-separated list of page numbers missing in the source directories
    (either accidentally skipped during scanning or not present at all).

``-action`` *{move,copy}*
    Whether to preserve or delete the original images
    from the source directories. Defaults to ``copy``.

``-o`` *directory name/path*
    Output directory for renamed scanned images. Defaults to ``out``
    and will be created automatically if does not exist.

``-h, --help``
    Show a help message and exit.

``-v, --version``
    Show a version information and exit.


.. _example:

=======
Example
=======

After scanning a book I am normally left with something like this:

.. code-block::

    $ tree ./book
    ./book
    ├── lside
    │   ├── scan0001.tiff
    │   ├── scan0002.tiff
    │     ...
    └── rside
        ├── scan0001.tiff
        ├── scan0002.tiff
          ...

    2 directories, 198 files

where ``rside`` contains even-numbered pages. Suppose I skimmed through
the directories and realised I missed two pages: 2 and 10.

Then I run ``scansort`` to collate the directories:

.. code-block::

    $ scansort -odd lside -even rside -missing 2,6 ./book


The utility opens an editor to review the result:

.. code-block::

    # Please review the correspondence between files and book pages
    './book/lside/scan0001.tiff':   1
    './book/lside/scan0002.tiff':   3
    './book/rside/scan0001.tiff':   4
    './book/lside/scan0003.tiff':   5
    './book/lside/scan0004.tiff':   7
    './book/rside/scan0002.tiff':   8
    ...

I can edit the page numbers right away
or remove all lines to cancel the operation
(e.g. if it turns out there are more pages missing).
Then I save and close the editor and the pages are collated:

.. code-block::

    $ tree ./book/out
    ./book/out
    ├── scan0001.tif
    ├── scan0003.tif
    ├── scan0004.tif
    ├── scan0005.tif
    ├── scan0007.tif
        ...
    └── scan0200.tif

    0 directories, 198 files

Note that the missing page number are omitted. I can then scan those separately
and put in place.
