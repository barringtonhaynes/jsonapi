from setuptools import setup, find_packages

setup(
    name="jsonapi",
    version="0.9",
    packages=find_packages(exclude=["tests*"]),
    license="MIT",
    description="A Python package for working with JSON API and FastAPI",
    long_description=open("README.md", encoding="utf-8").read(),
    long_description_content_type="text/markdown",
    install_requires=["pydantic>=2.3.0", "fastapi>=0.101.1"],
    url="https://github.com/barringtonhaynes/jsonapi",
    author="Barrington Haynes",
    author_email="barrington@littledog.co",
    keywords="json, api",
)
