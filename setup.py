from setuptools import setup, find_packages


setup(
    name='bexio-python',
    version='0.0.1',
    description='',
    url='https://github.com/jpgehrig/bexio-python',
    keywords=[
        'python',
        'bexio',
        'cli',
    ],
    author='jpgehrig',
    license='unlicensed',
    packages=find_packages(exclude=('tests')),
    install_requires=[
        'click~=8.0',
        'requests~=2.25',
        'python-dateutil~=2.8'
    ],
    entry_points='''
        [console_scripts]
        bexio=bexio.cli:main
    ''',
    python_requires=">=3.7",
    classifiers=[
        "Natural Language :: English",
        "Intended Audience :: Developers",
        "Development Status :: 3 - Alpha",
        "License :: OSI Approved :: MIT License",
        "Topic :: Software Development :: Libraries",
        "Programming Language :: Python",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
    ],
)
