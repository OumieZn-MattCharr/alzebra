import setuptools

with open ('README.md', 'r') as fh:
    long_description = fh.read ()

NAME = 'beta-Panda'
USERNAME = 'oumiezn-mattcharr'

setuptools.setup (
    name = NAME,
    version = '0.0.1',
    author = USERNAME,
    author_email = 'oumiezn.mattcharr@gmail.com',
    description = '',
    long_description = long_description,
    long_description_content_type = 'text/markdown',
    url = 'https://github.com/' + USERNAME + '/' + NAME + '/',
    packages = setuptools.find_packages (),
    classifiers = [
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: GNU Lesser General Public License v2 (LGPLv2)',
        'Operating System :: OS Independent',
    ],
    python_requires = '>=3.7'
)
