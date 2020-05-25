import setuptools

with open ('README.md', 'r') as fh:
    long_description = fh.read ()

setuptools.setup (
    name = 'Alzebra',
    version = '0.0.1',
    author = 'OumieZn&MattCharr',
    author_email = '_',
    description = '',
    long_description = long_description,
    long_description_content_type = 'text/markdown',
    url = 'https://github.com/' + 'username' + '/' + 'name_project' + '.git',
    packages = setuptools.find_packages (),
    classifiers = [
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: GNU Lesser General Public License v2 (LGPLv2)',
        'Operating System :: OS Independent',
    ],
    python_requires = '>=3.6'
)