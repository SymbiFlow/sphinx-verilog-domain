import setuptools

with open("README.rst", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="sphinx-verilog-domain",
    version="0.0.1",
    author="SymbiFlow Authors",
    author_email="symbiflow@lists.librecores.org",
    description="Verilog Domain for Sphinx",
    long_description=long_description,
    long_description_content_type="text/x-rst",
    url="https://github.com/SymbiFlow/sphinx-verilog-domain",
    python_requires=">=3.7",
    packages=setuptools.find_packages(),
    package_data={'': ["verilog.lark"]},
    include_package_data=True,
    install_requires=[
        'setuptools',
        'docutils',
        'sphinx',
        'lark-parser'
    ],
    classifiers=[
        'Development Status :: 4 - Beta',
        'Framework :: Sphinx :: Extension',
        'Intended Audience :: Developers',
        "License :: OSI Approved :: ISC License (ISCL)",
        "Programming Language :: Python :: 3",
        'Natural Language :: English',
        'Topic :: Documentation :: Sphinx',
    ],
)
