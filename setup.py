from setuptools import setup

with open('requirements.txt') as f:
    required = f.read().splitlines()

setup(
    name='licecomb',
    description='Check GitHub repositories for license files',
    author='Kristian Glass',
    author_email='licecomb@doismellburning.co.uk',
    url='https://github.com/doismellburning/licecomb',
    version='0.1',
    license='mit',
    install_requires=required,
    packages=['licecomb'],
    entry_points={
        "console_scripts": [
            "licecomb = licecomb:main",
        ],
    },
)
