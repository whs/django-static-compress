from setuptools import find_packages, setup

setup(
    name="django-static-compress",
    version="2.1.0",
    url="https://github.com/whs/django-static-compress",
    author="Manatsawin Hanmongkolchai",
    author_email="manatsawin+pypi@gmail.com",
    description="Precompress Django static files with Brotli and Zopfli",
    license="MIT",
    packages=find_packages(exclude=["tests"]),
    include_package_data=True,
    install_requires=["Django", "Brotli~=1.0.9", "zopfli~=0.1.8"],
    classifiers=[
        "Development Status :: 5 - Production/Stable",
        "Environment :: Web Environment",
        "Framework :: Django",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Programming Language :: Python",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3 :: Only",
        "Programming Language :: Python :: 3.4",
        "Programming Language :: Python :: 3.5",
        "Programming Language :: Python :: 3.6",
        "Topic :: Software Development :: Pre-processors",
    ],
)
