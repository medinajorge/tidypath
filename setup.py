from setuptools import setup, find_packages

setup(
    name='tidypath',
    version='1.0.0',
    author="Jorge Medina Hernández",
    author_email='medinahdezjorge@gmail.com',
    packages=find_packages('tidypath'),
    package_dir={'': 'tidypath'},
    url='https://github.com/medinajorge/tidypath',
    description="Automatically store/load data in a tidy, efficient way.",
    long_description="Avoid spending time and lines of code creating directories, deciding filenames, etc. Tidypath automatically does it in an efficient, user-friendly way.",
    keywords=['tidy', 'project organization', 'project', 'organization', 'path', 'storage'],
    classifiers = [
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: GNU Affero General Public License v3",
        "Operating System :: OS Independent",
        "Topic :: System :: Filesystems",
        "Development Status :: 4 - Beta",
    ],
    install_requires=[
        'numpy',
        'pandas', 
        'matplotlib',
        'plotly'
    ],
)