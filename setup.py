from setuptools import find_packages, setup

setup(
    name='django-static-compress',
    version='1.0.0',
    url='http://github.com/django/channels',
    author='Django Software Foundation',
    author_email='foundation@djangoproject.com',
    description="Brings event-driven capabilities to Django with a channel system. Django 1.8 and up only.",
    license='MIT',
    packages=find_packages(exclude=['tests']),
    include_package_data=True,
    install_requires=[
        'Brotli~=0.6.0',
        'zopfli~=0.1.1',
    ],
    classifiers=[
        'Development Status :: 5 - Production/Stable',
        'Environment :: Web Environment',
        'Framework :: Django',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3 :: Only',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
        'Topic :: Software Development :: Pre-processors',
    ],
)
