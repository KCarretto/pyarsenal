"""
Setup info used by pip.
"""
from setuptools import setup, find_packages

setup(
    name="pyarsenal",
    url="https://github.com/kcarretto/pyarsenal",
    author="Kyle Carretto",
    author_email="kcarretto@gmail.com",
    version="1.2.0",
    packages=find_packages(),
    install_requires=[
        "prompt-toolkit==1.0.15",
        "fire==0.1.3",
        "requests==2.18.4",
        "colorama==0.3.9",
    ],
    entry_points={
        "console_scripts": [
            "arsenal=pyarsenal.tools.console:main",
            "arsenal-cli=pyarsenal.tools.cli:main",
        ]
    },
    license="GNU GPLv3",
    long_description="A python client for the Arsenal Red Team server. https://github.com/kcarretto/arsenal",
)
