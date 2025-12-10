import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="biobb_lsvs",
    version="5.1.0",
    author="Biobb developers",
    author_email="genis.bayarri@irbbarcelona.org",
    description="biobb_lsvs is the Biobb module collection to perform virtual screening studies.",
    long_description=long_description,
    long_description_content_type="text/markdown",
    keywords="Bioinformatics Workflows BioExcel Compatibility",
    url="https://github.com/bioexcel/biobb_lsvs",
    project_urls={
        "Documentation": "http://biobb-lsvs.readthedocs.io/en/latest/",
        "Bioexcel": "https://bioexcel.eu/",
    },
    packages=setuptools.find_packages(exclude=["docs", "test"]),
    package_data={"biobb_lsvs": ["py.typed"]},
    install_requires=["biobb_common==5.1.1"],
    python_requires=">=3.9",
    entry_points={
        "console_scripts": [
            "smina_run = biobb_lsvs.smina.smina_run:main",
        ]
    },
    classifiers=[
        "Development Status :: 5 - Production/Stable",
        "Programming Language :: Python :: 3.9",
        "License :: OSI Approved :: Apache Software License",
        "Operating System :: MacOS :: MacOS X",
        "Operating System :: POSIX",
        "Operating System :: Unix",
    ],
)
