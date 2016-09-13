# -*- coding: utf-8 -*-

from distutils.core import setup

setup(
    name='taskrunner',
    version='0.1',
    author='Clément zotti',
    author_email='clement.zotti@usherbrooke.ca',
    packages=['taskrunner', ],
    scripts=['bin/taskrunner',
             'bin/serverpool', ],
    url='https://github.com/czotti/taskrunner',
    license='LICENSE.txt',
    description='Easy to use taskrunner using task spooler queue.',
    long_description=open('README.md').read(),
    # install_requires=[''],
    # package_data={'': ['']}
)
