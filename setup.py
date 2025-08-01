import codecs
from os import path

from setuptools import setup
from versioningit import get_cmdclasses

here = path.abspath(path.dirname(__file__))

with codecs.open(path.join(here, "README.md"), encoding="utf-8") as f:
    readme = f.read()

setup(
    name="python-epo-ops-client",
    cmdclass=get_cmdclasses(),
    description=(
        "Python client for EPO OPS, the European Patent Office's Open Patent Services API."
    ),
    long_description_content_type="text/markdown",
    long_description=readme,
    author="George Song",
    author_email="george@monozuku.com",
    maintainer="Andreas Motl",
    maintainer_email="andreas.motl@ip-tools.org",
    url="https://github.com/ip-tools/python-epo-ops-client",
    download_url="https://pypi.org/project/python-epo-ops-client/#files",
    packages=["epo_ops", "epo_ops.middlewares"],
    package_dir={"epo_ops": "epo_ops"},
    include_package_data=True,
    install_requires=[
        "dogpile.cache<1.5",
        "importlib-metadata; python_version<'3.8'",
        "python-dateutil<2.10",
        "requests>=2.27,<3",
        "six<2",
    ],
    extras_require={
        "develop": [
            "ruff<0.13; python_version >= '3.7'",
            "twine<7",
            "wheel<1",
        ],
        "test": [
            "pytest<9",
            "pytest-cache<2",
            "pytest-cov<6.3",
            "python-dotenv<1.2",
            "responses<0.26",
        ],
    },
    zip_safe=False,
    classifiers=[
        "Development Status :: 5 - Production/Stable",
        "Intended Audience :: Developers",
        "Natural Language :: English",
        "License :: OSI Approved :: Apache Software License",
        "Programming Language :: Python",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Programming Language :: Python :: 3.12",
        "Programming Language :: Python :: 3.13",
        "Topic :: Software Development :: Libraries",
        "Topic :: Software Development :: Libraries :: Python Modules",
    ],
    keywords=[
        "ops",
        "epo",
        "epo-ops",
        "patent-data",
        "patent-office",
        "patent-data-api",
        "european patent office",
        "open patent services",
    ],
)
