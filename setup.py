from setuptools import setup

setup(
    name='scansort',
    version='0.1',
    platforms='any',
    packages=['scansort'],
    entry_points={'console_scripts': ['scansort = scansort.__main__:main']},
    install_requires=['PyYAML'],
    author='Max Kuznetsov',
    author_email='maks.kuznetsov@gmail.com',
    description='Scansort helps to collate and rename book scan images',
    license='MIT',
    url='https://github.com/mkuznets/scansort',

    classifiers=[
        'License :: OSI Approved :: MIT License',
        'Intended Audience :: End Users/Desktop',
        'Operating System :: OS Independent',
        'Programming Language :: Python :: 3 :: Only',
        'Programming Language :: Python :: 3.4',
        'Topic :: Multimedia :: Graphics :: Capture :: Scanners',
    ],
)
