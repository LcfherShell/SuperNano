from setuptools import setup, find_packages

setup(
    name="SuperNano",
    version="2.2.1",
    author="LcfherShell",
    author_email="alfiandecker2@gmail.com",
    description="A console-based text editor built with Python and curses.",
    long_description=open('README.md').read(),
    long_description_content_type="text/markdown",
    url="https://github.com/LcfherShell/SuperNano",
    packages=find_packages(),  # This automatically finds both 'supernano' and 'utils'
    include_package_data=True,
    install_requires=[
      # Add other dependencies here
    ],
    entry_points={
        "console_scripts": [
            "supernano=supernano.__main__:main",  # Entry point untuk __main__.py
            "isupernano=supernano.install:install_script",  # Entry point untuk install.py
        ],
    },
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
)
