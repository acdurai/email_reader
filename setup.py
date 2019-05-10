from setuptools import setup, find_packages
from os import path
from io import open

here = path.abspath(path.dirname(__file__))

with open(path.join(here, 'README.rst'), encoding='utf-8') as readme_file:
    readme = readme_file.read()

with open(path.join(here, 'HISTORY.rst'), encoding='utf-8') as history_file:
    history = history_file.read().replace('.. :changelog:', '')


setup(
    name='email_reader',  
    version='1.0.5',  
    description='Sample email reader ',  
    long_description=readme + '\n\n' + history,
    author='Chelladurai',
    author_email='acdurai04@gmail.com',
    url='https://github.com/acdurai/email_reader',
    # packages=['email_reader'],
    packages=find_packages(exclude=['contrib', 'docs', 'tests']),
    
    classifiers=[  # Optional
        'Development Status :: 3 - Alpha',
        'Intended Audience :: Developers',
        'Topic :: Software Development :: Build Tools',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 2',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
    ],

    install_requires=['cryptography'],
    include_package_data=True,

   

    

    project_urls={  # Optional
        'Bug Reports': 'https://github.com/acdurai/email_reader/issues',
        'Funding': 'https://donate.pypi.org',
        'Say Thanks!': 'http://saythanks.io/to/example',
        'Source': 'https://github.com/acdurai/email_reader/',
    },
)
