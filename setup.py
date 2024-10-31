from setuptools import setup, find_packages

with open('README.md', 'r', encoding='utf-8') as fh:
    long_description = fh.read()

setup(
    name='remote-env',  # Ensure this matches the package name
    version='0.1.0',
    packages=find_packages(),
    install_requires=[
        'kazoo',
    ],
    author='Roman Medvedev',
    author_email='github@romavm.dev',  # Replace with your actual email
    description='Remote env for python',
    long_description=long_description,
    long_description_content_type='text/markdown',
    url='https://github.com/Romamo/remote-env',
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Intended Audience :: Developers',
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
        'Topic :: Software Development :: Libraries :: Python Modules',
    ],
    python_requires='>=3.10',
)
