import pathlib
from setuptools import setup

from rptree import __version__

HERE = pathlib.Path().cwd()
DESCRIPTION = HERE.joinpath("README.md").read_text()
VERSION = __version__


setup(
    name="rptree",
    version=VERSION,
    description="Generate directory tree diagrams for Real Python articles",
    long_description=DESCRIPTION,
    long_description_content_type="text/markdown",
    url="https://github.com/realpython/rptree",
    author="Real Python",
    author_email="info@realpython.com",
    maintainer="Leodanis Pozo Ramos",
    maintainer_email="leodanis@realpython.com",
    license="MIT",
    classifiers=[
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: Implementation :: CPython",
    ],
    packages=["rptree"],
    include_package_data=True,
    entry_points={
        "console_scripts": [
            "rptree=rptree.__main__:main",
        ]
    },
)
