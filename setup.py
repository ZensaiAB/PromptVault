from setuptools import setup, find_packages

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setup(
    name="promptvault",  # Keep the distribution name as PromptVault
    version="0.1.0",
    author="Christoffer Edlund",
    author_email="christoffer@zensai.io",
    description="A utility package for managing and generating prompts for language models.",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/ZensaiAB/PromptVault",
    package_dir={"promptvault": "src"},
    packages=["promptvault", "promptvault.vault"],
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: Apache License 2.0",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.9",
)
