from setuptools import setup, find_packages

from rptree import __version__


setup(
    name="rptree",
    version=__version__,
    description="A directory tree generator for the command line",
    author="Real Python",
    license="MIT",
    packages=find_packages(),
    include_package_data=True,
    install_requires=[
        "pathspec>=0.10",
    ],
    entry_points={
        "console_scripts": [
            "rptree=rptree.__main__:main",
        ],
    },
    python_requires=">=3.8",
)