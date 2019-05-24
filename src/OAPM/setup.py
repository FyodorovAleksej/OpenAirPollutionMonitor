#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""The setup script."""
from pip._internal.req import parse_requirements
from setuptools import setup, find_packages

# parse_requirements() returns generator of pip.req.InstallRequirement objects
install_reqs = parse_requirements('requirements.txt', session='hack')

reqs = [str(ir.req) for ir in install_reqs]

setup(
    author="Alexey Sergeevich Fyodorov",
    author_email='Fyodorov.aleksej@gmail.com',
    classifiers=[
        'Development Status :: 2 - Pre-Alpha',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Natural Language :: English',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
    ],
    description="Open project for monitoring air pollution",
    entry_points={
        'console_scripts': [
            'dumper=dumper.cli:main',
        ],
    },
    install_requires=reqs,
    license="MIT license",
    include_package_data=True,
    keywords='air pollution',
    name='open air pollution monitor',
    packages=find_packages(include=['dumper']),
    setup_requires=reqs,
    test_suite='tests',
    tests_require=reqs,
    url='https://github.com/FyodorovAleksej/OpenAirPollutionMonitor',
    version='0.1.0',
    zip_safe=False,
)