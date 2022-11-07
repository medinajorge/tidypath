from setuptools import setup, find_packages


setup(
    name='tidypath',
    version='0.0.1',
    license='GNU General Public License v3.0',
    author="Jorge Medina Hernández",
    author_email='medinahdezjorge@gmail.com',
    packages=find_packages('tidypath'),
    package_dir={'': 'tidypath'},
    url='https://github.com/medinajorge/tidypath',
    description="Automatically store/load data in a tidy, efficient way.",
    long_description="Avoid spending time and lines of code creating directories, deciding filenames, etc. Tidypath automatically does it in an efficient, user-friendly way.",
    keywords=['tidy', 'project organization', 'project', 'organization', 'path', 'storage'],
    install_requires=[
        'numpy',
        'pandas', 
        'matplotlib',
        'plotly'
      ],
)