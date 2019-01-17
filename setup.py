from setuptools import setup, find_packages

name = "jupyter_server_extension"
version = "0.1"

setup_args = dict(
    name            = name,
    description     = "Jupyter server extension as a jupyter application",
    long_description = """
    """,
    version         = version,
    packages        = find_packages(),
    author          = 'Jupyter Development Team',
    author_email    = 'jupyter@googlegroups.com',
    url             = 'http://jupyter.org',
    license         = 'BSD',
    platforms       = "Linux, Mac OS X, Windows",
    keywords        = [],
    classifiers     = [
        'Intended Audience :: Developers',
        'Intended Audience :: System Administrators',
        'Intended Audience :: Science/Research',
        'License :: OSI Approved :: BSD License',
        'Programming Language :: Python',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3',
    ],
    zip_safe = False,
    install_requires = [
    ],
    extras_require = {
    },
    python_requires = '>=3.4', 
)


# Run setup --------------------
def main():
    setup(**setup_args)

if __name__ == '__main__':
    main()
