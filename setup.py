
from setuptools import setup, find_packages

setup(
    name='PromptVault',
    version='0.1.0',
    author='Christoffer Edlund',
    author_email='christoffer@zensai.io',
    description='A utility package for managing and generating prompts for language models.',
    long_description=open('README.md').read(),
    long_description_content_type='text/markdown',
    url='https://github.com/ZensaiAB/PromptValut', 
    packages=find_packages(),
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
    ],
    python_requires='>=3.6',
)
