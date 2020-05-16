import os
import re
import subprocess
from pathlib import Path

from setuptools import setup

package_name = 'djangorestframework-datatables-editor'
folder_name = 'rest_framework_datatables_editor'
description = ('Seamless integration between Django REST framework and '
               'Datatables (https://datatables.net) with supporting '
               'Datatables editor')
url = 'https://github.com/VVyacheslav/django-rest-framework-datatables-editor'
author = 'Vyacheslav V.V.'
author_email = 'vvvyacheslav23@gmail.com'
license = 'MIT'

version_re = re.compile('^Version: (.+)$', re.M)


def get_long_description():
    """ Return rst formatted readme and changelog. """
    files_to_join = ['README.rst', 'docs/changelog.rst']
    description = []
    for file in files_to_join:
        with open(file) as f:
            description.append(f.read())
    return '\n\n'.join(description)


def get_packages(package):
    """
    Return root package and all sub-packages.
    """
    return [dirpath
            for dirpath, dirnames, filenames in os.walk(package)
            if os.path.exists(os.path.join(dirpath, '__init__.py'))]


def get_version():
    """
    Reads version from git status or PKG-INFO

    https://gist.github.com/pwithnall/7bc5f320b3bdf418265a
    """
    d: Path = Path(__file__).absolute().parent
    git_dir = d.joinpath('.git')
    if git_dir.is_dir():
        # Get the version using "git describe".
        cmd = 'git describe --tags --match [0-9]*'.split()
        try:
            version = subprocess.check_output(cmd).decode().strip()
        except subprocess.CalledProcessError:
            return None

        # PEP 386 compatibility
        if '-' in version:
            version = '.post'.join(version.split('-')[:2])

        # Don't declare a version "dirty" merely because a time stamp has
        # changed. If it is dirty, append a ".dev1" suffix to indicate
        # a development revision after the release.
        with open(os.devnull, 'w') as fd_devnull:
            subprocess.call(['git', 'status'],
                            stdout=fd_devnull, stderr=fd_devnull)

        cmd = 'git diff-index --name-only HEAD'.split()
        try:
            dirty = subprocess.check_output(cmd).decode().strip()
        except subprocess.CalledProcessError:
            return None

        if dirty != '':
            version += '.dev1'
    else:
        # Extract the version from the PKG-INFO file.
        try:
            with open('PKG-INFO') as v:
                version = version_re.search(v.read()).group(1)
        except FileNotFoundError:
            version = None

    return version


setup(
    name=package_name,
    version=get_version() or 'dev',
    url=url,
    license=license,
    description=description,
    long_description=get_long_description(),
    author=author,
    author_email=author_email,
    packages=get_packages(folder_name),
    install_requires=[
        'djangorestframework>=3.9.1',
    ],
    classifiers=[
        'Development Status :: 5 - Production/Stable',
        'Environment :: Web Environment',
        'Framework :: Django',
        'Framework :: Django :: 1.9',
        'Framework :: Django :: 1.10',
        'Framework :: Django :: 1.11',
        'Framework :: Django :: 2.0',
        'Framework :: Django :: 2.1',
        'Framework :: Django :: 2.2',
        'Framework :: Django :: 3.0',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
        'Natural Language :: English',
        'Programming Language :: Python :: 2',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
        'Topic :: Internet :: WWW/HTTP',
    ]
)
