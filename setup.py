import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="biobb_lsvs",
    version="4.1.0",
    author="Biobb developers",
    author_email="toni.sivula@uef.fi",
    description="Biobb_lsvs is a collection of tools to do large scale virtual screening.",
    long_description=long_description,
    long_description_content_type="text/markdown",
    keywords="Bioinformatics Workflows BioExcel Compatibility",
    url="https://github.com/tonisi/biobb_lsvs",
    project_urls={
        "Documentation": "http://biobb-template.readthedocs.io/en/latest/",
        "Bioexcel": "https://bioexcel.eu/"
    },
    packages=setuptools.find_packages(exclude=['adapters', 'docs', 'test']),
    package_data={'biobb_lsvs': ['py.typed']},
    install_requires=['biobb_common==4.1.0'],
    python_requires='>=3.8',
    entry_points={
        "console_scripts": [
            "smina_run = biobb_lsvs.smina.smina_run:main"
        ]
    },
    classifiers=(
        "Development Status :: 3 - Alpha",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "License :: OSI Approved :: Apache Software License",
        "Operating System :: MacOS :: MacOS X",
        "Operating System :: POSIX",
    ),
)
