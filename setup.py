from setuptools import setup, find_packages

setup(
    name="axioma",
    version="1.0.0",
    description="Lenguaje de programacion en espanol",
    packages=find_packages(),
    entry_points={
        "console_scripts": [
            "axioma=axioma.cli:main",
        ],
    },
    python_requires=">=3.8",
)
