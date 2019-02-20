from setuptools import setup, find_packages


with open('README_PYPI.md') as file:
    long_description = file.read()

setup(
    name="tpro",
    version="0.06",
    url='https://github.com/zevaverbach/tpro',
    install_requires=[
        'Click',
        'nltk',
        ],
    include_package_data=True,
    packages=find_packages(),
    description=(
        'tpro processes transcripts from speech-to-text services and outputs '
        'to various formats.'),
    long_description_content_type='text/markdown',
    long_description=long_description,
    entry_points='''
        [console_scripts]
        tpro=tpro.tpro:cli
    ''',
        )
