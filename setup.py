import setuptools


with open("README.md", "r") as fh:
    long_description = fh.read()


setuptools.setup(
    name="sqlsite",
    version="0.0.2",
    author="Jamie Matthews",
    author_email="jamie@mtth.org",
    description="A tool for serving simple websites, JSON APIs and static files directly from a SQLite database.",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/j4mie/sqlsite",
    packages=setuptools.find_packages(),
    classifiers=[
        "Topic :: Internet :: WWW/HTTP",
        "Environment :: Web Environment",
        "Programming Language :: Python :: 3",
        "License :: Public Domain",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.7',
    install_requires=[
        "apsw",
        "jinja2",
    ]
)
