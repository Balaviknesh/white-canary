from setuptools import setup

setup(
    name='white-canary',
    version='0.2.0',
    description='Python test package',
    license='GPL v3',
    author='Balaviknesh Sekar',
    packages=['src'],
    package_data={'src': ['description.txt']
                  },
    install_requires=['flask', 'pygame', 'requests', 'wheel'],
    entry_points={
        'console_scripts': [
            'white-canary=src.app:main']
    },
    classifiers=['Operating System :: OS Independent',
                 'Operating System :: MacOS :: MacOS X',
                 'Operating System :: Microsoft :: Windows',
                 'Operating System :: POSIX',
                 'License :: OSI Approved :: GNU General Public License v3 (GPLv3)'],
)
