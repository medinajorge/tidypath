from setuptools import setup, find_packages

setup(
    name='tidypath',
    version='1.0.0',
    author="Jorge Medina Hernández",
    author_email='medinahdezjorge@gmail.com',
    packages=find_packages('tidypath'),
    package_dir={'': 'tidypath'},
    url='https://github.com/medinajorge/tidypath',
    download_url='https://github.com/medinajorge/tidypath/archive/refs/tags/v1.0.1.tar.gz'
    description="Automatically store/load data in a tidy, efficient way.",
    long_description="Avoid spending time and lines of code creating directories, deciding filenames, etc. Tidypath automatically does it in an efficient, user-friendly way.",
    keywords=['tidy', 'project organization', 'project', 'organization', 'path', 'storage'],
    classifiers = [
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: GNU Affero General Public License v3",
        "Operating System :: OS Independent",        
        "Development Status :: 5 - Production/Stable",
        "Topic :: Scientific/Engineering",
        "Topic :: Office/Business",
        "Intended Audience :: Science/Research",
    ],
    install_requires=[
        'numpy',
        'pandas', 
        'matplotlib',
        'plotly'
    ],
)