#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""The setup script."""

from setuptools import setup, find_packages
import inspect
from pathlib import Path

HOME_DIR = Path(inspect.getfile(inspect.currentframe())).parent


def filter_req_paths(paths, func):
    """Return list of filtered libs."""
    if not isinstance(paths, list):
        raise ValueError("Paths must be a list of paths.")

    libs = set()
    junk = set(['\n'])
    for p in paths:
        with p.open(mode='r') as reqs:
            lines = set([line for line in reqs if func(line)])
            libs.update(lines)

    return list(libs - junk)


def is_pipable(line):
    """Filter for pipable reqs."""
    if "# not_pipable" in line:
        return False
    elif line.startswith('#'):
        return False
    else:
        return True

def clean_reqs(reqs):
    return [req.split(" --hash")[0] for req in reqs]


with open('README.rst') as readme_file:
    readme = readme_file.read()

with open('HISTORY.rst') as history_file:
    history = history_file.read()

requirements = filter_req_paths(paths=[HOME_DIR / "requirements.txt"], func=is_pipable)
requirements = clean_reqs(requirements)

setup_requirements = ["pytest-runner"]

test_requirements = test_requirements = ["pytest"]

{%- set license_classifiers = {
    'MIT license': 'License :: OSI Approved :: MIT License',
    'BSD license': 'License :: OSI Approved :: BSD License',
    'ISC license': 'License :: OSI Approved :: ISC License (ISCL)',
    'Apache Software License 2.0': 'License :: OSI Approved :: Apache Software License',
    'GNU General Public License v3': 'License :: OSI Approved :: GNU General Public License v3 (GPLv3)'
} %}

setup(
    name='{{ cookiecutter.project_slug }}',
    version='{{ cookiecutter.version }}',
    description="{{ cookiecutter.project_short_description }}",
    long_description=readme + '\n\n' + history,
    author="{{ cookiecutter.full_name.replace('\"', '\\\"') }}",
    author_email='{{ cookiecutter.email }}',
    url='https://github.com/{{ cookiecutter.github_username }}/{{ cookiecutter.project_slug }}',
    packages=find_packages(),
    {%- if 'no' not in cookiecutter.command_line_interface|lower %}
    entry_points={
        'console_scripts': [
            '{{ cookiecutter.project_slug }}={{ cookiecutter.project_slug }}.cli:main'
        ]
    },
    {%- endif %}
    include_package_data=True,
    install_requires=requirements,
{%- if cookiecutter.open_source_license in license_classifiers %}
    license="{{ cookiecutter.open_source_license }}",
{%- endif %}
    zip_safe=False,
    keywords='{{ cookiecutter.project_slug }}',
    classifiers=[
        'Development Status :: 2 - Pre-Alpha',
        'Intended Audience :: Developers',
{%- if cookiecutter.open_source_license in license_classifiers %}
        '{{ license_classifiers[cookiecutter.open_source_license] }}',
{%- endif %}
        'Natural Language :: English',
        'Programming Language :: Python :: 3.6',
    ],
    test_suite='tests',
    tests_require=test_requirements,
    setup_requires=setup_requirements,
)
